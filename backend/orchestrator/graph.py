from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict, total=False):
    project_id: str
    scene: dict
    coverage: dict
    edge_profile: dict
    power: dict
    routes: dict
    bom: dict
    policies: dict
    costs: dict
    jira: dict
    artifacts: dict
    evidence: dict
    messages: list

def _pass(s): return s

def build_graph():
    g = StateGraph(State)
    # Add nodes placeholders
    for n in ["SceneAgent","CoverageAgent","EdgeSizingAgent","PowerAgent","RoutingAgent","BOMAgent","PolicyAgent","CostAgent","JiraAgent","ArtifactAgent","ComplianceAgent"]:
        g.add_node(n, _pass)
    # Simple linear flow for MVP
    flow = ["SceneAgent","CoverageAgent","EdgeSizingAgent","PowerAgent","RoutingAgent","BOMAgent","PolicyAgent","CostAgent","JiraAgent","ArtifactAgent","ComplianceAgent"]
    for i in range(len(flow)-1):
        g.add_edge(flow[i], flow[i+1])
    g.add_edge(flow[-1], END)
    g.set_entry_point(flow[0])
    return g.compile()

ORCHESTRATION NOTES
- Each Agent node will:
  - Read and write fields on State
  - Use tools in planners/* and generators/*
  - Append a short message to State.messages
