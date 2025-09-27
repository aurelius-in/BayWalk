from fastapi import FastAPI
from api.routers import projects, generate, plan, policy, evidence
app = FastAPI(title="BayWalk API")
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(plan.router, tags=["plan"])
app.include_router(generate.router, tags=["generate"])
app.include_router(policy.router, tags=["policy"])
app.include_router(evidence.router, tags=["evidence"])
