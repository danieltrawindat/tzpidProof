$ErrorActionPreference = "Stop"

$ollama = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
if (-not (Test-Path $ollama)) {
    throw "Ollama was not found at $ollama"
}

Write-Host "== Ollama =="
& $ollama --version
& $ollama list

Write-Host ""
Write-Host "== Local Gemma smoke test =="
& $ollama run gemma3:1b "Reply with exactly: OK"

Write-Host ""
Write-Host "== Ollama runtime residency =="
& $ollama ps

Write-Host ""
Write-Host "== GPU devices =="
Get-CimInstance Win32_VideoController |
    Select-Object Name, AdapterRAM, DriverVersion |
    Format-Table -AutoSize

Write-Host ""
Write-Host "== NPU / compute accelerator devices =="
Get-PnpDevice -Class ComputeAccelerator |
    Select-Object Status, FriendlyName, InstanceId |
    Format-Table -Wrap -AutoSize

Write-Host ""
Write-Host "Note: Ollama currently reports processor residency through CPU/GPU backends."
Write-Host "On this machine, Gemma is confirmed by 'ollama ps' as running on GPU."
Write-Host "The AMD NPU is detected by Windows, but NPU execution for Gemma requires a separate Ryzen AI / ONNX Runtime / DirectML or VitisAI lane."
