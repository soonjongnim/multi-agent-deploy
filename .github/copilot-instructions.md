## 목적

이 문서는 AI 코딩 에이전트가 이 저장소에서 바로 생산적으로 작업할 수 있도록 최소한의 실행 가능한 컨텍스트를 제공합니다.
아키텍처, 실행/빌드 워크플로우, 파일 규약, 코드베이스에서 발견되는 구체적인 예시를 중심으로 요약합니다.

## 아키텍처 — 전체 개요
- **백엔드 (Python / FastAPI)**: `backend/app`에는 프로젝트에서 사용하는 FastAPI 관련 코드가 모여 있습니다.
  - `app/main.py` — 주 백엔드 앱입니다. `app/generator` 폴더를 `/generated` 경로로 정적 마운트하고, `app/generator/server.py`를 서브프로세스로 자동 실행합니다.
  - `app/manage.py` — 디자인 → 프론트엔드 → 백엔드 → QA → Vercel 배포의 멀티스테이지 파이프라인을 실행하는 배포 관리 엔드포인트입니다.
- **Generator 서버**: `backend/app/generator/server.py`는 `app/generator/api.py`를 없으면 생성하고, 별도 Uvicorn 서버를 포트 `9000`에서 실행합니다. 생성된 백엔드 코드는 `app/generator`에 기록됩니다.
- **Agents**: `backend/app/agents/*`는 소형 모듈들(예: `design_agent`, `frontend_agent`, `backend_agent`, `qa_agent`, `gpt_verification_agent`)로 구성되어 있으며, 공통 LLM 클라이언트 `agents/llm_client.py`를 사용하고 코드나 아티팩트를 문자열로 반환합니다.
- **DB 및 영속성**: `backend/app/db.py`는 로컬 SQLite 데이터베이스 `deployments.db`를 사용하며 `init_db`, `save_deployment`, `get_deployments` 같은 헬퍼를 제공합니다.
- **프론트엔드**: `frontend/`는 Vite + React 앱입니다. 프론트엔드는 백엔드 엔드포인트를 호출합니다(예: `frontend/src/api/backend.js`).

## 핵심 통합 지점 (먼저 확인할 것)
- LLM 설정: `backend/app/agents/llm_client.py` — 환경변수 `OPENAI_API_KEY`를 필요로 하며 `langchain_openai.ChatOpenAI`로 `llm` 객체를 생성합니다.
- Generator: `backend/app/generator/server.py` — `app/generator/api.py`를 생성하고 포트 `9000`에서 리로드 모드로 실행합니다. `main.py`가 이 프로세스를 자동으로 시작합니다.
- 배포 흐름: `backend/app/manage.py`는 파이프라인을 조율하고 `vercel` CLI와 `VERCEL_TOKEN` 환경변수를 사용하여 생성된 프로젝트를 배포합니다.
- 정적 서빙: `app/main.py`는 `app/generator`를 `/generated`로 마운트하여 생성된 정적 출력을 제공합니다.

## 명령 및 실행 예제 (정확한 예)
PowerShell(리포지토리 루트 기준):

백엔드 의존성 설치:
```
cd backend; pip install -r requirements.txt
```

백엔드 시작 (Generator도 자동 실행됨):
```
cd backend
uvicorn app.main:app --reload --port 8000
```

설명: `app.main`을 시작하면 `app/generator/server.py`가 서브프로세스로 실행되어 포트 `9000`에서 Uvicorn을 띄우고, `app/generator/api.py`가 없으면 생성합니다.

프론트엔드 실행 (Vite):
```
cd frontend
npm install
npm run dev
```
프론트엔드가 백엔드를 호출하려면 `VITE_API_URL`(예: `http://localhost:8000`)을 설정하세요.

필요한 환경변수:
- `OPENAI_API_KEY` — `agents/llm_client.py`에서 필요합니다.
- `VERCEL_TOKEN` — `manage.py`가 `vercel --prod` 호출에 사용합니다.
- `VITE_API_URL` — 프론트엔드가 백엔드 주소로 사용합니다.

