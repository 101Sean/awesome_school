# 어썸스쿨 (Awesome School) 찾아가는 교육 신청 포털

어썸스쿨의 대표 교육 프로그램 소개, 비동기 교육 신청 접수, 관리자 전용 운영 대시보드, 연락 가능 날짜 기준 자동 안내 메일 발송, 그리고 Google Spreadsheet API 연동 기능을 갖춘 풀스택 웹 애플리케이션입니다.

---

## 1. 프로젝트 개요 및 설계 의도

### 디렉토리 구조 및 도메인 분리 (`programs` vs `applications`)
데이터의 성격(조회 중심 정적 콘텐츠 vs 트랜잭션 중심 운영 데이터)과 권한 경계에 따라 두 개의 독립된 Django App으로 분리했습니다.

```text
awesome_school/
├── backend/
│   ├── apps/
│   │   ├── programs/          # [교육 과정 도메인] Read-Heavy 교육 프로그램 및 차시별 커리큘럼 API
│   │   └── applications/      # [교육 신청 도메인] Write-Heavy 신청 접수, 관리자 CRUD, 메일 배치, 시트 연동
│   ├── config/                # 프로젝트 전역 설정(settings.py) 및 URL 라우팅
│   ├── templates/
│   │   ├── index.html         # 사용자 랜딩 페이지 및 비동기 교육 신청 폼
│   │   └── manage.html        # 관리자 전용 신청 현황 대시보드
│   └── manage.py
├── docker-compose.yml         # 로컬 개발용 PostgreSQL 컨테이너 구성
├── .env.example               # 환경변수 템플릿
└── requirements.txt
```

- **단방향 의존성 설계:** `applications` 앱이 `programs` 앱을 `ForeignKey`로 단방향 참조하도록 구성하여 도메인 간 결합도를 낮추고 순환 참조를 방지했습니다.
- **권한 경계(Permission Boundary) 분리:** 교육 과정 조회(`GET /api/programs/`)와 교육 신청 접수(`POST /api/applications/`)는 외부 사용자에게 개방(`AllowAny`)하고, 신청 내역 목록 조회·상태 변경(`PATCH`)·삭제(`DELETE`) 및 자동화 배치 트리거는 관리자(`IsAdminUser`) 전용으로 보호했습니다.
- **배치 작업의 멱등성(Idempotency) 보장:** 자동 안내 메일 발송(`send_reminders`) 실행 시 `is_reminded` 플래그와 `reminded_at` 타임스탬프를 기록하여, 스케줄러가 중복 실행되더라도 동일 신청자에게 메일이 재발송되지 않도록 설계했습니다.
- **외부 의존성 Graceful Fallback:** 로컬 및 심사 환경에서 별도의 SMTP 계정이나 Google Cloud 인증 키, PostgreSQL 데몬이 없더라도 즉시 동작·검증할 수 있도록 콘솔 메일 백엔드, Google Sheets 시뮬레이션(`dry_run`) 모드, SQLite 폴백 구성을 지원합니다.

---

## 2. 사용 기술 (Tech Stack)

- **Backend:** Python 3.9, Django 4.2, Django REST Framework (DRF)
- **Database:** PostgreSQL 15 (Docker Compose) / SQLite3
- **Frontend:** Django Templates, Tailwind CSS, Vanilla JavaScript (`Fetch API`)
- **Automation & External API:** Django Custom Management Command (`send_reminders`), `gspread` & `google-auth` (Google Sheets API v4)

---

## 3. 주요 구현 기능

1. **교육 프로그램 소개 및 비동기 신청 (`/`)**
   - 대표 교육 프로그램 카드 선택 시 차시별 상세 커리큘럼 및 신청 폼 선택값 자동 동기화
   - 과거 날짜 선택 차단(프론트엔드 `min` 속성 + 백엔드 Serializer 유효성 검증) 및 `Fetch API` 기반 비동기 접수
2. **관리자 전용 신청 관리 대시보드 (`/manage/`)**
   - `LoginRequiredMixin` 및 `IsAdminUser` 기반 접근 제어 (비로그인 접근 시 `/admin/login/` 자동 리다이렉트)
   - 진행 상태(`접수` / `확인중` / `완료`)별 실시간 통계 카드, 상태 필터링, 비동기 상태 변경(`PATCH`) 및 삭제(`DELETE`)
   - 대시보드 상단 액션 버튼을 통한 **안내 메일 일괄 발송** 및 **Google 시트 내보내기** 즉시 실행
3. **연락 가능 날짜 기준 자동 안내 메일 발송 (`send_reminders`)**
   - `available_date`가 기준일 이하이면서 미발송(`is_reminded=False`)인 신청 건을 조회해 안내 이메일 발송
   - `--date YYYY-MM-DD` CLI 옵션을 지원하여 미래 날짜 기준 발송 및 중복 발송 차단 동작을 즉시 검증 가능
4. **Google Spreadsheet API 연동 신청 목록 내보내기**
   - 서비스 계정(`Service Account`) 인증을 통해 전체 신청 내역과 안내 메일 발송 여부를 스프레드시트에 일괄 업데이트

---

## 4. AWS 배포 구성 및 운영 계획

실제 운영 환경 배포 시 안정성, 보안, 정기 배치 자동화를 고려하여 다음과 같은 AWS 아키텍처를 구성했습니다.

