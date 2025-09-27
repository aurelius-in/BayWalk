from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Planners / Generators
from planners.coverage import compute_coverage
from planners.edge_sizing import size_edge
from planners.power_poe import poe_budget
from planners.routing import cable_routes
from generators.bom import build_bom
from generators.jira import build_jira_epics_stories

# Observability
from opentelemetry import trace
from prometheus_client import Counter, Gauge

tracer = trace.get_tracer("baywalk.orchestrator")
planners_runs_total = Counter("planners_runs_total", "Total planner/agent runs", ["agent"]) 
coverage_pct_gauge = Gauge("coverage_pct_gauge", "Latest computed coverage percent")


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
    with tracer.start_as_current_span("SceneAgent"):
        planners_runs_total.labels(agent="SceneAgent").inc()
        state.setdefault("scene", {})
        _append(state, "SceneAgent: scene loaded")
    return state


def coverage_agent(state: State) -> State:
    with tracer.start_as_current_span("CoverageAgent"):
        planners_runs_total.labels(agent="CoverageAgent").inc()
        scene = state.get("scene", {})
        targets = {"coverage_pct": 0.9}
        coverage = compute_coverage(scene, targets)
        state["coverage"] = coverage
        coverage_pct_gauge.set(float(coverage.get("pct", 0)) * 100.0)
        _append(state, "CoverageAgent: coverage computed")
    return state


def edge_sizing_agent(state: State) -> State:
    with tracer.start_as_current_span("EdgeSizingAgent"):
        planners_runs_total.labels(agent="EdgeSizingAgent").inc()
        placements = state.get("coverage", {}).get("placements", [])
        models = {"detector": {"fps": 8}}
        edge = size_edge(placements, models)
        state["edge_profile"] = edge
        _append(state, "EdgeSizingAgent: edge profile sized")
    return state


def power_agent(state: State) -> State:
    with tracer.start_as_current_span("PowerAgent"):
        planners_runs_total.labels(agent="PowerAgent").inc()
        placements = state.get("coverage", {}).get("placements", [])
        power = poe_budget(placements)
        state["power"] = power
        _append(state, "PowerAgent: PoE budget computed")
    return state


def routing_agent(state: State) -> State:
    with tracer.start_as_current_span("RoutingAgent"):
        planners_runs_total.labels(agent="RoutingAgent").inc()
        scene = state.get("scene", {})
        placements = state.get("coverage", {}).get("placements", [])
        routes = cable_routes(scene, placements)
        state["routes"] = routes
        _append(state, "RoutingAgent: cable routes estimated")
    return state


def bom_agent(state: State) -> State:
    with tracer.start_as_current_span("BOMAgent"):
        planners_runs_total.labels(agent="BOMAgent").inc()
        edge = state.get("edge_profile", {})
        placements = state.get("coverage", {}).get("placements", [])
        bom = build_bom(edge, placements)
        state["bom"] = bom
        _append(state, "BOMAgent: BOM assembled")
    return state


def policy_agent(state: State) -> State:
    with tracer.start_as_current_span("PolicyAgent"):
        planners_runs_total.labels(agent="PolicyAgent").inc()
        state["policies"] = {"allow": True, "checks": ["encryption", "rbac", "zones"]}
        _append(state, "PolicyAgent: policy placeholders prepared")
    return state


def cost_agent(state: State) -> State:
    with tracer.start_as_current_span("CostAgent"):
        planners_runs_total.labels(agent="CostAgent").inc()
        state["costs"] = {"estimated_total_usd": state.get("bom", {}).get("total_usd", 0.0)}
        _append(state, "CostAgent: cost placeholder computed")
    return state


def jira_agent(state: State) -> State:
    with tracer.start_as_current_span("JiraAgent"):
        planners_runs_total.labels(agent="JiraAgent").inc()
        project = {"id": state.get("project_id", "")}
        coverage = state.get("coverage", {})
        edge = state.get("edge_profile", {})
        jira = build_jira_epics_stories(project, coverage, edge)
        state["jira"] = jira
        _append(state, "JiraAgent: epics and stories drafted")
    return state


def artifact_agent(state: State) -> State:
    with tracer.start_as_current_span("ArtifactAgent"):
        planners_runs_total.labels(agent="ArtifactAgent").inc()
        state["artifacts"] = {"kit_ready": False}
        _append(state, "ArtifactAgent: artifact placeholders prepared")
    return state


def compliance_agent(state: State) -> State:
    with tracer.start_as_current_span("ComplianceAgent"):
        planners_runs_total.labels(agent="ComplianceAgent").inc()
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
