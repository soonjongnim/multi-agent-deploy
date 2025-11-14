import openai, os, json
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_verify_and_fix(content: str, stage: str) -> (str, bool, str):
    """
    GPT를 사용해 코드/디자인/프론트엔드/백엔드 검증
    - 문제 없으면 그대로 반환
    - 문제 있으면 GPT가 수정 후 반환
    """
    prompt = f"""
You are an expert {stage} reviewer and fixer.
1. Review the following {stage} code/content.
2. Identify any issues or defects.
3. If issues exist, rewrite/fix the code to correct them.
4. Return JSON: {{ "fixed": "<fixed_content>", "issues_found": true/false, "message": "description" }}
Content:
{content}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    try:
        result = json.loads(response.choices[0].message.content.strip())
        return result["fixed"], result["issues_found"], result["message"]
    except Exception as e:
        return content, True, f"GPT parsing error: {e}"
