from django.core.management.base import BaseCommand
from apps.programs.models import Program


class Command(BaseCommand):
    help = "히어로스쿨 교육 과정 3종(AI 리터러시, 데이터분석, 바이브코딩) 데이터 생성"

    def handle(self, *args, **options):
        programs_data = [
            {
                "title": "AI 리터러시 히어로",
                "subtitle": "생성형 AI의 원리와 윤리 이슈를 이해하고, 실습과 카드뉴스 제작을 통해 디지털 시민 역량을 기르는 AI 리터러시 교육",
                "description": (
                    "단순한 AI 툴 사용법을 넘어 편향성과 할루시네이션 등 핵심 윤리 개념을 익히고, "
                    "프롬프트 엔지니어링과 팩트체크 과정을 거쳐 타깃 맞춤형 카드뉴스를 직접 기획·제작하는 참여형 교육입니다."
                ),
                "curriculum": [
                    {
                        "step": "1교시",
                        "title": "AI 리터러시와 윤리",
                        "content": "AI 윤리 빙고 게임을 통해 핵심 개념(편향성, 할루시네이션 등)을 익히고 실제 사례 탐색을 통해 디지털 정보 판단 능력을 기릅니다.",
                    },
                    {
                        "step": "2교시",
                        "title": "AI 윤리 이슈 분석",
                        "content": "팀별로 선정한 AI 윤리 이슈의 구조를 파악하고, 이해관계자 분석을 통해 문제의 핵심을 심층적으로 분석합니다.",
                    },
                    {
                        "step": "3교시",
                        "title": "프롬프트 기획 및 실습",
                        "content": "프롬프트 엔지니어링의 핵심 원칙을 이해하고, 생성형 AI를 활용하여 타깃 독자에게 맞는 카드뉴스 초안을 생성합니다.",
                    },
                    {
                        "step": "4교시",
                        "title": "AI 결과물 검증 및 편집",
                        "content": "AI가 생성한 초안의 사실 여부를 팩트체크하고, 타깃 독자의 수준과 공감대에 맞게 표현의 적절성을 검토·보완합니다.",
                    },
                    {
                        "step": "5교시",
                        "title": "AI 산출물 시각화",
                        "content": "카드뉴스 디자인 원칙을 학습하고 시각화 디자인을 수행하며, 전체적인 통일성을 점검하여 최종 산출물을 완성합니다.",
                    },
                    {
                        "step": "6교시",
                        "title": "결과 공유와 AI 시민성 내면화",
                        "content": "완성된 카드뉴스를 공유하여 피드백을 교환하고, 디지털 시민으로서의 역할과 다짐을 작성합니다.",
                    },
                ],
                "thumbnail_url": "https://awesomeschool-portal.s3.amazonaws.com/portal/static/images/education/literacy/main.png",
                "is_active": True,
            },
            {
                "title": "데이터분석 히어로",
                "subtitle": "노코드 AI 도구로 데이터를 분석하고 시각화하며 문제 해결 역량을 기르는 실습형 데이터 교육",
                "description": (
                    "기후 변화와 물가 등 실생활 공공데이터를 기반으로 과학적 가설을 세우고, "
                    "노코드 AI 분석 도구를 활용해 시계열·산점도 그래프를 생성하여 데이터 기반 결론을 도출하는 프로젝트형 수업입니다."
                ),
                "curriculum": [
                    {
                        "step": "1교시",
                        "title": "데이터 수사대와 가설 설정",
                        "content": "실생활 질문을 통해 기후 변화가 물가에 미치는 영향을 이해하고, 분석의 방향이 되는 과학적 가설을 수립합니다.",
                    },
                    {
                        "step": "2교시",
                        "title": "데이터 구조 탐색과 수집",
                        "content": "공공데이터의 컬럼 구조를 파악하고, 숫자 데이터만으로는 알기 어려운 상관관계를 분석해야 하는 이유를 체감합니다.",
                    },
                    {
                        "step": "3교시",
                        "title": "AI와 함께하는 데이터 시각화",
                        "content": "생성형 AI 프롬프트 엔지니어링 원칙을 배우고, 데이터 시각화 목적에 맞는 그래프 구성 요소(축, 제목, 범례)를 학습합니다.",
                    },
                    {
                        "step": "4교시",
                        "title": "변화 읽기: 시계열 분석",
                        "content": "AI를 활용해 시간대별 기온과 가격 변화를 그래프로 나타내고, 특정 시점의 데이터 변화와 특징을 비교 분석합니다.",
                    },
                    {
                        "step": "5교시",
                        "title": "데이터로 검증하기",
                        "content": "두 변수(기온, 가격) 간의 관계를 산점도로 표현하여 상관관계를 탐색하고, 초기 가설의 타당성을 검토합니다.",
                    },
                    {
                        "step": "6교시",
                        "title": "결과 해석과 데이터 피칭",
                        "content": "분석한 그래프에 근거하여 기후 위기와 물가의 관계를 설명하고, 데이터 기반 실천 방안을 발표합니다.",
                    },
                ],
                "thumbnail_url": "https://awesomeschool-portal.s3.amazonaws.com/portal/static/images/education/analytics/main.png",
                "is_active": True,
            },
            {
                "title": "바이브코딩 히어로",
                "subtitle": "자신의 진로 관점에서 학교와 지역의 문제를 발견하고, 생성형 AI와 바이브코딩을 활용해 문제를 해결하는 웹서비스를 직접 기획·제작하는 프로젝트형 AI 진로교육",
                "description": (
                    "자신의 관심 진로를 관점으로 학교와 지역의 실제 문제를 발견하고, "
                    "생성형 AI와 바이브코딩을 활용해 작동하는 웹서비스 프로토타입 제작부터 사용자 테스트, 웹 포트폴리오까지 완성하는 교육입니다."
                ),
                "curriculum": [
                    {
                        "step": "1교시",
                        "title": "바이브코딩으로 문제 바라보기",
                        "content": "바이브코딩의 원리를 이해하고, 자신의 진로 관점에서 학교와 지역의 문제를 발견하여 해결할 문제를 구체화합니다.",
                    },
                    {
                        "step": "2교시",
                        "title": "문제 파고들기와 서비스 설계",
                        "content": "AI와 동료 인터뷰를 통해 문제의 원인과 사용자 요구를 탐구하고, 서비스 핵심 기능을 정의하여 우선순위를 결정합니다.",
                    },
                    {
                        "step": "3교시",
                        "title": "프로토타입 제작하기",
                        "content": "서비스 기획안을 제작용 프롬프트로 구체화하고, 바이브코딩을 활용해 실제로 작동하는 웹서비스 프로토타입을 제작합니다.",
                    },
                    {
                        "step": "4교시",
                        "title": "사용자 테스트와 개선하기",
                        "content": "동료 사용자 테스트를 통해 실제 사용자의 반응을 확인하고, 피드백 우선순위를 판단하여 웹서비스를 수정·개선합니다.",
                    },
                    {
                        "step": "5교시",
                        "title": "서비스 완성하기",
                        "content": "남은 개선 과제를 점검해 웹서비스를 최종 보완하고, 문제와 대상·해결 방법이 드러나는 서비스 소개서를 작성합니다.",
                    },
                    {
                        "step": "6교시",
                        "title": "포트폴리오와 쇼케이스",
                        "content": "문제 발견부터 서비스 제작·개선까지의 과정을 웹 포트폴리오로 완성하고, 서로의 결과물을 탐방하며 공유합니다.",
                    },
                ],
                "thumbnail_url": "https://awesomeschool-portal.s3.amazonaws.com/portal/static/images/education/vibe/main.png",
                "is_active": True,
            },
        ]

        for item in programs_data:
            program, created = Program.objects.update_or_create(
                title=item["title"],
                defaults=item,
            )
            status_msg = "생성 완료" if created else "업데이트 완료"
            self.stdout.write(self.style.SUCCESS(f"[{status_msg}] {program.title}"))