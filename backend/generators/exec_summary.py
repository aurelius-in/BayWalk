from pathlib import Path
from typing import Dict, Any


def write_exec_summary(root: Path, plan: Dict[str, Any]):
    summary = root / "OnePager.md"
    coverage = plan.get("coverage", {}).get("pct", 0)
    edge = plan.get("edge_profile", {}).get("type", "n/a")
    total_cost = plan.get("bom", {}).get("total_usd", 0.0)
    routes = plan.get("routes", {}).get("total_length_m", 0.0)

    md = f"""
# BayWalk Exec Summary

- Coverage: {coverage*100:.1f}%
- Edge: {edge}
- Estimated CapEx: ${total_cost:,.2f}
- Cable Length: {routes:.1f} m

Artifacts are available under this kit folder.
""".lstrip()
    summary.write_text(md)