```text
[Client (Browser)]
       │ HTTPS (AWS Certificate Manager SSL/TLS)
       ▼
[Nginx Reverse Proxy / Application Load Balancer]
       │
       ├── 정적 파일 서빙 ──► [Amazon S3] (로고, 이미지, CSS/JS 에셋)
       │
       └── 애플리케이션 요청
              ▼
       [Amazon EC2 (Ubuntu + Docker + Gunicorn + Django)]
              │
              ├── 데이터 영속화 ──► [Amazon RDS for PostgreSQL] (Private Subnet 격리)
              ├── 보안 자격증명 ──► [AWS Secrets Manager / SSM Parameter Store]
              ├── 이메일 발송   ──► [Amazon SES] (SMTP 연동)
              └── 일일 스케줄링 ──► [Amazon EventBridge Scheduler] ──► 매일 09:00 `manage.py send_reminders` 실행
```

- **웹 애플리케이션 계층 (Amazon EC2 + Nginx + Gunicorn):** 초기 트래픽 규모와 비용 효율성을 고려해 단일 EC2(`t3.small`) 기반 Docker 환경으로 배포하며, Nginx 리버스 프록시 앞단에서 SSL/TLS 종료 및 정적 파일 처리를 수행합니다.
- **데이터베이스 격리 (Amazon RDS for PostgreSQL):** 애플리케이션 서버와 DB를 분리하고 Private Subnet에 배치해 외부 직접 접근을 차단하며, 자동 백업 및 스냅샷으로 신청 데이터의 무결성을 확보합니다.
- **배치 자동화 (Amazon EventBridge Scheduler):** 별도의 상시 워커 서버(Celery 등) 운영 부담을 줄이기 위해, EventBridge 스케줄러가 매일 오전 9시 트리거를 발생시켜 `python manage.py send_reminders` 커맨드를 실행합니다.
- **보안 및 메일 인프라 (AWS Secrets Manager & Amazon SES):** DB 접속 정보, Django `SECRET_KEY`, Google Service Account 키는 저장소에서 완전히 분리하여 Secrets Manager로 주입하고, 운영 메일 발송은 Amazon SES를 통해 도달률을 확보합니다.

---

## 5. AI 코딩 보조 도구 사용 내역 및 활용 이유

개발 생산성을 높이면서도 코드 품질과 아키텍처 일관성을 유지하기 위해 **Gemini** 및 **Claude Code CLI**를 페어 프로그래밍 도구로 활용했습니다.

### 활용 내역 및 이유
- **초기 아키텍처 검토 및 보일러플레이트 생성:** `programs`와 `applications` 앱 분리 구조 설계 검토, DRF Serializer 및 View 기본 골격 작성에 활용해 초기 세팅 시간을 단축했습니다.
- **프론트엔드 UI:** 백엔드 핵심 로직(권한 분리, 데이터 무결성, 자동화 배치)에 집중하기 위해, Tailwind CSS 기반 반응형 랜딩 페이지(`index.html`)와 관리자 대시보드(`manage.html`)의 비동기 `fetch` 스크립트 초안을 빠르게 생성했습니다.

### 개발자 직접 검증 및 개선 사항
- AI가 제안한 초기 템플릿 렌더링 방식 중 Django `QuerySet`을 `json_script`로 직렬화할 때 발생한 `TypeError` 원인을 분석하고, REST API(`/api/programs/`) 비동기 조회 방식으로 일원화해 데이터 흐름을 단순화했습니다.
- 관리자 API(`views.py`)의 권한 분기(`AllowAny` vs `IsAdminUser`) 및 Git 브랜치 병합 이력을 직접 검수하고, 외부 인증 키나 SMTP 계정이 없는 평가 환경에서도 오류 없이 동작하도록 Fallback 로직을 보완했습니다.

---

## 6. 심사자용 로컬 실행 및 테스트 가이드

### ① 저장소 클론 및 가상환경 설정
```bash
git clone [https://github.com/101Sean/awesome_school.git](https://github.com/101Sean/awesome_school.git)
cd awesome_school

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### ② 데이터베이스 실행 및 마이그레이션
*(Docker가 실행 중인 환경에서는 아래 명령어로 PostgreSQL 컨테이너를 먼저 띄웁니다.)*
```bash
docker compose up -d db
```
*(Docker 없이 로컬 SQLite로 바로 실행하려면 `.env` 미설정 상태에서 바로 아래 마이그레이션을 진행하면 됩니다.)*

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

### ③ 개발 서버 실행 및 기능 확인
```bash
python manage.py runserver
```
- **사용자 교육 신청 페이지:** `http://127.0.0.1:8000/`
  - 대표 교육 프로그램 카드 클릭 → 커리큘럼 확인 → 교육 신청 접수 테스트
- **관리자 전용 대시보드:** `http://127.0.0.1:8000/manage/`
  - 생성한 슈퍼유저 계정으로 로그인 후 상태 필터링, 상태 변경(`접수`/`확인중`/`완료`), **안내 메일 일괄 발송**, **Google 시트 내보내기** 버튼 동작 확인
- **Django Admin:** `http://127.0.0.1:8000/admin/`

### ④ 자동 안내 메일 발송 CLI 및 단위 테스트 실행
```bash
# 오늘 날짜 기준 안내 메일 발송 (터미널 콘솔에 발송 본문 출력)
python manage.py send_reminders

# 특정 미래 날짜를 지정하여 발송 테스트 (동일 날짜 재실행 시 중복 발송 차단 확인 가능)
python manage.py send_reminders --date 2026-12-01

# 핵심 비즈니스 로직 단위 테스트 실행 (총 5개 테스트 케이스 검증)
python manage.py test
```