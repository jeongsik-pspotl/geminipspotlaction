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

    # 1. 논브레이킹 스페이스(\xa0), 제로위치 공백(\u200b), BOM(\ufeff) 등을 일반 공백이나 빈 문자로 치환
    text = (
        text.replace("\xa0", " ")
        .replace("\u200b", "")
        .replace("\u200e", "")
        .replace("\u200f", "")
        .replace("\ufeff", "")
    )

    # 2. 줄바꿈 문자 통일 (Windows \r\n -> Unix \n)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 3. 인코딩 깨짐을 유발하는 불필요한 제어 문자 제거 (탭(\t)과 줄바꿈(\n)은 보존)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)

    # 4. 각 라인별 우측 공백 제거 및 연속된 과도한 빈 줄 정리 (선택사항)
    lines = [line.rstrip() for line in text.split("\n")]
    cleaned_text = "\n".join(lines).strip()

    return cleaned_text


def generate_trend_report():
    """Gemini API를 활용해 IT 트렌드 요약 생성"""
    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(timeout=120000),  # 2분 대기 타임아웃
    )

    prompt = (
        "클라우드(Cloud), AI/ML, Spring Boot, Redis 분야의 핵심 기술 트렌드와"
        " 백엔드 아키텍처 모범 사례를 3가지 주제로 나누어 읽기 쉬운 요약"
        " 리포트 형태로 한국어로 작성해줘."
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Gemini API 호출 시도 {attempt + 1}/{max_retries}...")
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            if response and response.text:
                # 보완된 정제 함수 적용
                return clean_text_robust(response.text)
        except Exception as e:
            print(f"시도 {attempt+1} 실패: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)  # 10초 대기 후 재시도
            else:
                raise e

    raise Exception("모든 API 호출 시도가 실패했습니다.")


def send_gmail_message(subject, content):
    """Gmail SMTP를 사용해 이메일 발송"""
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL

    # 한글 및 특수문자가 포함된 제목을 안전하게 헤더 인코딩
    msg["Subject"] = Header(subject, "utf-8")

    # 이메일 본문 작성 (UTF-8 인코딩 명시)
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
    print("IT 트렌드 리포트 생성 중...")
    report = generate_trend_report()

    subject = "[Daily IT Tech Trend Briefing]"

    print("Gmail로 메일 발송 중...")
    if send_gmail_message(subject, report):
        print("성공적으로 이메일을 발송했습니다!")
    else:
        print("이메일 발송에 실패했습니다.")