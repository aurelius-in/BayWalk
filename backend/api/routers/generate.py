from fastapi import APIRouter
router = APIRouter()

@router.post("/projects/{pid}/generate")
def generate_artifacts(pid: str):
    # stub, will call generators later
    return {"project_id": pid, "status": "generation_started"}
