# 🚀 Daily AI-Powered IT Trend Notifier & Automation Pipeline

> **GitHub Actions와 Google Gemini API를 연동하여 매일 최신 IT 기술 트렌드를 자동으로 수집·정제하고, Gmail로 브리핑 리포트를 발송하는 무중단 백엔드 자동화 파이프라인 프로젝트입니다.**

---

## 📊 프로젝트 완성률 (Completion Rate: **95%**)

- [x] **Core Logic:** Gemini API 연동 및 맞춤형 프롬프트 설계 (100%)
- [x] **Fault Tolerance & Resilience:** 서버 과부하(`503`/`504`) 대응 헬스체크 및 백오프 대기 로직 (100%)
- [x] **Text Sanitization:** 특수 공백(`\xa0`) 및 제어 문자 정제 파이프라인 (100%)
- [x] **Delivery System:** Gmail SMTP 연동 및 UTF-8 헤더 인코딩 (100%)
- [x] **CI/CD Automation:** GitHub Actions 크론 스케줄링 (KST 기준 매일 밤 10시 5분) 구축 (100%)
- [ ] **Extension:** 생성된 리포트를 GitHub 저장소 내 Markdown(`.md`) 파일로 자동 커밋 및 푸시 기능 추가 (진행 중)

---

## 1. 프로젝트 정의 및 목표 (Project Definition)

* **목표:** 백엔드 엔지니어의 실무 역량 강화를 위한 자율형 에이전트 및 자동화 파이프라인 구축. 수동으로 찾아보기 번거로운 **Cloud, AI/ML, Spring Boot, Redis** 등 핵심 기술 트렌드를 AI가 매일 요약하여 개인 메일함으로 자동 배달합니다.
* **핵심 가치:**
    * 외부 API 연동 시 발생할 수 있는 네트워크 지연 및 서버 과부하 상황을 프로그래밍적으로 방어하는 **견고한 예외 처리(Resilience)** 구현.
    * 퍼블릭(Public) 저장소 공개 시 민감 정보 유출을 원천 차단하는 **보안 아키텍처** 적용.

---

## 2. 주요 기능 및 구현 목록 (Features & Architecture)

| 구분 | 기능 명칭 | 설명 |
| :--- | :--- | :--- |
| **AI Engine** | Gemini API 연동 (`gemini-3.8-flash`) | 최신 모델을 활용해 지정된 IT 기술 스택의 핵심 트렌드 요약 리포트 생성 |
| **Resilience** | 사전 헬스체크 및 백오프 (`wait_for_model_health`) | 본문 요청 전 `"ping"` 테스트를 수행하여 서버 과부하 감지 시 점진적 대기(15s $\rightarrow$ 30s) 후 실행 |
| **Sanitizer** | 텍스트 정제 파이프라인 (`clean_text_robust`) | 유니코드 특수 공백(`\xa0`, `\u200b` 등) 및 제어 문자를 제거하여 인코딩 에러 예방 |
| **Delivery** | Gmail SMTP 자동 발송 (`smtplib`) | TLS 보안 연결(Port 587) 및 UTF-8 헤더 인코딩을 통한 안정적인 메일 전송 |
| **CI/CD** | GitHub Actions Cron Automation | 매일 한국 시간(KST) 밤 10시 5분(`5 13 * * *` UTC)에 무인 자동 실행 |

---

## 3. 트러블슈팅 및 해결 과정 (How Challenges Are Handled)

파이프라인 구축 과정에서 직면했던 대표적인 장애 요소들과 이를 해결한 엔지니어링 접근 방식입니다.

* **Issue 1: 서버 과부하 및 타임아웃 (`503 UNAVAILABLE` / `504 DEADLINE_EXCEEDED`)**
    * *원인:* 전 세계 트래픽 피크 시간대에 대형 프롬프트를 전송할 경우 서버가 응답을 주지 못하고 커넥션이 끊기는 현상 발생.
    * *해결:*
        1. HTTP 클라이언트 옵션에 밀리초 단위 타임아웃(`types.HttpOptions(timeout=120000)`)을 넉넉하게 부여.
        2. 무거운 요청을 보내기 전 가벼운 핑 테스트로 모델 상태를 검증하는 `wait_for_model_health` 함수를 도입하여 서버가 안정화될 때까지 지능적으로 대기하도록 설계.
* **Issue 2: SMTP 이메일 발송 시 인코딩 크래시 (`UnicodeEncodeError: 'ascii' codec can't encode character '\xa0'`)**
    * *원인:* AI가 생성한 텍스트 내부에 눈에 보이지 않는 논브레이킹 스페이스(`\xa0`) 등이 포함되어 있어 파이썬 기본 인코딩(ASCII) 과정에서 예외 발생.
    * *해결:* 정규식과 문자열 치환 메서드를 결합한 `clean_text_robust` 함수를 구현하여, 메일 전송 직전 모든 제어 문자와 숨은 공백을 완벽하게 정제.

---

## 4. 실행 결과 예시 (Expected Output Example)

파이프라인이 정상적으로 작동하여 수신된 이메일 브리핑 리포트의 예시 구조입니다.

```text
Subject: [Daily IT Tech Trend Briefing]

[Daily IT Tech Trend Briefing - 2026.10.31]

1. Cloud & Architecture
- AWS Landing Zone 기반 멀티 아키텍처 재해복구(DR) 자동화 트렌드
- MSA 환경에서의 분산 트랜잭션 관리와 SAGA 패턴 적용 모범 사례

2. Spring Boot & Backend
- Spring Boot 3.x 환경에서의 가비지 컬렉션(GC) 성능 최적화 전략
- Virtual Threads(Project Loom) 도입에 따른 고도화된 I/O 처리 성능 비교

3. AI/ML & Redis Caching
- 분산 캐시 환경에서 Redis Cluster 장애 대응 및 락(Lock) 안정성 확보 방안
- 로컬 LLM 프로토타이핑을 위한 M1 Pro 기반 경량화 파이프라인 구축 사례
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