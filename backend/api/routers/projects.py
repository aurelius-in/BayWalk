from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Project

router = APIRouter()


class ProjectIn(BaseModel):
    name: str
    targets: dict
    scene_ref: str


@router.post("")
def create_project(p: ProjectIn, db: Session = Depends(get_db)):
    pid = str(uuid4())
    proj = Project(id=pid, name=p.name, targets=p.targets, scene_ref=p.scene_ref, status="created")
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return {
        "id": proj.id,
        "name": proj.name,
        "targets": proj.targets,
        "scene_ref": proj.scene_ref,
        "status": proj.status,
    }


@router.get("/{pid}")
def get_project(pid: str, db: Session = Depends(get_db)):
    proj = db.get(Project, pid)
    if not proj:
        raise HTTPException(status_code=404, detail="project not found")
    return {
        "id": proj.id,
        "name": proj.name,
        "targets": proj.targets,
        "scene_ref": proj.scene_ref,
        "status": proj.status,
    }


class SceneUpload(BaseModel):
    scene: dict
    name: str = "Unnamed"
    targets: dict = {}


@router.post("/upload")
def upload_scene(payload: SceneUpload, db: Session = Depends(get_db)):
    pid = str(uuid4())
    import json
    from pathlib import Path

    samples = Path("samples")
    samples.mkdir(exist_ok=True)
    scene_path = samples / f"{pid}.scene.json"
    scene_path.write_text(json.dumps(payload.scene, indent=2))

    proj = Project(
        id=pid,
        name=payload.name,
        targets=payload.targets,
        scene_ref=str(scene_path),
        status="created",
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return {
        "id": proj.id,
        "name": proj.name,
        "targets": proj.targets,
        "scene_ref": proj.scene_ref,
        "status": proj.status,
    }
