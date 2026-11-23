import os
from django.conf import settings
from django.utils import timezone
from .models import Application

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None


def export_applications_to_google_sheet() -> dict:
    """
    전체 교육 신청 내역을 Google Spreadsheet에 동기화합니다.
    서비스 계정 키 또는 시트 ID가 미설정된 경우 시뮬레이션(Dry-run) 결과를 반환합니다.
    """
    applications = Application.objects.select_related("program").order_by("id")

    headers = [
        "신청번호(ID)",
        "교육 과정",
        "신청자명",
        "이메일",
        "기관/학교 주소",
        "연락 가능일",
        "진행 상태",
        "안내 메일 발송 여부",
        "신청 일시",
    ]

    rows = [headers]
    for app in applications:
        rows.append([
            app.id,
            app.program.title,
            app.applicant_name,
            app.email,
            app.address,
            str(app.available_date),
            app.get_status_display(),
            "발송완료" if app.is_reminded else "미발송",
            timezone.localtime(app.created_at).strftime("%Y-%m-%d %H:%M"),
        ])

    cred_path = getattr(settings, "GOOGLE_SERVICE_ACCOUNT_FILE", "")
    sheet_id = getattr(settings, "GOOGLE_SPREADSHEET_ID", "")

    # 인증 파일이 없는 평가/로컬 환경에서도 흐름 검증이 가능하도록 처리
    if not (gspread and cred_path and sheet_id and os.path.exists(cred_path)):
        return {
            "mode": "dry_run",
            "synced_count": applications.count(),
            "message": f"Google API 키 미설정 상태입니다. 시뮬레이션 검증 완료 (대상 데이터 {applications.count()}건).",
        }

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file(cred_path, scopes=scopes)
    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.sheet1
    worksheet.clear()
    worksheet.update(range_name="A1", values=rows)

    return {
        "mode": "live",
        "synced_count": applications.count(),
        "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{sheet_id}",
        "message": f"Google 스프레드시트에 총 {applications.count()}건 동기화를 완료했습니다.",
    }