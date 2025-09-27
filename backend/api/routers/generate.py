from fastapi import APIRouter
from orchestrator.graph import build_graph, State

router = APIRouter()


@router.post("/projects/{pid}/generate")
def generate_artifacts(pid: str):
    graph = build_graph()
    state: State = {"project_id": pid, "messages": []}
    result: State = graph.invoke(state)
    return {
        "project_id": pid,
        "status": "generation_started",
        "messages": result.get("messages", []),
    }
