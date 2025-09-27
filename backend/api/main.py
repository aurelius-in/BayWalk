from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from api.routers import projects, generate, plan, policy, evidence
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="BayWalk API")


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return PlainTextResponse(data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(plan.router, tags=["plan"])
app.include_router(generate.router, tags=["generate"])
app.include_router(policy.router, tags=["policy"])
app.include_router(evidence.router, tags=["evidence"])
