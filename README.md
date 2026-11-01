# 🚀 Daily AI-Powered IT Trend Notifier & Automation Pipeline

> ⚠️ **프로젝트 상태 안내 (Project Status: Paused)**  
> 본 프로젝트는 **Google Gemini API의 무료 티어(Free Tier) 일일 호출 제한(20회/일)** 및 **유료 플랜 전환 필요성**으로 인해 메일 발송 및 자동화 파이프라인 작업이 **일시 중단(Pause)**된 상태입니다.  
> 추가적인 유료 플랜 연동 전까지 메일 브리핑 자동 발송 기능의 정상 동작이 어려워 개발 및 운용을 잠시 보류합니다.

---

## 📊 프로젝트 완성률 (Completion Rate: **90% - Paused**)

- [x] **Core Logic:** Gemini API 연동 및 맞춤형 프롬프트 설계 (100%)
- [x] **Fault Tolerance & Resilience:** 서버 과부하(`503`/`504`) 대응 헬스체크, 타임아웃 확장(180s) 및 백오프 재시도 로직 (100%)
- [x] **Text Sanitization:** 특수 공백(`\xa0`) 및 제어 문자 정제 파이프라인 (100%)
- [x] **Delivery System:** Gmail SMTP 연동 및 UTF-8 헤더 인코딩 구현 완료 (100%) *(API 유료 전환 이슈로 일시 중단)*
- [x] **CI/CD Automation:** GitHub Actions 크론 스케줄링 (KST 기준 매일 밤 10시 5분) 구축 (100%)
- [x] **GitOps Integration:** 생성된 리포트를 저장소 내 `docs/` 마크다운(`.md`) 파일로 자동 생성 및 커밋/푸시 파이프라인 완성 (100%)

---

## 1. 프로젝트 정의 및 목표 (Project Definition)

- **목표:** 백엔드 엔지니어의 실무 역량 강화를 위한 자율형 에이전트 및 자동화 파이프라인 구축. 수동으로 찾아보기 번거로운 **Spring Boot, Cloud, AI/ML** 등 핵심 백엔드 기술 트렌드를 AI가 매일 요약하여 개인 메일함과 저장소 문서로 자동 배달 및 저장합니다.
- **핵심 가치:**
    * 외부 API 연동 시 발생할 수 있는 네트워크 지연 및 서버 과부하 상황을 프로그래밍적으로 방어하는 **견고한 예외 처리(Resilience)** 구현.
    * 퍼블릭(Public) 저장소 공개 시 민감 정보 유출을 원천 차단하는 **보안 아키텍처** 적용.
    * AI 응답 결과를 저장소 버전 관리에 자동 등록하는 **GitOps 파이프라인** 구현.

---

## 2. 주요 기능 및 구현 목록 (Features & Architecture)

| 구분 | 기능 명칭 | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| **AI Engine** | Gemini API 연동 (`gemini-3.8-flash`) | 최신 모델을 활용해 핵심 IT 기술 스택 및 백엔드 아키텍처 모범 사례 요약 리포트 생성 | API Quota 제약 |
| **Resilience** | 사전 헬스체크 및 3분 타임아웃 확장 | 본문 요청 전 `"ping"` 헬스체크 및 `timeout=180000ms` 확장으로 타임아웃 최소화 | 정상 구현 |
| **Retry Logic** | 지능형 재시도 로직 (`generate_trend_report`) | `504 DEADLINE_EXCEEDED` 감지 시 백오프 대기(10s $\rightarrow$ 20s) 후 최대 3회 재시도 | 정상 구현 |
| **Sanitizer** | 텍스트 정제 파이프라인 (`clean_text_robust`) | 유니코드 특수 공백(`\xa0`, `\u200b` 등) 및 제어 문자를 제거하여 인코딩 에러 예방 | 정상 구현 |
| **Delivery** | Gmail SMTP 자동 발송 (`smtplib`) | TLS 보안 연결(Port 587) 및 UTF-8 헤더 인코딩을 통한 안정적인 메일 전송 | **유료 플랜 필요 (중단)** |
| **GitOps** | 문서 자동 저장 및 배포 (`docs/`) | 메일 발송 성공 후 `docs/trend-report-YYYY-MM-DD.md`로 자동 저장 및 Git Push 연동 | 정상 구현 |
| **CI/CD** | GitHub Actions Cron Automation | 매일 한국 시간(KST) 밤 10시 5분(`5 13 * * *` UTC)에 무인 자동 실행 | **중단 중** |

