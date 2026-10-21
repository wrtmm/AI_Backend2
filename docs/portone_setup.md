# PortOne 결제 설정

현재 프로젝트는 PortOne V2 SDK를 이용해 Toss Payments(신모듈) 카드 결제를 요청하도록 구성되어 있습니다. 브라우저가 결제를 요청하고, 서버가 PortOne에서 결제 정보를 다시 조회해 금액과 상태를 확인한 뒤 수강 등록을 완료합니다. 실제로 사용할 PG는 `PORTONE_CHANNEL_KEY`에 대응하는 PortOne 채널에서 결정됩니다.

## PortOne 계정과 연동 정보 준비

1. [PortOne 관리자 콘솔](https://admin.portone.io/)에서 계정을 만들고 이메일 인증을 마칩니다.
2. **결제 연동 → 연동 관리 → 채널 관리**에서 연동 모드를 **테스트**로 선택하고, 결제대행사 **토스페이먼츠**, 결제 모듈 **신모듈**, 결제 방식 **일반 결제**, 결제 수단 **신용카드**로 테스트 채널을 추가합니다. PortOne 공식 가이드는 V2 사용 시 토스페이먼츠(신모듈)로 연동하도록 안내합니다.
3. 콘솔의 **결제 연동 → 연동 관리**에서 Store ID와 방금 추가한 채널 키를 확인합니다. 기존 다른 PG 채널의 키를 설정하면 요청한 Toss Payments 경로로 결제되지 않습니다.
4. **결제 연동 → 연동 관리 → 식별코드·API Keys → V2 API**에서 API Secret을 발급하고 바로 안전한 곳에 복사합니다. API Secret은 백엔드에서만 사용하며 브라우저에 넣지 않습니다.

실제 결제를 받으려면 Toss Payments 계약, 사업자 인증 및 실연동 채널 설정이 별도로 필요합니다. 테스트 채널로 실제 청구가 이뤄지지는 않습니다.

PortOne의 [결제 연동 준비 가이드](https://developers.portone.io/opi/ko/integration/ready/readme)는 가입, 테스트 채널, 실연동 채널, Store ID 및 V2 API Secret 발급 절차를 설명합니다.

## 백엔드 환경 변수

백엔드 서버를 실행하는 PowerShell 세션에서 계정별 값을 설정합니다. 값을 저장소 파일이나 프론트엔드 환경 변수에 넣지 마세요.

```powershell
$env:PORTONE_STORE_ID = "store-..."
$env:PORTONE_CHANNEL_KEY = "channel-key-..."
$env:PORTONE_API_SECRET = "..."
$env:CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"
```

설정한 같은 터미널에서 사용자가 백엔드 서버를 시작해야 합니다. 세 변수가 비어 있으면 주문 API가 결제 준비를 거부합니다.

프론트엔드 배포 주소에서 API를 호출하려면 `frontend/.env.local`에 백엔드 주소를 지정합니다. 로컬 기본값은 `http://127.0.0.1:8000`입니다.

```dotenv
VITE_API_BASE_URL=https://api.example.com
```

운영 환경에서는 백엔드 `CORS_ORIGINS`에도 실제 프론트엔드 origin을 지정합니다.

테스트 채널을 사용하는 동안에는 테스트용 Store ID와 채널 키를 설정합니다. `PORTONE_API_SECRET`도 같은 PortOne 계정에서 발급한 V2 API Secret이어야 합니다.

## 구현된 결제 API

- `POST /payments/orders`: 로그인한 수강생이 `{ "course_id": 1 }`을 보냅니다. 서버가 강의 가격으로 주문을 생성합니다.
- `POST /payments/complete`: 브라우저가 `{ "paymentId": "..." }`을 보냅니다. 서버가 PortOne 결제 상태·금액·통화를 조회해 확인한 경우에만 수강 등록합니다.
- `GET /payments/enrollments`: 로그인한 수강생의 강의 ID를 반환합니다.

프론트엔드 SDK는 [PortOne JavaScript SDK V2](https://developers.portone.io/sdk/ko/v2-sdk/readme?v=v2)를 사용합니다. 서버 검증은 [인증 결제 연동 가이드](https://developers.portone.io/opi/ko/integration/start/v2/checkout)와 [REST API V2](https://developers.portone.io/api/rest-v2)를 따릅니다.

## 현재 범위

카드 일반결제만 연결했습니다. 결제 취소/환불, 결제 웹훅을 통한 결과 복구, 가상계좌·간편결제 및 강의 등록/수정 화면은 별도 구현이 필요합니다.
