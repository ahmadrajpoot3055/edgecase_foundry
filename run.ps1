# EdgeCase Foundry PowerShell Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  EdgeCase Foundry - Minimalist Edge-Case Testing" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Load .env variables into current process
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $parts = $line.Split("=", 2)
            [System.Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim(), "Process")
        }
    }
    Write-Host "[*] Loaded environment variables from .env" -ForegroundColor Green
}

if (-not (Test-Path ".\.venv\Scripts\streamlit.exe")) {
    Write-Host "[!] Virtual environment not found. Creating .venv..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\pip install -r requirements.txt
}

Write-Host "[*] Launching Streamlit..." -ForegroundColor Green
& .\.venv\Scripts\streamlit.exe run app.py
