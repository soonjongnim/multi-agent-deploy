from agents.llm_client import llm  # 공통 LLM 가져오기

# 디자인 레이아웃 생성 함수
def create_layout(user_request: str) -> str:
    """
    사용자의 웹사이트 요청(user_request)을 받아
    간단한 HTML 레이아웃(HTML만, CSS/JS 제외)을 생성합니다.
    """
    prompt = f"""
You are a professional web designer. Create a simple HTML layout (without CSS/JS) 
for a website with the following description: {user_request}.
Output only HTML code.
"""
    result = llm.invoke(prompt)
    # content 속성만 반환
    html = result.content.strip()
    return html
