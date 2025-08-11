# PMPT CLI Windows Installation Script
# PowerShell script to install PMPT CLI on Windows

param(
    [switch]$Force = $false
)

Write-Host "🚀 PMPT CLI Windows Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python 3.8+ is required but not found" -ForegroundColor Red
    Write-Host "Please install Python from: https://python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

# Check if Git is installed
Write-Host "🔍 Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
    } else {
        throw "Git not found"
    }
} catch {
    Write-Host "❌ Git is required but not found" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Create installation directory
$installDir = "$env:LOCALAPPDATA\pmpt-cli"
Write-Host "📁 Installation directory: $installDir" -ForegroundColor Blue

if (Test-Path $installDir) {
    if ($Force) {
        Write-Host "🗑️  Removing existing installation..." -ForegroundColor Yellow
        Remove-Item -Path $installDir -Recurse -Force
    } else {
        Write-Host "⚠️  Existing installation found. Use -Force to overwrite" -ForegroundColor Yellow
        $response = Read-Host "Do you want to continue? (y/N)"
        if ($response -notmatch '^[Yy]') {
            Write-Host "Installation cancelled" -ForegroundColor Red
            exit 1
        }
        Remove-Item -Path $installDir -Recurse -Force
    }
}

# Clone repository
Write-Host "📥 Cloning PMPT CLI repository..." -ForegroundColor Blue
try {
    git clone https://github.com/hawier-dev/pmpt-cli.git $installDir
    if ($LASTEXITCODE -ne 0) {
        throw "Git clone failed"
    }
} catch {
    Write-Host "❌ Failed to clone repository" -ForegroundColor Red
    exit 1
}

# Change to installation directory
Set-Location $installDir

# Install package in development mode
Write-Host "📦 Installing PMPT CLI..." -ForegroundColor Blue
try {
    pip install -e .
    if ($LASTEXITCODE -ne 0) {
        throw "pip install failed"
    }
} catch {
    Write-Host "❌ Failed to install package" -ForegroundColor Red
    exit 1
}

# Check if installation was successful
Write-Host "🧪 Testing installation..." -ForegroundColor Blue
try {
    $pmptVersion = pmpt version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Installation successful!" -ForegroundColor Green
        Write-Host $pmptVersion -ForegroundColor Green
    } else {
        throw "pmpt command not found"
    }
} catch {
    Write-Host "❌ Installation verification failed" -ForegroundColor Red
    Write-Host "The 'pmpt' command might not be in your PATH" -ForegroundColor Yellow
    Write-Host "You may need to restart your terminal if this is a new installation" -ForegroundColor Yellow
}

Write-Host "" 
Write-Host "🎉 PMPT CLI Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "• Run 'pmpt' to get started" -ForegroundColor White
Write-Host "• Run 'pmpt --help' for help" -ForegroundColor White
Write-Host "• Run 'pmpt config' to configure your API keys" -ForegroundColor White
Write-Host ""
Write-Host "Note: Updates work immediately, but new installations may require terminal restart" -ForegroundColor Yellow