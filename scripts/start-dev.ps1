<#
start-dev.ps1

개요:
- 이 스크립트는 개발 편의를 위해 백엔드(uvicorn)와 프론트엔드(Vite)를
  각각 새 PowerShell 창으로 동시에 실행합니다.
- 저장소 루트에서 실행하세요: `./scripts/start-dev.ps1`

동작:
- backend: `uvicorn app.main:app --reload --port 8000` (작업 디렉터리: `backend`)
- frontend: `npm run dev` (작업 디렉터리: `frontend`)

참고:
- 이 스크립트는 Windows PowerShell(v5.1) 환경을 가정합니다.
- 필요 시 의존성 설치(`pip install -r requirements.txt`, `npm install`)를 먼저 수행하세요.
#>

Set-StrictMode -Version Latest

function Test-CommandAvailable {
    param([string]$cmd)
    return (Get-Command $cmd -ErrorAction SilentlyContinue) -ne $null
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

Write-Host "Repository root: $root" -ForegroundColor Cyan

if (-not (Test-CommandAvailable -cmd python)) {
    Write-Warning "'python'를 찾을 수 없습니다. Python이 설치되어 있고 PATH에 포함되어 있는지 확인하세요."
}
if (-not (Test-CommandAvailable -cmd npm)) {
    Write-Warning "'npm'을 찾을 수 없습니다. Node.js/NPM이 설치되어 있는지 확인하세요."
}

Write-Host "-- 개발 서버를 실행합니다 --" -ForegroundColor Green

# Backend: run in new PowerShell window
$backendCmd = "cd `"$root\backend`"; uvicorn app.main:app --reload --port 8000"
Start-Process -FilePath powershell -ArgumentList "-NoExit", "-Command", $backendCmd
Write-Host "Started backend in new window: uvicorn app.main:app --reload --port 8000"

# Frontend: run in new PowerShell window
$frontendCmd = "cd `"$root\frontend`"; npm run dev"
Start-Process -FilePath powershell -ArgumentList "-NoExit", "-Command", $frontendCmd
Write-Host "Started frontend in new window: npm run dev"

Write-Host "Dev servers started. Check the new windows for logs." -ForegroundColor Cyan

Write-Host "If ports are already in use, stop the conflicting processes or change ports in the commands." -ForegroundColor Yellow
