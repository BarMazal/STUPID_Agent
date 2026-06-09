# Setup Script for STUPID Workspace Ingestion & Visualization Pipeline
# Operating System: Windows (PowerShell)

Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "[SYSTEM] Starting STUPID Workspace Bringup and Environment Setup..." -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

# Step 1: Check Python installation
Write-Host "`n[CHECK] Checking Python installation..." -ForegroundColor Yellow
$pythonPath = "python"
$pythonInstalled = $false
$pythonVersion = ""

# Helper to verify a python path works
function Test-PythonPath($path) {
    try {
        # Run version command and check if it runs successfully and contains 'Python'
        $version = & $path --version 2>$null
        if ($LASTEXITCODE -eq 0 -and $version -like "*Python*") {
            return @($true, $version)
        }
    } catch {}
    return @($false, "")
}

# Try default system python command
$res = Test-PythonPath "python"
if ($res[0]) {
    $pythonInstalled = $true
    $pythonVersion = $res[1]
} else {
    # Try common installation locations on Windows
    $commonDirs = @(
        "$env:LOCALAPPDATA\Programs\Python",
        "C:\Program Files\Python"
    )
    foreach ($dir in $commonDirs) {
        if (Test-Path $dir) {
            # Find python.exe in subfolders (e.g. Python312, Python311)
            $foundPythons = Get-ChildItem -Path $dir -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue
            foreach ($py in $foundPythons) {
                $res = Test-PythonPath $py.FullName
                if ($res[0]) {
                    $pythonPath = $py.FullName
                    $pythonInstalled = $true
                    $pythonVersion = $res[1]
                    # Prepend python folder to path for this session so venv creation and pip install works
                    $pyDir = Split-Path $py.FullName -Parent
                    $env:PATH = "$pyDir;" + $env:PATH
                    break
                }
            }
        }
        if ($pythonInstalled) { break }
    }
}

if ($pythonInstalled) {
    Write-Host "[ OK ] Python found: $pythonVersion ($pythonPath)" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Python is not installed, not in your system PATH, or pointing to a Microsoft Store placeholder." -ForegroundColor Red
    Write-Host "[INFO] Please download and install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "[INFO] Make sure to check the box 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host "[INFO] Note: If Python is installed but fails, search Windows Settings for 'App Execution Aliases' and turn off Python." -ForegroundColor Yellow
    Exit 1
}

# Step 2: Create virtual environment (.venv)
Write-Host "`n[VENV] Setting up virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "   Creating new virtual environment '.venv'..." -ForegroundColor Gray
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] Failed to create virtual environment." -ForegroundColor Red
        Exit 1
    }
    Write-Host "[ OK ] Virtual environment '.venv' created successfully." -ForegroundColor Green
} else {
    Write-Host "[ OK ] Virtual environment '.venv' already exists." -ForegroundColor Green
}

# Step 3: Install Python Dependencies
Write-Host "`n[VENV] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "   Upgrading pip and installing packages..." -ForegroundColor Gray
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\pip.exe install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] Dependency installation failed." -ForegroundColor Red
        Exit 1
    }
    Write-Host "[ OK ] Dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Host "[FAIL] requirements.txt not found!" -ForegroundColor Red
    Exit 1
}

# Step 4: Download and Setup Ollama
Write-Host "`n[OLLAMA] Checking Ollama installation..." -ForegroundColor Yellow
$ollamaInstalled = $false
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    $ollamaInstalled = $true
} elseif (Test-Path "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe") {
    $ollamaInstalled = $true
    # Add to path for this session
    $env:PATH += ";$env:LOCALAPPDATA\Programs\Ollama"
}

if ($ollamaInstalled) {
    Write-Host "[ OK ] Ollama installation detected." -ForegroundColor Green
} else {
    Write-Host "   Ollama not found. Downloading the installer..." -ForegroundColor Gray
    $installerPath = Join-Path $env:TEMP "OllamaSetup.exe"
    try {
        Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $installerPath -UseBasicParsing
        Write-Host "[ OK ] Download complete. Launching Ollama setup window..." -ForegroundColor Green
        Start-Process -FilePath $installerPath
        Read-Host -Prompt "[INPUT] Press Enter here AFTER the Ollama installation is complete to continue"
        $ollamaInstalled = $true
        # Add to path for this session
        $env:PATH += ";$env:LOCALAPPDATA\Programs\Ollama"
    } catch {
        Write-Host "[FAIL] Failed to download Ollama installer." -ForegroundColor Red
        Write-Host "[INFO] Please manually download and install Ollama from https://ollama.com" -ForegroundColor Yellow
    }
}

# Step 5: Start Ollama service & Pull Model
if ($ollamaInstalled) {
    Write-Host "`n[START] Ensuring Ollama service is running..." -ForegroundColor Yellow
    
    # Check if port 11434 is responding
    $ollamaRunning = $false
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434" -ErrorAction SilentlyContinue
        if ($response -eq "Ollama is running") {
            $ollamaRunning = $true
        }
    } catch {}

    if (-not $ollamaRunning) {
        Write-Host "   Starting Ollama app..." -ForegroundColor Gray
        $ollamaAppPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama app.exe"
        if (Test-Path $ollamaAppPath) {
            Start-Process -FilePath $ollamaAppPath
            # Wait for service to warm up
            for ($i = 0; $i -lt 10; $i++) {
                Start-Sleep -Seconds 1
                try {
                    $response = Invoke-RestMethod -Uri "http://localhost:11434" -ErrorAction SilentlyContinue
                    if ($response -eq "Ollama is running") {
                        $ollamaRunning = $true
                        break
                    }
                } catch {}
            }
        }
    }

    if ($ollamaRunning) {
        Write-Host "[ OK ] Ollama service is running." -ForegroundColor Green
        Write-Host "`n[MODEL] Pulling deepseek-r1:14b language model (this may take a few minutes)..." -ForegroundColor Yellow
        ollama pull deepseek-r1:14b
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[ OK ] Model deepseek-r1:14b pulled successfully." -ForegroundColor Green
        } else {
            Write-Host "[WARN] Failed to pull model automatically. You can run 'ollama pull deepseek-r1:14b' manually." -ForegroundColor Yellow
        }
    } else {
        Write-Host "[FAIL] Could not start or detect Ollama service." -ForegroundColor Red
        Write-Host "[INFO] Please launch Ollama manually and pull the model: 'ollama pull deepseek-r1:14b'" -ForegroundColor Yellow
    }
}

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "[DONE] Bringup and configuration setup is complete!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "[INFO] To start the interactive configuration dashboard, run:" -ForegroundColor Yellow
Write-Host "   .venv\Scripts\python.exe STUPIDConsoleUI.py --configure" -ForegroundColor Cyan
Write-Host "`n[INFO] To run the tutorial walkthrough guide, run:" -ForegroundColor Yellow
Write-Host "   .venv\Scripts\python.exe STUPIDTutorial.py" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Green
