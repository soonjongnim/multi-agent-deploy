from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

# 공통 LLM 객체
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-3.5-turbo",
    temperature=0
)
