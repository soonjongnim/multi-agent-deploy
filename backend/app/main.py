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
from fastapi import UploadFile, File
from pathlib import Path
import time
try:
    import whisper
except Exception:
    whisper = None
else:
    # 모델 캐시 (첫 요청에 로드)
    _whisper_model = None
import socket
try:
    from openai import OpenAI as OpenAIClient
except Exception:
    OpenAIClient = None

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


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """오디오(mp3/wav) 파일을 받아 OpenAI Whisper를 통해 텍스트로 변환하여 반환합니다.

    폼 필드: file (multipart/form-data)
    """

    # local whisper 사용: 설치되어있지 않으면 에러 반환
    if whisper is None:
        return {"error": "Local whisper is not installed on the server. Install 'openai-whisper' and ffmpeg."}

    accepted = {"audio/mpeg", "audio/wav", "audio/x-wav", "audio/vnd.wave", "audio/mp3"}
    if file.content_type not in accepted:
        return {"error": f"Unsupported content-type: {file.content_type}. Please upload mp3 or wav."}

    tmp_dir = Path("./tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".mp3" if ("mpeg" in file.content_type or file.filename.lower().endswith('.mp3')) else ".wav"
    dest = tmp_dir / f"upload_{int(time.time()*1000)}{suffix}"

    contents = await file.read()
    dest.write_bytes(contents)

    try:
        # 모델을 한 번 로드해서 재사용하는 방식으로 개선
        model_name = os.getenv("WHISPER_MODEL", "small")
        # whisper.load_model는 무겁기 때문에 애플리케이션 레벨에서 한 번만 로드해서 재사용합니다.
        global _whisper_model
        if _whisper_model is None:
            _whisper_model = whisper.load_model(model_name)
        model = _whisper_model
        transcription = model.transcribe(str(dest))
        # whisper 패키지의 transcribe 결과는 dict 형태로 'text'에 결과가 들어옵니다.
        text = transcription.get("text") if isinstance(transcription, dict) else str(transcription)

        if not text:
            return {"error": "No transcription returned from provider", "raw": transcription}

        # 요약: OpenAI GPT-3.5-turbo를 사용해서 전사 텍스트를 요약합니다.
        summary = None
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key and OpenAIClient is not None:
                # OpenAI v1 client usage (openai>=1.0.0)
                client = OpenAIClient(api_key=openai_api_key)

                prompt = (
                    "다음 회의 전사 내용을 한국어로 간결하게 요약해 주세요.\n"
                    "- 핵심 항목(3~6개) 형식으로 정리하고, 마지막에 한 줄 TL;DR을 작성하세요.\n\n"
                    f"전사:\n{text}"
                )

                resp = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant who summarizes meeting transcripts concisely in Korean."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.2,
                    max_tokens=400,
                )

                # 안전하게 summary 추출 — 응답 객체 모양이 다양할 수 있으니 여러 케이스를 시도합니다.
                summary_text = None
                try:
                    # dict-like
                    summary_text = resp['choices'][0]['message'].get('content')
                except Exception:
                    try:
                        # object-like (resp.choices[0].message.content)
                        summary_text = resp.choices[0].message.content
                    except Exception:
                        summary_text = None

                summary = summary_text.strip() if summary_text else None
            else:
                # OpenAI client missing or API key not set — 요약을 생성하지 않습니다.
                if OpenAIClient is None:
                    summary = 'Summary generation skipped: openai package (v1) not available on server.'
                else:
                    summary = 'Summary generation skipped: OPENAI_API_KEY not set on server.'

        except Exception as sum_err:
            # 요약 실패 시에도 전사 텍스트는 반환하도록 함
            summary = f"Summary generation failed: {sum_err}"

        return {"text": text, "summary": summary}

    except Exception as e:
        return {"error": str(e)}
    finally:
        try:
            dest.unlink()
        except Exception:
            pass
