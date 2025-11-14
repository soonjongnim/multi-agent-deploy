from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0)

def qa_test(html):
    prompt = PromptTemplate(
        input_variables=["html"],
        template="""
You are a QA tester for websites. Check the following HTML code:
{html}
Does it have a header (<h1>)? Does it have basic styling? Return a short summary like 'QA Passed' or 'QA Failed' with reasons.
"""
    )
    result = llm.predict(prompt.format(html=html))
    return result
