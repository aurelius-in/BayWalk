# Runtime Containers

## Triton
- Requires NVIDIA GPU and drivers.
- Build (optional) or run server mounting the generated model repo:
```
docker run --gpus all --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v $(pwd)/delivery-kit/<pid>/runtime/triton:/models \
  nvcr.io/nvidia/tritonserver:24.08-py3 tritonserver --model-repository=/models
```

## ONNX Runtime (placeholder)
- The kit writes `runtime/onnxruntime/session.json`.
- Customize a small FastAPI server to serve the model, or integrate into edge app.
