#requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$SkipScreenCapture  # pass -SkipScreenCapture to skip installing screen capture dependencies
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Move to the folder this script lives in
Push-Location $PSScriptRoot
try {
    Write-Host "Setting up Messenger AI Assistant..." -ForegroundColor Green

    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Host "PowerShell 5+ is required" -ForegroundColor Red
        exit 1
    }
    Write-Host ("PowerShell version: {0}" -f $PSVersionTable.PSVersion) -ForegroundColor Green


    # Check Python version
    try {
        $pythonVersion = python --version 2>&1
        $pythonMajorMinor = ($pythonVersion -split ' ')[1] -split '\.' | Select-Object -First 2
        $pythonVersionNumber = [double]"$($pythonMajorMinor[0]).$($pythonMajorMinor[1])"
        if ($pythonVersionNumber -lt 3.11) {
            Write-Host ("Python 3.11+ is required. Current: {0}" -f $pythonVersion) -ForegroundColor Red
            exit 1
        }
        Write-Host ("Python version: {0}" -f $pythonVersion) -ForegroundColor Green
    } catch {
        Write-Host "Python 3.11+ is required. Install from https://python.org/" -ForegroundColor Red
        exit 1
    }

    # Check gcloud CLI
    try {
        gcloud --version | Out-Null
        Write-Host "Google Cloud CLI installed" -ForegroundColor Green
    } catch {
        Write-Host "Google Cloud CLI is not installed. See https://cloud.google.com/sdk/docs/install" -ForegroundColor Red
        exit 1
    }

    # Check gcloud authentication
    try {
        $activeAccounts = gcloud auth list --filter=status:ACTIVE --format="value(account)"
        if (-not $activeAccounts) {
            Write-Host "Not authenticated. Run: gcloud auth login" -ForegroundColor Red
            exit 1
        }
        Write-Host "Google Cloud authenticated" -ForegroundColor Green
    } catch {
        Write-Host "Google Cloud authentication failed" -ForegroundColor Red
        exit 1
    }

    # Resolve important paths relative to repo root (parent of /infra)
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

    # Try common layouts
    $serverDirCandidates = @(
        (Join-Path $repoRoot "server"),
        (Join-Path $repoRoot "assist\server")
    )
    $screenCaptureDirCandidates = @(
        (Join-Path $repoRoot "screen_capture"),
        (Join-Path $repoRoot "assist\screen_capture")
    )

    $serverDir = $serverDirCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    $screenCaptureDir = $screenCaptureDirCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

    if (-not $serverDir) {
        throw "Could not locate 'server' directory. Checked:`n  - $($serverDirCandidates -join "`n  - ")"
    }
    if (-not $screenCaptureDir) {
        throw "Could not locate 'screen_capture' directory. Checked:`n  - $($screenCaptureDirCandidates -join "`n  - ")"
    }

    $envPath    = Join-Path $repoRoot ".env"
    $envExample = Join-Path $repoRoot ".env.example"
    $logsDir    = Join-Path $repoRoot "logs"
    $dataDir    = Join-Path $repoRoot "data"
    $docsReadme = Join-Path $repoRoot "docs\README.md"

    Write-Host "Repo root: $repoRoot" -ForegroundColor DarkGray
    Write-Host "Server dir: $serverDir" -ForegroundColor DarkGray
    Write-Host "Screen capture dir: $screenCaptureDir" -ForegroundColor DarkGray

    # Set up environment variables
    if (-not (Test-Path $envPath)) {
        Write-Host "Creating .env file..." -ForegroundColor Yellow
        if (Test-Path $envExample) {
            Copy-Item $envExample $envPath -Force
            Write-Host "Please edit .env with your Google Cloud project details" -ForegroundColor Yellow
        } else {
            Write-Host ".env.example not found at $envExample" -ForegroundColor Red
        }
    }

    # Enable required Google Cloud APIs
    Write-Host "Enabling Google Cloud APIs..." -ForegroundColor Yellow
    gcloud services enable aiplatform.googleapis.com firestore.googleapis.com generativelanguage.googleapis.com
    Write-Host "Google Cloud APIs enabled" -ForegroundColor Green

    # Install Python dependencies
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    Push-Location $serverDir
    try {
        if (-not (Test-Path "requirements.txt")) {
            throw "requirements.txt not found in $serverDir"
        }
        python -m pip install -r requirements.txt
        Write-Host "Python dependencies installed" -ForegroundColor Green
    } finally {
        Pop-Location
    }

    # Install screen capture dependencies
    if ($SkipScreenCapture) {
        Write-Host "Skipping screen capture dependencies (per -SkipScreenCapture)" -ForegroundColor Yellow
    } else {
        Push-Location $screenCaptureDir
        try {
            if (-not (Test-Path "requirements.txt")) {
                throw "requirements.txt not found in $screenCaptureDir"
            }
            Write-Host "Installing screen capture dependencies..." -ForegroundColor Yellow
            python -m pip install -r requirements.txt
            Write-Host "Screen capture dependencies installed" -ForegroundColor Green
        } finally {
            Pop-Location
        }
    }

    # Create directories
    Write-Host "Creating directories..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Write-Host "Directories created" -ForegroundColor Green

    Write-Host ""
    Write-Host "Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Edit .env with your Google Cloud project details"
    Write-Host "2. Run 'python assist/launcher.py' to start the application"
    Write-Host "3. Open Messenger Web in your browser"
    Write-Host "4. Use the screen capture GUI to start recording"
    Write-Host ""
    Write-Host ("For more information, see {0}" -f $docsReadme) -ForegroundColor Cyan
}
finally {
    Pop-Location
}
