# PowerShell installation script for PMPT CLI
param(
    [switch]$Force
)

# Configuration
$AppName = "pmpt"
$RepoUrl = "https://github.com/hawier-dev/pmpt-cli.git"
$InstallDir = "$env:LOCALAPPDATA\$AppName"
$BinDir = "$env:LOCALAPPDATA\Microsoft\WindowsApps"
$WrapperScript = "$BinDir\$AppName.cmd"

Write-Host "Installing PMPT CLI..." -ForegroundColor Blue

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "Error: Python 3.8+ is required but not installed." -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Check Python version
try {
    $versionCheck = python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python version too old"
    }
} catch {
    Write-Host "Error: Python 3.8+ is required." -ForegroundColor Red
    exit 1
}

# Check if git is installed
try {
    git --version | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Git not found"
    }
} catch {
    Write-Host "Error: Git is required but not installed." -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com" -ForegroundColor Yellow
    exit 1
}

# Create directories
if (!(Test-Path -Path (Split-Path $InstallDir -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $InstallDir -Parent) -Force | Out-Null
}

# Remove existing installation
if (Test-Path -Path $InstallDir) {
    if ($Force) {
        Write-Host "Removing existing installation..." -ForegroundColor Yellow
        Remove-Item -Path $InstallDir -Recurse -Force
    } else {
        $response = Read-Host "Existing installation found. Remove it? (y/N)"
        if ($response -match "^[Yy]") {
            Write-Host "Removing existing installation..." -ForegroundColor Yellow
            Remove-Item -Path $InstallDir -Recurse -Force
        } else {
            Write-Host "Installation cancelled." -ForegroundColor Yellow
            exit 1
        }
    }
}

# Clone repository
Write-Host "Cloning repository..." -ForegroundColor Blue
try {
    git clone $RepoUrl $InstallDir
    if ($LASTEXITCODE -ne 0) {
        throw "Git clone failed"
    }
} catch {
    Write-Host "Error: Failed to clone repository." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Blue
Set-Location $InstallDir
try {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        throw "Virtual environment creation failed"
    }
} catch {
    Write-Host "Error: Failed to create virtual environment." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Blue
try {
    & "$InstallDir\venv\Scripts\python.exe" -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        throw "Pip upgrade failed"
    }
    
    & "$InstallDir\venv\Scripts\pip.exe" install -e .
    if ($LASTEXITCODE -ne 0) {
        throw "Package installation failed"
    }
} catch {
    Write-Host "Error: Failed to install dependencies." -ForegroundColor Red
    exit 1
}

# Create wrapper script
Write-Host "Creating wrapper script..." -ForegroundColor Blue
$wrapperContent = @"
@echo off
"$InstallDir\venv\Scripts\python.exe" "$InstallDir\pmpt_main.py" %*
"@

try {
    $wrapperContent | Out-File -FilePath $WrapperScript -Encoding ASCII
    Write-Host "✓ PMPT CLI installed successfully!" -ForegroundColor Green
    Write-Host "Usage: $AppName" -ForegroundColor Blue
    Write-Host "First run will guide you through configuration." -ForegroundColor Blue
} catch {
    Write-Host "Error: Failed to create wrapper script." -ForegroundColor Red
    Write-Host "You can manually run: python `"$InstallDir\pmpt_main.py`"" -ForegroundColor Yellow
}

# Test installation
Write-Host "`nTesting installation..." -ForegroundColor Blue
try {
    & $AppName --help 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Installation test successful!" -ForegroundColor Green
    } else {
        Write-Host "⚠ Installation completed but test failed. You may need to restart your terminal." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Installation completed but test failed. You may need to restart your terminal." -ForegroundColor Yellow
}