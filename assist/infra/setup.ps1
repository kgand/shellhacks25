#requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$SkipExtensionBuild  # pass -SkipExtensionBuild to skip building the Chrome extension
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

    # Check Node.js version
    try {
        $nodeVersion = node --version
        $nodeMajorVersion = [int]($nodeVersion -replace '^v','' -split '\.')[0]
        if ($nodeMajorVersion -lt 20) {
            Write-Host ("Node.js 20+ is required. Current: {0}" -f $nodeVersion) -ForegroundColor Red
            exit 1
        }
        Write-Host ("Node.js version: {0}" -f $nodeVersion) -ForegroundColor Green
    } catch {
        Write-Host "Node.js is not installed. Install Node.js 20+ from https://nodejs.org/" -ForegroundColor Red
        exit 1
    }

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
    $extDirCandidates = @(
        (Join-Path $repoRoot "chrome-ext"),
        (Join-Path $repoRoot "assist\chrome-ext")
    )

    $serverDir = $serverDirCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    $extDir    = $extDirCandidates    | Where-Object { Test-Path $_ } | Select-Object -First 1

    if (-not $serverDir) {
        throw "Could not locate 'server' directory. Checked:`n  - $($serverDirCandidates -join "`n  - ")"
    }
    if (-not $extDir) {
        throw "Could not locate 'chrome-ext' directory. Checked:`n  - $($extDirCandidates -join "`n  - ")"
    }

    $envPath    = Join-Path $repoRoot ".env"
    $envExample = Join-Path $repoRoot ".env.example"
    $logsDir    = Join-Path $repoRoot "logs"
    $dataDir    = Join-Path $repoRoot "data"
    $docsReadme = Join-Path $repoRoot "docs\README.md"

    Write-Host "Repo root: $repoRoot" -ForegroundColor DarkGray
    Write-Host "Server dir: $serverDir" -ForegroundColor DarkGray
    Write-Host "Chrome-ext dir: $extDir" -ForegroundColor DarkGray

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

    # Build Chrome extension (optional / auto-detect)
    if ($SkipExtensionBuild) {
        Write-Host "Skipping Chrome extension build (per -SkipExtensionBuild)" -ForegroundColor Yellow
    } else {
        Push-Location $extDir
        try {
            $pkgJsonPath = Join-Path $extDir "package.json"
            $hasPackage  = Test-Path $pkgJsonPath
            $hasBuild    = $false

            if ($hasPackage) {
                try {
                    $pkg = Get-Content $pkgJsonPath -Raw | ConvertFrom-Json
                    $hasBuild = $null -ne $pkg.scripts -and $pkg.scripts.PSObject.Properties.Name -contains "build"
                } catch {
                    Write-Host "Warning: could not parse package.json; will try to run build if present." -ForegroundColor Yellow
                }
            }

            if (-not $hasPackage -or -not $hasBuild) {
                Write-Host "No build step detected for Chrome extension. You can load the folder as an unpacked extension if it contains plain JS/HTML/CSS and a valid manifest.json." -ForegroundColor Yellow
            } else {
                Write-Host "Building Chrome extension..." -ForegroundColor Yellow

                # Call npm.cmd to avoid npm.ps1 + StrictMode issues
                $npmCmd = (Get-Command npm.cmd -ErrorAction SilentlyContinue).Source
                if (-not $npmCmd) {
                    # common fallback
                    $npmCmd = Join-Path $env:ProgramFiles "nodejs\npm.cmd"
                }
                if (-not (Test-Path $npmCmd)) {
                    throw "Could not find npm.cmd. Ensure Node.js is installed correctly."
                }

                if (Test-Path "package-lock.json") {
                    & $npmCmd ci
                } else {
                    & $npmCmd install
                }
                & $npmCmd run build

                Write-Host "Chrome extension built" -ForegroundColor Green
            }
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
    Write-Host "2. Run 'make dev' to start the development server"
    Write-Host "3. Load the Chrome extension:"
    Write-Host "   - If a build was produced: chrome-ext\dist (or assist\chrome-ext\dist)"
    Write-Host "   - If no build step: load the source folder directly ONLY if it is plain JS/HTML/CSS with a valid manifest.json"
    Write-Host ""
    Write-Host ("For more information, see {0}" -f $docsReadme) -ForegroundColor Cyan
}
finally {
    Pop-Location
}
