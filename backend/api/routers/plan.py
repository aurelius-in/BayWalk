from fastapi import APIRouter
router = APIRouter()

@router.post("/projects/{pid}/plan")
def run_planners(pid: str):
    # stub, will call orchestrator later
    return {"project_id": pid, "status": "planning_started"}
