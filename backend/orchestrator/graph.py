from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Planners / Generators
from planners.coverage import compute_coverage
from planners.edge_sizing import size_edge
from planners.power_poe import poe_budget
from planners.routing import cable_routes
from generators.bom import build_bom
from generators.jira import build_jira_epics_stories


class State(TypedDict, total=False):
    project_id: str
    scene: Dict[str, Any]
    coverage: Dict[str, Any]
    edge_profile: Dict[str, Any]
    power: Dict[str, Any]
    routes: Dict[str, Any]
    bom: Dict[str, Any]
    policies: Dict[str, Any]
    costs: Dict[str, Any]
    jira: Dict[str, Any]
    artifacts: Dict[str, Any]
    evidence: Dict[str, Any]
    messages: List[str]


def _ensure_messages(state: State) -> None:
    if "messages" not in state or state.get("messages") is None:
        state["messages"] = []


def _append(state: State, msg: str) -> None:
    _ensure_messages(state)
    state["messages"].append(msg)


# Agents

def scene_agent(state: State) -> State:
    # For MVP, leave scene as-is if present, else use empty dict placeholder
    state.setdefault("scene", {})
    _append(state, "SceneAgent: scene loaded")
    return state


def coverage_agent(state: State) -> State:
    scene = state.get("scene", {})
    # Targets placeholder for MVP
    targets = {"coverage_pct": 0.9}
    coverage = compute_coverage(scene, targets)
    state["coverage"] = coverage
    _append(state, "CoverageAgent: coverage computed")
    return state


def edge_sizing_agent(state: State) -> State:
    placements = state.get("coverage", {}).get("placements", [])
    # Models placeholder
    models = {"detector": {"fps": 8}}
    edge = size_edge(placements, models)
    state["edge_profile"] = edge
    _append(state, "EdgeSizingAgent: edge profile sized")
    return state


def power_agent(state: State) -> State:
    placements = state.get("coverage", {}).get("placements", [])
    power = poe_budget(placements)
    state["power"] = power
    _append(state, "PowerAgent: PoE budget computed")
    return state


def routing_agent(state: State) -> State:
    scene = state.get("scene", {})
    placements = state.get("coverage", {}).get("placements", [])
    routes = cable_routes(scene, placements)
    state["routes"] = routes
    _append(state, "RoutingAgent: cable routes estimated")
    return state


def bom_agent(state: State) -> State:
    edge = state.get("edge_profile", {})
    placements = state.get("coverage", {}).get("placements", [])
    bom = build_bom(edge, placements)
    state["bom"] = bom
    _append(state, "BOMAgent: BOM assembled")
    return state


def policy_agent(state: State) -> State:
    # Placeholder policy evaluation result; real evaluation in later phase
    state["policies"] = {"allow": True, "checks": ["encryption", "rbac", "zones"]}
    _append(state, "PolicyAgent: policy placeholders prepared")
    return state


def cost_agent(state: State) -> State:
    # Placeholder cost rollup; real rollups in later phase
    state["costs"] = {"estimated_total_usd": state.get("bom", {}).get("total_usd", 0.0)}
    _append(state, "CostAgent: cost placeholder computed")
    return state


def jira_agent(state: State) -> State:
    project = {"id": state.get("project_id", "")}
    coverage = state.get("coverage", {})
    edge = state.get("edge_profile", {})
    jira = build_jira_epics_stories(project, coverage, edge)
    state["jira"] = jira
    _append(state, "JiraAgent: epics and stories drafted")
    return state


def artifact_agent(state: State) -> State:
    # Placeholder metadata for artifacts; writing happens in later phase
    state["artifacts"] = {"kit_ready": False}
    _append(state, "ArtifactAgent: artifact placeholders prepared")
    return state


def compliance_agent(state: State) -> State:
    # Placeholder compliance fields
    state["evidence"] = {"bundle_ready": False}
    _append(state, "ComplianceAgent: compliance placeholders prepared")
    return state


def build_graph():
    g = StateGraph(State)

    # Add nodes
    g.add_node("SceneAgent", scene_agent)
    g.add_node("CoverageAgent", coverage_agent)
    g.add_node("EdgeSizingAgent", edge_sizing_agent)
    g.add_node("PowerAgent", power_agent)
    g.add_node("RoutingAgent", routing_agent)
    g.add_node("BOMAgent", bom_agent)
    g.add_node("PolicyAgent", policy_agent)
    g.add_node("CostAgent", cost_agent)
    g.add_node("JiraAgent", jira_agent)
    g.add_node("ArtifactAgent", artifact_agent)
    g.add_node("ComplianceAgent", compliance_agent)

    # Linear MVP flow
    flow = [
        "SceneAgent",
        "CoverageAgent",
        "EdgeSizingAgent",
        "PowerAgent",
        "RoutingAgent",
        "BOMAgent",
        "PolicyAgent",
        "CostAgent",
        "JiraAgent",
        "ArtifactAgent",
        "ComplianceAgent",
    ]
    for i in range(len(flow) - 1):
        g.add_edge(flow[i], flow[i + 1])
    g.add_edge(flow[-1], END)
    g.set_entry_point(flow[0])

    return g.compile()
