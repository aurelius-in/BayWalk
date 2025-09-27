from pathlib import Path
from typing import Dict, Any, List
import subprocess


def _md_table(headers: List[str], rows: List[List[str]]) -> str:
    sep = ["---" for _ in headers]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(sep) + " |"]
    for r in rows:
        lines.append("| " + " | ".join(map(str, r)) + " |")
    return "\n".join(lines)


def write_cost_summary(root: Path, bom: Dict[str, Any]):
    costs_dir = root / "costs"
    costs_dir.mkdir(parents=True, exist_ok=True)

    items = bom.get("items", [])
    rows = [[i.get("sku"), i.get("qty"), f"${i.get('unit_usd')}", f"${i.get('qty') * i.get('unit_usd')}"] for i in items]
    table = _md_table(["SKU", "Qty", "Unit", "Line Total"], rows)

    total = bom.get("total_usd", 0.0)
    plus = round(total * 1.1, 2)
    minus = round(total * 0.9, 2)

    md = f"""
# Cost Summary

Total: ${total}

## Items

{table}

## Sensitivity (+/- 10%)

- Low: ${minus}
- High: ${plus}
""".lstrip()
    (costs_dir / "summary.md").write_text(md)

    # Try to run infracost if present
    try:
        tf_path = root / "infra" / "terraform"
        out = subprocess.run(
            ["infracost", "breakdown", "--path", str(tf_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        (costs_dir / "cloud.txt").write_text(out.stdout or out.stderr)
    except Exception as e:
        (costs_dir / "cloud.txt").write_text(f"infracost not run: {e}")
