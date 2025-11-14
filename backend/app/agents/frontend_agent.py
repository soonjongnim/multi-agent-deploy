from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0)

def generate_frontend(html_layout):
    prompt = PromptTemplate(
        input_variables=["html"],
        template="""
You are a web developer. Take the following HTML layout:
{html}
Add CSS (for styling) and JS (basic interaction), then return full HTML code including <style> and <script> sections.
"""
    )
    full_html = llm.predict(prompt.format(html=html_layout))
    return full_html
