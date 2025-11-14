from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
frontend_content = "<h1>Loading...</h1>"

@app.get("/", response_class=HTMLResponse)
def home():
    return frontend_content

def set_frontend(html):
    global frontend_content
    frontend_content = html
