import base64
import hashlib
import hmac
import json
import os
import secrets
import time


PASSWORD_ITERATIONS = 310_000
TOKEN_LIFETIME_SECONDS = int(os.getenv("TOKEN_LIFETIME_SECONDS", "3600"))


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${_b64encode(salt)}${_b64encode(digest)}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        scheme, iterations, salt_text, digest_text = encoded_hash.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        expected = _b64decode(digest_text)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), _b64decode(salt_text), int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str) -> str:
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": subject, "iat": now, "exp": now + TOKEN_LIFETIME_SECONDS}
    unsigned = f"{_json_segment(header)}.{_json_segment(payload)}"
    signature = hmac.new(_secret_key(), unsigned.encode("ascii"), hashlib.sha256).digest()
    return f"{unsigned}.{_b64encode(signature)}"


def decode_access_token(token: str) -> dict:
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
        header = json.loads(_b64decode(header_segment))
        if header != {"alg": "HS256", "typ": "JWT"}:
            raise ValueError("Unsupported token algorithm")
        unsigned = f"{header_segment}.{payload_segment}"
        expected = hmac.new(_secret_key(), unsigned.encode("ascii"), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, _b64decode(signature_segment)):
            raise ValueError("Invalid token signature")
        payload = json.loads(_b64decode(payload_segment))
        if not isinstance(payload.get("sub"), str) or int(payload["exp"]) <= int(time.time()):
            raise ValueError("Expired or invalid token")
        return payload
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError("Invalid access token") from error


def _secret_key() -> bytes:
    return os.getenv("JWT_SECRET_KEY", "local-development-secret-change-before-deploy").encode("utf-8")


def _json_segment(value: dict) -> str:
    return _b64encode(json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8"))


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
