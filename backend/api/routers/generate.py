from fastapi import APIRouter
from pathlib import Path
from orchestrator.graph import build_graph, State
from generators.iac import write_infra
from generators.integration import write_integrations
from generators.jira import build_jira_epics_stories, write_jira_bundle
from generators.compliance import write_compliance_bundle
from generators.costs import write_cost_summary

router = APIRouter()


@router.post("/projects/{pid}/generate")
def generate_artifacts(pid: str):
    graph = build_graph()
    state: State = {"project_id": pid, "messages": []}
    result: State = graph.invoke(state)

    kit_root = Path("delivery-kit") / pid
    placements = result.get("coverage", {}).get("placements", [])

    # Infra
    write_infra(kit_root, result)

    # Integrations
    write_integrations(kit_root, placements)

    # Jira
    jira_bundle = build_jira_epics_stories({"id": pid}, result.get("coverage", {}), result.get("edge_profile", {}))
    write_jira_bundle(kit_root, jira_bundle)

    # Compliance
    write_compliance_bundle(kit_root, {"id": pid}, result, result.get("policies", {}))

    # Costs
    write_cost_summary(kit_root, result.get("bom", {}))

    return {
        "project_id": pid,
        "status": "generation_started",
        "kit_path": str(kit_root),
        "messages": result.get("messages", []),
    }
