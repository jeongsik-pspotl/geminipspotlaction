import os
import smtplib
import httpx
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# 1. 환경변수 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_USER = os.environ.get("GMAIL_USER")          # 발신용 Gmail 주소
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")  # Gmail 앱 비밀번호 (16자리)
TO_EMAIL = os.environ.get("TO_EMAIL")              # 수신용 이메일 주소

def generate_trend_report():
    """Gemini API를 활용해 IT 트렌드 요약 생성"""
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = "클라우드(Cloud), AI/ML, Spring Boot, Redis 분야의 오늘 주요 IT 소식과 핵심 기술 트렌드를 읽기 쉬운 요약 리포트 형태로 작성해줘."

    # 최신 지원 모델(gemini-2.5-flash) 적용
    client = genai.Client(
            api_key=os.environ["GEMINI_API_KEY"],
            http_options={
                "timeout": 120.0
            },  # 2분 동안 응답 대기 허용
    )
    
    # response = client.models.generate_content(
    #         model='gemini-2.5-flash',
    #         contents=prompt,
    #         )

    return response.text

def send_gmail_message(subject, content):
    """Gmail SMTP를 사용해 이메일 발송"""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    # 이메일 본문 작성
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # Gmail SMTP 서버 연결 및 발송 (Port 587 사용)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # TLS 보안 연결
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

    subject = "📧 [매일 IT 기술 트렌드 브리핑]"

    print("Gmail로 메일 발송 중...")
    if send_gmail_message(subject, report):
        print("성공적으로 이메일을 발송했습니다!")
    else:
        print("이메일 발송에 실패했습니다.")
