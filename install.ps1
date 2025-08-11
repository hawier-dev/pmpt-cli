# PMPT CLI Windows Installation Script - Builds Executable
# PowerShell script to build and install PMPT CLI executable on Windows

param(
    [switch]$Force = $false
)

Write-Host "🚀 PMPT CLI Windows Installer (Executable Build)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Set installation directories
$installDir = "$env:LOCALAPPDATA\pmpt-cli"
$binDir = "$env:LOCALAPPDATA\pmpt"

# Check if already installed and not forcing
if ((Test-Path "$binDir\pmpt.exe") -and -not $Force) {
    Write-Host "⚠️  PMPT CLI is already installed" -ForegroundColor Yellow
    Write-Host "Use -Force to reinstall" -ForegroundColor Yellow
    $response = Read-Host "Do you want to continue? (y/N)"
    if ($response -notmatch '^[Yy]') {
        Write-Host "Installation cancelled" -ForegroundColor Red
        exit 0
    }
}

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

# Remove existing installation if forcing
if ((Test-Path $installDir) -and $Force) {
    Write-Host "🗑️  Removing existing source..." -ForegroundColor Yellow
    Remove-Item $installDir -Recurse -Force -ErrorAction SilentlyContinue
}
if ((Test-Path $binDir) -and $Force) {
    Write-Host "🗑️  Removing existing executable..." -ForegroundColor Yellow
    Remove-Item $binDir -Recurse -Force -ErrorAction SilentlyContinue
}

# Create installation directory
Write-Host "📁 Creating installation directory..." -ForegroundColor Blue
try {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Host "✅ Created: $installDir" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create installation directory" -ForegroundColor Red
    exit 1
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

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Blue
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install dependencies"
    }
} catch {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install PyInstaller
Write-Host "📦 Installing PyInstaller..." -ForegroundColor Blue
try {
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install PyInstaller"
    }
} catch {
    Write-Host "❌ Failed to install PyInstaller" -ForegroundColor Red
    exit 1
}

# Build executable
Write-Host "🔨 Building executable..." -ForegroundColor Blue
try {
    pyinstaller --onefile --name pmpt --console --clean --noconfirm main.py
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed"
    }
} catch {
    Write-Host "❌ Failed to build executable" -ForegroundColor Red
    exit 1
}

# Check if executable was created
if (Test-Path "dist\pmpt.exe") {
    $size = [math]::Round((Get-Item "dist\pmpt.exe").Length / 1MB, 1)
    Write-Host "✅ Successfully built pmpt.exe ($size MB)" -ForegroundColor Green
    
    # Create bin directory
    if (-not (Test-Path $binDir)) {
        New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    }
    
    # Copy executable
    Copy-Item "dist\pmpt.exe" "$binDir\pmpt.exe" -Force
    Write-Host "📦 Installed executable to: $binDir\pmpt.exe" -ForegroundColor Green
    
    # Add to PATH if not already there
    $userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
    if ($userPath -notlike "*$binDir*") {
        Write-Host "🔗 Adding to PATH..." -ForegroundColor Blue
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$binDir", [EnvironmentVariableTarget]::User)
        Write-Host "✅ Added to PATH. Please restart your terminal." -ForegroundColor Green
    } else {
        Write-Host "✅ Already in PATH" -ForegroundColor Green
    }
    
    # Test installation
    Write-Host "🧪 Testing installation..." -ForegroundColor Blue
    try {
        & "$binDir\pmpt.exe" version
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Installation test passed" -ForegroundColor Green
        } else {
            throw "Test failed"
        }
    } catch {
        Write-Host "⚠️  Executable created but test failed" -ForegroundColor Yellow
        Write-Host "You may need to restart your terminal" -ForegroundColor Yellow
    }
    
    Write-Host "" 
    Write-Host "🎉 PMPT CLI Installation Complete!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "• Executable: $binDir\pmpt.exe" -ForegroundColor White
    Write-Host "• Run 'pmpt' from any directory to use the tool" -ForegroundColor White
    Write-Host "• Run 'pmpt --help' for help" -ForegroundColor White
    Write-Host "• Run 'pmpt config' to configure your API keys" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: Restart your terminal if the command is not found" -ForegroundColor Yellow
    
} else {
    Write-Host "❌ Build failed - executable not found" -ForegroundColor Red
    exit 1
}