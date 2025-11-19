# backend/app/routes/generator.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.design_agent import create_layout
from agents.frontend_agent import generate_frontend
from agents.backend_agent import create_backend_api
from utils.file_saver import save_files_to_generator_folder   # 저장 함수

import subprocess
import sys
import socket
from pathlib import Path
import time

router = APIRouter()

class Prompt(BaseModel):
    prompt: str


def _find_free_port(start_port: int = 9000, max_port: int = 9100) -> int:
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found")


@router.post("/generate")
def generate(payload: Prompt):
    # Simple server-side logging
    print("/generate called with prompt:", payload.prompt)
    
    frontend_html = "<h1>Hello</h1>"
    frontend_js = "console.log('hello')"
    backend_code = create_backend_api(frontend_html)

    # 저장
    save_files_to_generator_folder(frontend_html, frontend_js, backend_code)

    # server.py 생성
    server_path = "app/generator/server.py"
    with open(server_path, "w", encoding="utf-8") as f:
        f.write(backend_code)

    # server.py 실행
    subprocess.Popen(["python", server_path])

    return {"status": "ok"}
    # 1. HTML 레이아웃 생성
    # try:
    #     html = create_layout(payload.prompt)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Design agent error: {e}")

    # # 2. 완성된 프론트엔드 코드 생성
    # try:
    #     full_frontend = generate_frontend(html)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Frontend agent error: {e}")

    # # 3. 백엔드 코드 생성
    # try:
    #     backend_code = create_backend_api(full_frontend)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Backend agent error: {e}")

    # # 4. 생성된 파일 저장 (writes to app/generator/api.py etc.)
    # try:
    #     save_files_to_generator_folder(
    #         html=html,
    #         frontend_code=full_frontend,
    #         backend_code=backend_code,
    #     )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"File save error: {e}")

    # # 5. Start a new uvicorn process to serve the generated api if possible
    # try:
    #     # find free port starting at 9000
    #     port = _find_free_port(9000, 9200)

    #     # backend dir is two parents above this routes file (repo/backend)
    #     backend_dir = Path(__file__).resolve().parents[2]

    #     # spawn uvicorn as a subprocess using the package import path
    #     cmd = [sys.executable, "-m", "uvicorn", "app.generator.api:app", "--port", str(port)]
    #     proc = subprocess.Popen(cmd, cwd=str(backend_dir))

    #     # give the server a moment to start
    #     time.sleep(0.5)

    #     url = f"http://127.0.0.1:{port}"
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Failed to start generated server: {e}")

    # return {"status": "ok", "generated_url": "http://127.0.0.1:9000"}
