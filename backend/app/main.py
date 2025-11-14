from agents.design_agent import create_layout
# from agents.frontend_agent import generate_frontend
# from agents.backend_agent import set_frontend
# from agents.qa_agent import qa_test
import uvicorn

# 1. 사용자 요청
user_request = "Personal portfolio website with a profile, skills section, and contact form"

# 2. 디자인 생성 (GPT)
layout_html = create_layout(user_request)

# 3. 프론트엔드 코드 생성 (GPT)
# full_html = generate_frontend(layout_html)

# # 4. 백엔드 연결
# set_frontend(full_html)

# 5. QA 테스트 (GPT)
# qa_result = qa_test(full_html)
# print("QA Result:", qa_result)

# 6. 서버 실행
if __name__ == "__main__":
    print(layout_html)

    #uvicorn.run("agents.backend_agent:app", host="127.0.0.1", port=8000, reload=True)
