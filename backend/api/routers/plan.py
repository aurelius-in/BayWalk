from fastapi import APIRouter
from orchestrator.graph import build_graph, State
from api.schemas import PlanResponse

router = APIRouter()


@router.post("/projects/{pid}/plan", response_model=PlanResponse)
def run_planners(pid: str):
    graph = build_graph()
    state: State = {"project_id": pid, "messages": []}
    result: State = graph.invoke(state)
    return {
        "project_id": pid,
        "coverage": result.get("coverage", {}),
        "edge_profile": result.get("edge_profile", {}),
        "power": result.get("power", {}),
        "routes": result.get("routes", {}),
        "bom": result.get("bom", {}),
        "policies": result.get("policies", {}),
        "costs": result.get("costs", {}),
        "messages": result.get("messages", []),
    }
