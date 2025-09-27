from fastapi import APIRouter
import os
from pathlib import Path
from orchestrator.graph import build_graph, State
from evidence.signer import assemble_and_sign
from api.schemas import EvidenceResponse

router = APIRouter()


@router.post("/projects/{pid}/evidence", response_model=EvidenceResponse)
def build_evidence(pid: str):
    graph = build_graph()
    state: State = {"project_id": pid, "messages": []}
    result: State = graph.invoke(state)

    kit_root = Path("delivery-kit") / pid
    key_path = os.getenv("COSIGN_KEY_PATH", "./ci/keys/cosign.key")
    manifest = assemble_and_sign(kit_root, pid, key_path)
    return {"project_id": pid, "evidence": manifest}
