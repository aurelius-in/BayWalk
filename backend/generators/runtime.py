from pathlib import Path
from typing import Dict, Any


def write_runtime_configs(root: Path, edge: Dict[str, Any]):
    rt = root / "runtime"
    ort = rt / "onnxruntime"
    triton = rt / "triton"
    ort.mkdir(parents=True, exist_ok=True)
    triton.mkdir(parents=True, exist_ok=True)

    # ONNX Runtime session options
    (ort / "session.json").write_text(
        '{"intra_op_num_threads": 1, "graph_optimization_level": "ORT_ENABLE_ALL"}\n'
    )

    # Triton minimal config
    (triton / "config.pbtxt").write_text(
        'name: "detector"\nplatform: "onnxruntime_onnx"\nmax_batch_size: 1\n'
    )
