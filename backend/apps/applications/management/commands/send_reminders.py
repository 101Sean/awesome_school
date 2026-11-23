from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.applications.models import Application


class Command(BaseCommand):
    help = "연락 가능 날짜(available_date)가 도래한 미발송 신청자에게 안내 이메일을 자동 발송"

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            help="기준 날짜를 YYYY-MM-DD 형식으로 직접 지정할 수 있습니다. (미지정 시 오늘 날짜 기준)",
        )

    def handle(self, *args, **options):
        if options["date"]:
            target_date = datetime.strptime(options["date"], "%Y-%m-%d").date()
        else:
            target_date = timezone.localdate()

        # 기준일 이전 또는 당일이면서 아직 메일이 발송되지 않은(is_reminded=False) 건만 조회
        targets = Application.objects.select_related("program").filter(
            available_date__lte=target_date,
            is_reminded=False,
        )

        if not targets.exists():
            self.stdout.write(self.style.WARNING(f"[{target_date}] 발송 대상 신청 내역이 없습니다."))
            return

        sent_count = 0
        for app in targets:
            subject = f"[어썸스쿨] '{app.program.title}' 교육 신청 안내드립니다."
            message = (
                f"안녕하세요, {app.applicant_name}님.\n"
                f"주식회사 어썸스쿨 교육 운영팀입니다.\n\n"
                f"신청하신 [{app.program.title}] 과정의 연락 가능 희망일({app.available_date})이 도래하여 안내 메일을 드립니다.\n"
                f"- 신청 기관/주소: {app.address}\n"
                f"- 현재 진행 상태: {app.get_status_display()}\n\n"
                f"담당 매니저가 기재해 주신 연락처로 곧 상세 일정 조율을 위해 연락드리겠습니다.\n"
                f"감사합니다.\n\n"
                f"주식회사 어썸스쿨 | TEL: 070-7123-1111 | info@awesome-school.net"
            )

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[app.email],
                    fail_silently=False,
                )
                # 멱등성 보장: 발송 완료 플래그 및 시각 기록
                app.is_reminded = True
                app.reminded_at = timezone.now()
                app.save(update_fields=["is_reminded", "reminded_at"])
                sent_count += 1
                self.stdout.write(self.style.SUCCESS(f"[발송 완료] #{app.id} {app.applicant_name} ({app.email})"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"[발송 실패] #{app.id} {app.email}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"총 {sent_count}건의 안내 메일 발송을 완료했습니다."))