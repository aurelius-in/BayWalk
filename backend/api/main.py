from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routers import projects, generate, plan, policy, evidence
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from db.session import init_db
from api.auth import require_api_key

app = FastAPI(title="BayWalk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _on_startup():
    init_db()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return PlainTextResponse(data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


app.include_router(projects.router, prefix="/projects", tags=["projects"], dependencies=[Depends(require_api_key)])
app.include_router(plan.router, tags=["plan"], dependencies=[Depends(require_api_key)])
app.include_router(generate.router, tags=["generate"], dependencies=[Depends(require_api_key)])
app.include_router(policy.router, tags=["policy"], dependencies=[Depends(require_api_key)])
app.include_router(evidence.router, tags=["evidence"], dependencies=[Depends(require_api_key)])
