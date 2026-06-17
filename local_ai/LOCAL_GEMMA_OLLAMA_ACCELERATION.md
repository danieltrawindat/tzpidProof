# Local Gemma Acceleration Record

Generated: 2026-06-11

## Installed Local Model

- Runtime: Ollama `0.30.6`
- Model: `gemma3:1b`
- Smoke test: passed, model replied `OK`
- Runtime residency from `ollama ps`: `100% GPU`

## Detected Hardware

- GPU: NVIDIA GeForce RTX 4060 Laptop GPU
- iGPU: AMD Radeon(TM) 860M Graphics
- NPU: AMD `NPU Compute Accelerator Device`

## Current Status

Gemma is installed and running locally through Ollama. Ollama reports the loaded `gemma3:1b` model as `100% GPU`, so the current working path is GPU accelerated.

The AMD NPU is visible to Windows, but standard Ollama on Windows does not currently expose a reliable AMD Ryzen AI NPU backend for Gemma in the same way it reports CPU/GPU residency. For a true NPU-backed Gemma lane, use a separate Ryzen AI / ONNX Runtime GenAI / DirectML or VitisAI workflow with an NPU-ready ONNX model.

## Recheck Command

Run:

```powershell
D:\TZPIDProof\local_ai\check_local_gemma_acceleration.ps1
```

Expected key line:

```text
gemma3:1b ... PROCESSOR 100% GPU
```

## NPU Lane

The NPU path should be treated as a separate certificate lane:

1. Select an AMD Ryzen AI-compatible ONNX model.
2. Run with ONNX Runtime GenAI and the Ryzen AI execution provider or DirectML flow.
3. Record the provider, model hash, prompt, output, latency, and NPU utilization.
4. Store results beside the Wolfram/Isabelle/Python certificates rather than mixing them into the Ollama GPU lane.
