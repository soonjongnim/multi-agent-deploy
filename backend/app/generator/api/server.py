import json
def handler(request):
    # 요청 받기
    data = request.get_json() if hasattr(request, 'get_json') else {}
    prompt = data.get('prompt', 'default')

    # 생성된 프론트 HTML 반환 (여기선 단순 응답 예시)
    return {
        "status": "ok",
        "message": "Site generated",
        "prompt": prompt,
        "html": '<h1>ㅁㄴㅂ</h1>'
    }
