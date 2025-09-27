from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4
import json
from pathlib import Path
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


class SceneUpload(BaseModel):
    scene: dict
    name: str = "Unnamed"
    targets: dict = {}


@router.post("/upload")
def upload_scene(payload: SceneUpload):
    pid = str(uuid4())
    samples = Path("samples")
    samples.mkdir(exist_ok=True)
    scene_path = samples / f"{pid}.scene.json"
    scene_path.write_text(json.dumps(payload.scene, indent=2))
    DB[pid] = {
        "id": pid,
        "name": payload.name,
        "targets": payload.targets,
        "scene_ref": str(scene_path),
        "status": "created",
    }
    return DB[pid]
