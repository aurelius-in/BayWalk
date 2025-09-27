from fastapi import APIRouter
from pathlib import Path
import os
from orchestrator.graph import build_graph, State
from policy.engine import build_policy_input, write_policy_inputs, evaluate_opa
from api.schemas import PolicyResponse

router = APIRouter()


@router.post("/projects/{pid}/policy", response_model=PolicyResponse)
def run_policy(pid: str):
    graph = build_graph()
    state: State = {"project_id": pid, "messages": []}
    result: State = graph.invoke(state)

    inputs = build_policy_input(result)
    kit_root = Path("delivery-kit") / pid
    kit_root.mkdir(parents=True, exist_ok=True)
    write_policy_inputs(kit_root, inputs)

    opa_url = os.getenv("OPA_URL", "http://localhost:8181")
    resp = evaluate_opa(opa_url, "baywalk/network/allow", inputs)
    allow = resp.get("result", False)

    rationale = [
        "encryption at rest required",
        "encryption in transit required",
        "RBAC enabled",
        "zones validated",
        "SBOM present",
        "container images signed",
    ]
    return {"project_id": pid, "allow": bool(allow), "rationale": rationale}
