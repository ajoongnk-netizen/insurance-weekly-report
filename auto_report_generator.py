import os
import datetime
import json
import urllib.request
import urllib.error

def generate_weekly_report():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

    today = datetime.date.today()
    date_str = today.strftime("%Y년 %m월 %d일")

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

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"Gemini API 호출 실패 (HTTP {e.code}): {error_body}")

    if content.startswith("```html"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("index.html 리포트 생성이 완료되었습니다.")

if __name__ == "__main__":
    generate_weekly_report()