---

## 3. 트러블슈팅 및 해결 과정 (How Challenges Are Handled)

파이프라인 구축 과정에서 직면했던 대표적인 장애 요소들과 이를 해결한 엔지니어링 접근 방식입니다.

- **Issue 1: 무료 티어 API 할당량 초과 (`429 RESOURCE_EXHAUSTED`) [작업 중단 원인]**
    * *원인:* Gemini Free Tier 한도(일일 20회) 및 트래픽 과부하로 인해 지속적인 `429 RESOURCE_EXHAUSTED` 에러 발생.
    * *현황:* 정상적인 Daily 메일 발송 파이프라인 운용을 위해서는 **유료 플랜(Pay-as-you-go) 전환이 필수적**이므로 메일 발송 연동을 일시 보류함.
- **Issue 2: 서버 과부하 및 타임아웃 (`503 UNAVAILABLE` / `504 DEADLINE_EXCEEDED`)**
    * *원인:* 전 세계 트래픽 피크 시간대에 요청 전송 시 서버 응답 지연으로 타임아웃 발생.
    * *해결:*
        1. HTTP 클라이언트 옵션 타임아웃을 `180000ms`(3분)로 넉넉하게 확장.
        2. 가벼운 핑 테스트로 모델 상태를 검증하는 `wait_for_model_health` 함수 적용.
        3. `generate_trend_report` 함수에 `max_retries=3` 재시도 및 대기(Backoff) 로직을 추가하여 회복력(Resilience) 대폭 향상.
- **Issue 3: SMTP 이메일 발송 시 인코딩 크래시 (`UnicodeEncodeError: 'ascii' codec can't encode character '\xa0'`)**
    * *원인:* AI가 생성한 텍스트 내부에 논브레이킹 스페이스(`\xa0`) 등이 포함되어 ASCII 인코딩 실패.
    * *해결:* 정규식과 문자열 치환 메서드를 결합한 `clean_text_robust` 함수를 구현하여 모든 제어 문자와 특수 공백을 정제.

---

## 4. 실행 결과 예시 (Expected Output Example)

파이프라인이 정상적으로 작동하여 수신된 이메일 브리핑 리포트 및 `docs/` 폴더에 생성되는 마크다운 예시입니다.

```text
Subject: [Daily IT Tech Trend Briefing]

# [Daily IT Tech Trend Briefing - 2026-10-31]

1. Spring Boot 3.x 가비지 컬렉션(GC) 성능 최적화 및 Virtual Threads 적용 모범 사례
2. 분산 환경에서의 Redis 캐싱 전략 및 데이터 일관성 보장 방안
3. 클라우드 고가용성 아키텍처와 백엔드 서킷 브레이커(Circuit Breaker) 패턴 도입 가이드
```

---

## 5. 시작하기 및 로컬 실행 방법 (Getting Started)

1. **저장소 클론 및 패키지 설치**
   ```bash
   git clone https://github.com/your-username/gemini-trend-notifier.git
   cd gemini-trend-notifier
   pip install -r requirements.txt
   ```

2. **환경변수 설정 (`.env` 파일 생성)**
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   GMAIL_USER=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_gmail_app_password
   TO_EMAIL=recipient_email@gmail.com
   ```

3. **로컬 스크립트 실행 테스트**
   ```bash
   python main.py
   ```