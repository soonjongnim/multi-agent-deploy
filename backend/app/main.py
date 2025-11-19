# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.backend_agent import create_backend_api
from utils.file_saver import save_files_to_generator_folder
import subprocess
import threading
from dotenv import load_dotenv
import os
import socket

load_dotenv()
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
#print("VERCEL_TOKEN: ", VERCEL_TOKEN)
class PromptPayload(BaseModel):
    prompt: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프론트엔드 주소 넣어도 됨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

deploy_cmd = [
    "vercel",
    "deploy",
    "--prod",
    "--yes",
    "--confirm",
    "--no-clipboard",
    "--token", VERCEL_TOKEN
]

def find_free_port(start_port=9000):
    """비어있는 포트 자동 탐색"""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
        port += 1

@app.get("/")
def root():
    return {"message": "Main Agent Server Running"}

@app.post("/generate")
async def generate_site(payload: PromptPayload):
    # 1️⃣ 프론트엔드에서 생성 (예시 고정값)
    prompt = payload.prompt
    print(f"Received prompt: {prompt}")  # 서버 콘솔에 출력
    # prompt = payload.get("prompt", "My Portfolio")
    # 2️⃣ 프론트엔드 파일 생성
    frontend_html = f"<h1>{prompt}</h1>"
    frontend_js = "console.log('Generated Site Loaded')"

     # 3️⃣ 백엔드 파일 생성
    backend_code = create_backend_api(frontend_html)

    # 4️⃣ 생성된 파일 저장
    save_files_to_generator_folder(frontend_html, frontend_js, backend_code)

    # 5️⃣ 프리뷰 서버 자동 실행
    preview_port = find_free_port(9000)
    print(f"[PREVIEW] Running preview server on port {preview_port}")

    subprocess.Popen(
        ["uvicorn", "preview_server:app", "--host", "127.0.0.1", "--port", str(preview_port)],
        cwd="generator",
        stdout=None,   # 로그를 콘솔에 바로 보기 위해 None으로 변경
        stderr=None,
        shell=True
    )

    preview_url = f"http://127.0.0.1:{preview_port}"

    return {
        "prompt": prompt,
        "preview_url": preview_url,
        "message": "Preview server launched successfully"
    }

@app.post("/deploy")
async def deploy_site():
    # 4️⃣ Vercel 배포 자동화
    deploy_process = subprocess.run(
        deploy_cmd,
        cwd="generator",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        shell=True,
        text=True,
        encoding='utf-8'
    )

    print("배포 성공!")
    # Vercel CLI는 배포 URL을 표준 출력으로 반환합니다.
    deployment_url = deploy_process.stdout.strip()
    print("=== Vercel STDOUT ===")
    print(f"배포 URL: {deployment_url}")
    print("=== Vercel STDERR ===")
    print(deploy_process.stderr)

    return {
        "deploy_output": deployment_url,
        "deploy_error": deploy_process.stderr
    }
