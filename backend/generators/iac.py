from pathlib import Path
import json, yaml
def write_infra(root: Path, plan: dict):
    tf = root / "infra" / "terraform"
    helm = root / "infra" / "helm"
    tf.mkdir(parents=True, exist_ok=True)
    helm.mkdir(parents=True, exist_ok=True)
    (tf/"main.tf").write_text('// terraform scaffold\n')
    (helm/"values.yaml").write_text('# helm values scaffold\n')
