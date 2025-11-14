from agents.llm_client import llm  # 공통 LLM 가져오기

def generate_frontend(html_layout: str) -> str:
    prompt = f"""
You are a web developer. Take the following HTML layout:
{html_layout}
Add CSS (for styling) and JS (basic interaction), then return full HTML code including <style> and <script> sections.
"""
    result = llm.invoke(prompt)
    # content 속성만 반환
    full_html = result.content.strip()
    return full_html
