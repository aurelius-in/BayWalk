from fastapi import FastAPI
from api.routers import projects, generate, plan
app = FastAPI(title="BayWalk API")
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(plan.router, tags=["plan"])
app.include_router(generate.router, tags=["generate"])
