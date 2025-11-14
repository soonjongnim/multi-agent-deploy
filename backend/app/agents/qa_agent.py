from agents.llm_client import llm  # 공통 LLM 가져오기

def qa_test(html: str) -> str:
    prompt = f"""
You are a QA tester for websites. Check the following HTML code:
{html}
Does it have a header (<h1>)? Does it have basic styling? Return a short summary like 'QA Passed' or 'QA Failed' with reasons.
"""
    result = llm.invoke(prompt)
    # content 속성만 반환
    qa_result = result.content.strip()
    return qa_result
