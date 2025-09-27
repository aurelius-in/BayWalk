from pathlib import Path
from typing import Dict, Any
import textwrap


TF_MAIN = textwrap.dedent(
    """
    terraform {
      required_version = ">= 1.5.0"
      required_providers {
        kubernetes = {
          source  = "hashicorp/kubernetes"
          version = ">= 2.23.0"
        }
      }
    }

    provider "kubernetes" {}
    """
).lstrip()

HELM_VALUES = textwrap.dedent(
    """
    namespace: baywalk
    storage:
      pvcSize: 10Gi
      logsPvcSize: 5Gi
    imagePullPolicy: IfNotPresent
    """
).lstrip()


def write_infra(root: Path, plan: Dict[str, Any]):
    tf = root / "infra" / "terraform"
    helm = root / "infra" / "helm"
    tf.mkdir(parents=True, exist_ok=True)
    helm.mkdir(parents=True, exist_ok=True)
    (tf / "main.tf").write_text(TF_MAIN)
    (helm / "values.yaml").write_text(HELM_VALUES)