## 프로젝트 특화 규약 및 패턴
- 에이전트들은 원시 코드나 HTML 문자열을 반환합니다 — 예: `design_agent.create_layout(user_request)`는 HTML 문자열을 반환하고, `frontend_agent.generate_frontend(html)`는 완전한 프론트엔드 코드를 문자열로 반환합니다.
- 검증 단계: `gpt_verification_agent.gpt_verify_and_fix(...)`는 디자인/프론트엔드/백엔드 각 단계 이후에 호출되어 출력을 반복적으로 수정합니다.
- 생성 파일 저장: 생성 로직은 `app/generator`에 파일을 기록합니다(`utils/file_saver.py` 및 `generator/server.py` 참조). 또한 `manage.py`는 `deployments/<project_name>` 폴더에 배포 산출물을 씁니다.
- 함수 이름 불일치 주의: 일부 위치에서는 같은 동작을 가리키는데 다른 이름을 사용합니다(예: `manage.py`는 `generate_backend`를 호출하고 라우트 코드에서는 `create_backend_api`를 참조). 교차 변경을 할 때는 해당 에이전트 모듈의 실제 함수를 확인하세요.

## 변경 시 확인할 주요 파일
- `backend/app/main.py` — 마운트, generator 서브프로세스 동작, CORS 설정.
- `backend/app/manage.py` — 배포 파이프라인 및 Vercel 연동.
- `backend/app/generator/server.py` — generator 서버 수명주기와 `app/generator/api.py`의 위치.
- `backend/app/agents/llm_client.py` — LLM 초기화(모델, 온도, API 키 확인).
- `backend/app/agents/*.py` — 생성 로직을 변경해야 할 때 확인.
- `backend/app/db.py` — 배포 기록 관련 간단한 SQLite 헬퍼.
- `frontend/src/api/backend.js` — 프론트엔드→백엔드 호출 예시와 기대 JSON 형태(`/generate`, `/deploy`).

## 디버깅 팁 (구체적)
- 생성된 API 엔드포인트가 보이지 않으면 `app/generator/api.py`를 확인하세요 — `server.py`가 기본 템플릿을 자동 생성합니다.
- Generator가 실행되지 않으면 `uvicorn app.main:app`으로 백엔드를 실행하거나 `python app/generator/server.py`를 직접 실행해 9000 포트 로그를 확인하세요.
- LLM 오류: `OPENAI_API_KEY`가 설정되어 있는지 확인하세요. 설치된 `langchain_openai` 패키지의 API가 코드가 기대하는 형태(`llm.invoke(prompt)`이 `.content`를 가진 객체 반환)를 따르는지도 확인해야 합니다.
- Vercel 배포: `manage.py`가 `subprocess.run([... 'vercel' ...])`을 사용하므로, 로컬에 `vercel` CLI가 설치되어 있고 `VERCEL_TOKEN`이 환경변수로 설정되어야 합니다.

## AI 에이전트가 먼저 할 일
1. `backend/app/agents/llm_client.py`를 열어 LLM 설정과 필요한 환경변수를 확인합니다.
2. `backend/app/main.py`와 `backend/app/generator/server.py`를 읽어 generator의 수명주기와 출력 위치를 이해합니다.
3. 호출하거나 수정할 `backend/app/agents/*` 함수들의 실제 이름과 반환 타입을 확인합니다.
4. 로컬에서 백엔드(`uvicorn app.main:app`)를 실행하고 포트 `9000`의 generator 로그를 확인하여 엔드투엔드 동작을 검증합니다.

## 생성물 형식을 변경할 때
- 생성물 형식을 바꾸면 `utils/file_saver.py`와 `app/generator`를 함께 업데이트하세요 — 생성된 내용은 디스크에 직접 기록되고 배포됩니다.

## 유지보수자에게 물어볼 것
- 코드의 일부가 `create_backend_api`와 `generate_backend` 같은 서로 다른 함수명을 참조합니다. 어떤 이름을 표준으로 사용할지 확인해 주세요.

---
원하시면 이 변경을 포함한 PR을 열고 루트 README에 실행 예시(파워셸 명령)와 시작 시 필수 환경변수를 검사하는 작은 스크립트(`scripts/check_env.py` 또는 PowerShell)를 추가해 드릴 수 있습니다. 어떤 작업을 먼저 해드릴까요?
