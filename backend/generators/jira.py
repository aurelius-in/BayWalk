from pathlib import Path
from typing import Dict, Any
import json


DOR = "Backlog item defined, dependencies known, acceptance criteria listed"
DOD = "Code merged, tests passing, docs updated, demo recorded"


def build_jira_epics_stories(project: Dict[str, Any], coverage: Dict[str, Any], edge: Dict[str, Any]) -> Dict[str, Any]:
    # Produce JSON for Jira import. DoR/DoD, AC, risks
    return {
        "epics": [
            {"key": "BAY-1", "summary": "BayWalk Pilot", "dor": DOR, "dod": DOD},
        ],
        "stories": [
            {"summary": "Place cameras", "acceptance": ["All lanes visible", "No blind spots"]},
        ],
    }


def write_jira_bundle(root: Path, bundle: Dict[str, Any]):
    jira_dir = root / "jira"
    jira_dir.mkdir(parents=True, exist_ok=True)
    (jira_dir / "epics.json").write_text(json.dumps(bundle.get("epics", []), indent=2))
    (jira_dir / "stories.json").write_text(json.dumps(bundle.get("stories", []), indent=2))
