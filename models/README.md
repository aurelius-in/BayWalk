# Models Packaging Guide

## Export to ONNX
- Use dynamic axes for batch dims when possible.
- Example (PyTorch):

```python
torch.onnx.export(model, dummy, "detector.onnx", opset_version=17,
                  input_names=["input"], output_names=["boxes","scores"],
                  dynamic_axes={"input": {0: "batch"}, "boxes": {0: "batch"}, "scores": {0: "batch"}})
```

## Triton Model Repository Layout
```
runtime/triton/
  detector/
    1/
      model.onnx
    config.pbtxt
```

Minimal `config.pbtxt`:
```
name: "detector"
platform: "onnxruntime_onnx"
max_batch_size: 1
input [ { name: "input" data_type: TYPE_FP32 dims: [ 3, 640, 640 ] } ]
output [ { name: "boxes" data_type: TYPE_FP32 dims: [ -1, 4 ] }, { name: "scores" data_type: TYPE_FP32 dims: [ -1 ] } ]
```

## ORT Runtime
- Adjust `runtime/onnxruntime/session.json` if needed:
```
{"intra_op_num_threads": 1, "graph_optimization_level": "ORT_ENABLE_ALL"}
```

## Tips
- Validate with `onnx.checker.check_model` and `onnxruntime.InferenceSession`.
- Keep models <100MB for mobile-friendly deployments.
