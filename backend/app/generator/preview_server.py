from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATOR_DIR = os.path.join(BASE_DIR)  # frontend.html, frontend.js가 저장된 폴더

@app.get("/")
async def root():
    html_path = os.path.join(GENERATOR_DIR, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    return HTMLResponse("<h1>No preview available</h1>")

@app.get("/frontend.js")
async def serve_js():
    js_path = os.path.join(GENERATOR_DIR, "app.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse("// No JS available", media_type="application/javascript")
