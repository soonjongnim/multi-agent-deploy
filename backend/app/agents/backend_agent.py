def create_backend_api(frontend_html: str) -> str:
    """
    FastAPI 서버를 Vercel용 Python serverless function 형태로 생성
    """
    backend_template = f"""import json
def handler(request):
    # 요청 받기
    data = request.get_json() if hasattr(request, 'get_json') else {{}}
    prompt = data.get('prompt', 'default')

    # 생성된 프론트 HTML 반환 (여기선 단순 응답 예시)
    return {{
        "status": "ok",
        "message": "Site generated",
        "prompt": prompt,
        "html": {repr(frontend_html)}
    }}
"""
    return backend_template
