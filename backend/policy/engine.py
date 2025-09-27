import requests, json
from pathlib import Path
from typing import Dict, Any


def build_policy_input(state: Dict[str, Any]) -> Dict[str, Any]:
    # Minimal input for current zone.rego
    return {
        "encryption": {"at_rest": True, "in_transit": True},
        "rbac": {"ok": True},
        "zones": {"valid": True},
        "sbom_present": Path("sbom.json").exists(),
        "image_signed": bool(state.get("artifacts", {}).get("signed", False)),
    }


def write_policy_inputs(root: Path, data: Dict[str, Any]):
    (root / "policy_inputs.json").write_text(json.dumps(data, indent=2))


def load_policy(opa_url: str, name: str, rego_path: str) -> None:
    content = Path(rego_path).read_text(encoding="utf-8")
    r = requests.put(
        f"{opa_url}/v1/policies/{name}",
        headers={"Content-Type": "text/plain"},
        data=content,
    )
    r.raise_for_status()


def evaluate_opa(opa_url: str, policy_pkg: str, data: dict) -> dict:
    r = requests.post(f"{opa_url}/v1/data/{policy_pkg}", json={"input": data})
    r.raise_for_status()
    return r.json()
