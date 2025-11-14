from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, subprocess, hashlib, re, datetime
from db import init_db, save_deployment, update_deployment_status, get_deployments
from agents.design_agent import create_layout
from agents.frontend_agent import generate_frontend, set_frontend
from agents.backend_agent import generate_backend, save_backend
from agents.qa_agent import qa_test
from agents.gpt_verification_agent import gpt_verify_and_fix
from notify import send_slack, send_discord
import time

init_db()
app = FastAPI(title="Real-time Deployment Manager")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class DeployRequest(BaseModel):
    user_request: str
    parent_issue_number: int = None # 원본 Issue 연결

@app.post("/api/deploy")
def deploy(req: DeployRequest, parent_issue_number=None, max_retry=2):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    project_name = f"site-{hashlib.md5(req.user_request.encode()).hexdigest()[:6]}-{timestamp}"
    project_dir = os.path.join("deployments", project_name)
    os.makedirs(project_dir, exist_ok=True)

    # --- Design Stage ---
    design_html = create_layout(req.user_request)
    design_fixed, issues, msg = gpt_verify_and_fix(design_html, "Design")
    layout_html = design_fixed

    # --- Frontend Stage ---
    frontend_html = generate_frontend(layout_html)
    frontend_fixed, issues, msg = gpt_verify_and_fix(frontend_html, "Frontend")
    set_frontend(frontend_fixed)

    # --- Backend Stage ---
    backend_code = generate_backend(frontend_fixed)
    backend_fixed, issues, msg = gpt_verify_and_fix(backend_code, "Backend")
    save_backend(backend_fixed)

    # --- QA ---
    qa_result = qa_test(frontend_fixed)

    # --- Deployment ---
    with open(os.path.join(project_dir, "main.py"), "w") as f:
        f.write(backend_fixed)
    with open(os.path.join(project_dir, "vercel.json"), "w") as f:
        f.write('{"version":3,"builds":[{"src":"main.py","use":"@vercel/python"}]}')

    vercel_token = os.getenv("VERCEL_TOKEN")
    result = subprocess.run(["vercel", "--prod", "--confirm", "--token", vercel_token],
                            cwd=project_dir, capture_output=True, text=True)
    url_match = re.search(r"https://[^\s]+\.vercel\.app", result.stdout + result.stderr)
    deployment_url = url_match.group(0) if url_match else None

    if deployment_url:
        save_deployment(project_name, deployment_url, qa_result, status="success")
        return {"url": deployment_url, "qa": qa_result}
    else:
        return {"error": "Deployment failed"}

@app.get("/api/deployments")
def list_deployments():
    return get_deployments()
