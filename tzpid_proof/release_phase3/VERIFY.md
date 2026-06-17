# TZPID Phase 3 Verification Guide

Generated UTC: 2026-06-09T20:56:50+00:00
Generated from commit: `99303e1b22606b09ba32abc1706004cb3f609929`

Run these commands from `d:\tzpidNEW`.

## 1. Isabelle/HOL Build

```powershell
& 'D:\Isabelle2025\Isabelle2025-2\bin\isabelle' build -v -D 'd:\tzpidNEW\isabelle_tzpid'
```

Pass condition: command exits with code `0`.

## 2. Regenerate The Phase 2 Matrix

```powershell
python .\build_phase2_completion_matrix.py
```

Then verify there are no incomplete, missing, or unattached rows:

```powershell
Import-Csv .\TZPID_PHASE2_COMPLETION_MATRIX.csv |
  Where-Object { $_.completion_state -eq 'started_not_complete' -or $_.missing_files -ne '' -or $_.isabelle_checked -ne 'clean_build' -or $_.wolfram_certificate -eq 'not_attached' } |
  Format-Table -AutoSize
```

Pass condition: no rows are printed.

## 3. Regenerate Certificate Scripts

```powershell
$scripts = Get-ChildItem -File -Filter 'compute_*certificate*.py' | Sort-Object Name
foreach ($s in $scripts) {
  Write-Host "RUN $($s.Name)"
  python $s.FullName
  if ($LASTEXITCODE -ne 0) { throw "Certificate failed: $($s.Name)" }
}
```

Pass condition: every script exits with code `0`.

## 4. Check Certificate JSON Status Fields

```powershell
python -c "import json; from pathlib import Path; bad=[]; count=0
for path in Path('phase2_checks').glob('*CERTIFICATE.json'):
    count += 1; data=json.loads(path.read_text(encoding='utf-8'))
    def walk(obj, trail=''):
        if isinstance(obj, dict):
            for k,v in obj.items(): yield from walk(v, f'{trail}.{k}' if trail else k)
        elif isinstance(obj, list):
            for i,v in enumerate(obj): yield from walk(v, f'{trail}[{i}]')
        else: yield trail, obj
    for trail, value in walk(data):
        if value == 'fail': bad.append((str(path), trail))
print(f'certificate_json_files={count}')
assert not bad, bad
print('all certificate JSON status fields pass')"
```

Pass condition: `all certificate JSON status fields pass`.

## 5. Validate Release JSON

```powershell
python -m json.tool .\release_phase3\MANIFEST.json > $null
python -m json.tool .\release_phase3\CERTIFICATE_MANIFEST.json > $null
python -m json.tool .\release_phase3\HDF5_ARTIFACTS.json > $null
python -m json.tool .\release_phase3\ZENODO_METADATA.json > $null
```

Pass condition: every command exits with code `0`.

## 6. Git And Release Account Check

```powershell
git status --short --branch
git remote -v
git log -3 --oneline
```

Expected remote: `https://github.com/DanielAlexanderTrawin/tzpid-proof-pipeline.git`.

Expected note: user working notes may remain untracked until intentionally added:

- `fithflip.txt`
- `hyper-universality.txt`
- `key_nondimensional_numbers.txt`
