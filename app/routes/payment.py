import os
import uuid
from urllib.parse import quote

import httpx
import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.auth import get_current_user
from app.database import iter_connection
from app.responses import api_response


router = APIRouter(prefix="/payments", tags=["payments"])
PORTONE_API_BASE = "https://api.portone.io"
PORTONE_TIMEOUT = httpx.Timeout(60.0, connect=5.0)


class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_id: int = Field(gt=0)


class CompletePaymentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paymentId: str = Field(min_length=1, max_length=255, strict=True)


def _portone_config() -> tuple[str, str, str]:
    required = {
        name: os.getenv(name, "").strip()
        for name in ("PORTONE_STORE_ID", "PORTONE_CHANNEL_KEY", "PORTONE_API_SECRET")
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Payment service is not configured (missing: {', '.join(missing)})",
        )
    return required["PORTONE_STORE_ID"], required["PORTONE_CHANNEL_KEY"], required["PORTONE_API_SECRET"]


@router.post("/orders")
def create_order(
    payload: CreateOrderRequest,
    current_user: sqlite3.Row = Depends(get_current_user),
    connection: sqlite3.Connection = Depends(iter_connection),
):
    store_id, channel_key, _ = _portone_config()
    course = connection.execute(
        "SELECT id, title, price FROM courses WHERE id = ?",
        (payload.course_id,),
    ).fetchone()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    existing_enrollment = connection.execute(
        "SELECT 1 FROM enrollments WHERE user_id = ? AND course_id = ?",
        (current_user["id"], course["id"]),
    ).fetchone()
    if existing_enrollment is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course already purchased")

    pending_order = connection.execute(
        """SELECT payment_id, order_name, amount FROM payment_orders
           WHERE user_id = ? AND course_id = ? AND status = 'PENDING'
           ORDER BY created_at LIMIT 1""",
        (current_user["id"], course["id"]),
    ).fetchone()
    created = pending_order is None
    if pending_order is None:
        payment_id = f"course-{uuid.uuid4().hex}"
        order_name = course["title"]
        amount = course["price"]
        try:
            connection.execute(
                """INSERT INTO payment_orders
                   (payment_id, user_id, course_id, order_name, amount, currency, status)
                   VALUES (?, ?, ?, ?, ?, 'KRW', 'PENDING')""",
                (payment_id, current_user["id"], course["id"], order_name, amount),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            # The partial unique index handles simultaneous order requests too.
            pending_order = connection.execute(
                """SELECT payment_id, order_name, amount FROM payment_orders
                   WHERE user_id = ? AND course_id = ? AND status = 'PENDING'
                   ORDER BY created_at LIMIT 1""",
                (current_user["id"], course["id"]),
            ).fetchone()
            if pending_order is None:
                raise
            created = False
            payment_id = pending_order["payment_id"]
            order_name = pending_order["order_name"]
            amount = pending_order["amount"]
    else:
        payment_id = pending_order["payment_id"]
        order_name = pending_order["order_name"]
        amount = pending_order["amount"]

    return api_response(
        status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        "Payment order created" if created else "Pending payment order reused",
        {
            "paymentId": payment_id,
            "orderName": order_name,
            "amount": amount,
            # PortOne Browser SDK's currency enum for Korean won.
            "currency": "CURRENCY_KRW",
            "storeId": store_id,
            "channelKey": channel_key,
            "customer": {
                "fullName": current_user["name"],
                "email": current_user["email"],
            },
        },
    )


@router.post("/complete")
async def complete_payment(
    payload: CompletePaymentRequest,
    current_user: sqlite3.Row = Depends(get_current_user),
    connection: sqlite3.Connection = Depends(iter_connection),
):
    _, _, api_secret = _portone_config()
    order = connection.execute(
        """SELECT payment_id, user_id, course_id, amount, currency, status
           FROM payment_orders WHERE payment_id = ? AND user_id = ?""",
        (payload.paymentId, current_user["id"]),
    ).fetchone()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment order not found")

    payment_url = f"{PORTONE_API_BASE}/payments/{quote(payload.paymentId, safe='')}"
    try:
        async with httpx.AsyncClient(timeout=PORTONE_TIMEOUT) as client:
            response = await client.get(
                payment_url,
                headers={"Authorization": f"PortOne {api_secret}"},
            )
        response.raise_for_status()
        portone_payment = response.json()
    except (httpx.HTTPError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not verify payment with PortOne",
        ) from None

    verified = (
        isinstance(portone_payment, dict)
        and _payment_matches_order(portone_payment, order)
    )
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="PortOne payment status or order amount does not match",
        )

    # Keep payment and enrollment changes atomic and safe under duplicate callbacks.
    with connection:
        current_order = connection.execute(
            """SELECT status, course_id FROM payment_orders
               WHERE payment_id = ? AND user_id = ?""",
            (payload.paymentId, current_user["id"]),
        ).fetchone()
        if current_order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment order not found")
        if current_order["status"] == "PENDING":
            connection.execute(
                """UPDATE payment_orders SET status = 'PAID', paid_at = CURRENT_TIMESTAMP
                   WHERE payment_id = ? AND user_id = ? AND status = 'PENDING'""",
                (payload.paymentId, current_user["id"]),
            )
        elif current_order["status"] != "PAID":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment order is not payable")

        connection.execute(
            """INSERT OR IGNORE INTO enrollments (user_id, course_id, payment_id)
               VALUES (?, ?, ?)""",
            (current_user["id"], current_order["course_id"], payload.paymentId),
        )

    return api_response(
        status.HTTP_200_OK,
        "Payment verified and enrollment granted",
        {"paymentId": payload.paymentId, "status": "PAID", "course_id": current_order["course_id"]},
    )


def _payment_matches_order(payment: dict, order: sqlite3.Row) -> bool:
    amount = payment.get("amount")
    return (
        payment.get("id") == order["payment_id"]
        and payment.get("status") == "PAID"
        and isinstance(amount, dict)
        and type(amount.get("total")) is int
        and amount["total"] == order["amount"]
        and payment.get("currency") == order["currency"] == "KRW"
        and payment.get("storeId") == os.getenv("PORTONE_STORE_ID", "").strip()
    )


@router.get("/enrollments")
def list_enrollments(
    current_user: sqlite3.Row = Depends(get_current_user),
    connection: sqlite3.Connection = Depends(iter_connection),
):
    rows = connection.execute(
        "SELECT course_id FROM enrollments WHERE user_id = ? ORDER BY course_id",
        (current_user["id"],),
    ).fetchall()
    return api_response(
        status.HTTP_200_OK,
        "Enrollments retrieved successfully",
        {"course_ids": [row["course_id"] for row in rows]},
    )
