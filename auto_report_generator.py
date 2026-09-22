import os
import datetime
from google import genai

def generate_weekly_report():
    # 1. GitHub Secrets에서 API 키 가져오기
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

    # 2. 최신 Client 생성
    client = genai.Client(api_key=api_key)

    # 3. 오늘 날짜
    today = datetime.date.today()
    date_str = today.strftime("%Y년 %m월 %d일")

    # 4. 프롬프트
    prompt = f"""
    당신은 30년 차 보험 영업전략 및 데이터 분석 전문가입니다.
    오늘 날짜({date_str}) 기준으로 최신 보험 산업 및 GA 시장 동향 리포트를 작성해 주세요.

    [리포트 포함 내용]
    1. 금주 주요 경제 및 보험 시장 이슈
    2. GA(단독/연합) 채널 영업 및 상품 동향
    3. 현장 영업 조직을 위한 핵심 전략 추천

    [작성 규칙]
    - 모바일 및 PC에서 보기 편한 세련되고 현대적인 HTML 문서로 작성해 주세요.
    - <html> ~ </html> 태그를 포함하여 완전한 HTML 코드로 작성해 주세요.
    - 마크다운 블록(```html ... ```) 없이 순수 HTML 코드만 출력해 주세요.
    """

    print("Gemini API 호출 중...")
    
    # 최신 SDK 표준 gemini-1.5-flash 지정
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

    content = response.text.strip()
    
    # 마크다운 태그 제거
    if content.startswith("```html"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
        
    content = content.strip()

    # 5. index.html 파일 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("index.html 리포트 생성이 완료되었습니다.")

if __name__ == "__main__":
    generate_weekly_report()
