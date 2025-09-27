from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4
router = APIRouter()
DB = {}

class ProjectIn(BaseModel):
    name: str
    targets: dict
    scene_ref: str

@router.post("")
def create_project(p: ProjectIn):
    pid = str(uuid4())
    DB[pid] = {"id": pid, **p.model_dump(), "status": "created"}
    return DB[pid]

@router.get("/{pid}")
def get_project(pid: str):
    return DB.get(pid, {})
