from datetime import datetime
import os
import re
import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

# 1. 환경변수 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")


def clean_text_robust(text):
    """AI 응답 텍스트 내 특수 문자, 제어 문자, 이스케이프 및 공백을 안전하게 정제"""
    if not text:
        return ""

    text = (
        text.replace("\xa0", " ")
        .replace("\u200b", "")
        .replace("\u200e", "")
        .replace("\u200f", "")
        .replace("\ufeff", "")
    )
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def wait_for_model_health(client, max_attempts=5):
    """가벼운 핑 테스트로 모델이 정상(Healthy) 상태가 될 때까지 점진적 대기"""
    print("🔍 Gemini 모델 상태 헬스체크 중...")

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents="ping",
            )
            if response and response.text:
                print("✅ Gemini 모델이 정상(Healthy) 상태입니다.")
                return True
        except Exception as e:
            print(
                f"⚠️ 모델 과부하 또는 응답 지연 감지 (시도"
                f" {attempt}/{max_attempts}): {e}"
            )
            if attempt < max_attempts:
                wait_sec = attempt * 15
                print(f"⏳ {wait_sec}초 동안 대기 후 모델 상태를 다시 확인합니다...")
                time.sleep(wait_sec)
            else:
                print("❌ 최대 헬스체크 횟수를 초과했습니다. 잠시 후 다시 시도합니다.")
                return False
    return False


def generate_trend_report(client, max_retries=3):
    """간결한 프롬프트, 504 타임아웃 대응 재시도 로직이 포함된 리포트 생성"""
    # 💡 [개선] 프롬프트를 핵심 위주로 간결하게 다듬어 504 에러 가능성을 대폭 낮춤
    prompt = (
        "Spring Boot 핵심 기술 트렌드와 백엔드"
        " 아키텍처 모범 사례를 3가지 요점으로 나누어 한국어로 간결하고 명확하게"
        " 작성해줘."
    )

    for attempt in range(1, max_retries + 1):
        try:
            print(f"📊 IT 트렌드 리포트 생성 시도 {attempt}/{max_retries}...")
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            if response and response.text:
                return clean_text_robust(response.text)
        except Exception as e:
            print(
                f"⚠️ 리포트 생성 중 타임아웃/에러 발생 (시도"
                f" {attempt}/{max_retries}): {e}"
            )
            if attempt < max_retries:
                wait_sec = attempt * 10  # 10초, 20초 간격으로 대기 시간 증가
                print(f"⏳ {wait_sec}초 대기 후 리포트 생성을 재시도합니다...")
                time.sleep(wait_sec)
            else:
                raise Exception(
                    "모든 리포트 생성 시도가 실패했습니다 (DEADLINE_EXCEEDED)."
                )

    raise Exception("리포트 생성 내용이 비어 있습니다.")


def send_gmail_message(subject, content):
    """Gmail SMTP를 사용해 이메일 발송"""
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(content, "plain", "utf-8"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"이메일 발송 중 오류 발생: {e}")
        return False


if __name__ == "__main__":
    print("🚀 IT 트렌드 자동화 파이프라인 시작...")

    # 💡 [개선] 타임아웃을 180초(180000ms)로 넉넉하게 확장하여 대형 응답 허용
    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(timeout=180000),
    )

    # 1단계: 모델 헬스체크
    if not wait_for_model_health(client):
        print("💡 서버 과부하로 인해 이번 실행을 안전하게 종료합니다.")
        exit(0)

    # 2단계: 재시도 및 간결한 프롬프트가 적용된 리포트 생성
    print("📊 IT 트렌드 리포트 생성 중...")
    try:
        report = generate_trend_report(client)
    except Exception as e:
        print(f"❌ 리포트 생성 실패: {e}")
        exit(1)

    # 3단계: Gmail 발송
    subject = "[Daily IT Tech Trend Briefing]"
    print("📧 Gmail로 메일 발송 중...")
    if send_gmail_message(subject, report):
        print("🎉 성공적으로 이메일을 발송했습니다!")
    else:
        print("❌ 이메일 발송에 실패했습니다.")
        exit(1)

    # 4단계: 레포지토리 자동 반영을 위한 Markdown 파일 저장 (GitOps 연동)
    print("📝 레포지토리 반영을 위한 마크다운 파일 생성 중...")
    os.makedirs("docs", exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    file_path = f"docs/trend-report-{today_str}.md"

    markdown_content = (
        f"# [Daily IT Tech Trend Briefing - {today_str}]\n\n{report}"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"📁 파일 생성 완료: {file_path}")