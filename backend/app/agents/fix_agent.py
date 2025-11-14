def auto_fix_code(frontend_html: str, project_dir: str, verify_msg: str) -> str:
    """
    결함 메시지를 기반으로 자동 수정 수행
    예시:
    - HTML 구조 문제: <body> 태그 누락 시 추가
    - JS lint 문제: 간단한 문법 오류 자동 수정
    - CSS 오류: 기본 fallback 스타일 적용
    """
    fixed_html = frontend_html

    if "HTML missing <body> tag" in verify_msg:
        fixed_html = "<body>" + frontend_html + "</body>"

    # JS/CSS 문제는 간단 예시
    # 실제로는 GPT 모델로 수정 가능
    # ex) fixed_html = GPT_fix(frontend_html, verify_msg)

    return fixed_html
