from pathlib import Path
from typing import Dict, Any
from jinja2 import Template


IQ_TPL = Template("""
# Installation Qualification (IQ)

Project: {{ project.id }}
Edge: {{ plan.edge_profile.type }}
Switch: {{ plan.power.switch }}

Artifacts: {{ artifacts|length }} items
""")

OQ_TPL = Template("""
# Operational Qualification (OQ)

Coverage: {{ plan.coverage.pct * 100 }}%
Routes total length: {{ plan.routes.total_length_m }} m
""")

PQ_TPL = Template("""
# Performance Qualification (PQ)

BOM total: ${{ plan.bom.total_usd }}
Policies allow: {{ plan.policies.allow }}
""")

TRACE_TPL = Template("""
# Traceability

Messages:
{% for m in messages %}- {{ m }}
{% endfor %}
""")


def write_compliance_bundle(root: Path, project: Dict[str, Any], plan: Dict[str, Any], policies: Dict[str, Any]):
    comp = root / "compliance"
    comp.mkdir(parents=True, exist_ok=True)

    context = {
        "project": {"id": project.get("id")},
        "plan": plan,
        "policies": policies,
        "artifacts": plan.get("artifacts", {}),
        "messages": plan.get("messages", []),
    }

    (comp / "IQ.md").write_text(IQ_TPL.render(**context))
    (comp / "OQ.md").write_text(OQ_TPL.render(**context))
    (comp / "PQ.md").write_text(PQ_TPL.render(**context))
    (comp / "Traceability.md").write_text(TRACE_TPL.render(**context))
