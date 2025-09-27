# Setup script for Messenger AI Assistant (Windows PowerShell)

Write-Host "🚀 Setting up Messenger AI Assistant..." -ForegroundColor Green

# Check if running on Windows
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "❌ PowerShell 5+ is required" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PowerShell version: $($PSVersionTable.PSVersion)" -ForegroundColor Green

# Check Node.js version
try {
    $nodeVersion = node --version
    $nodeMajorVersion = [int]($nodeVersion -replace 'v', '' -split '\.')[0]
    if ($nodeMajorVersion -lt 20) {
        Write-Host "❌ Node.js version 20+ is required. Current version: $nodeVersion" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 20+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check Python version
try {
    $pythonVersion = python --version
    $pythonMajorMinor = ($pythonVersion -split ' ')[1] -split '\.' | Select-Object -First 2
    $pythonVersionNumber = [double]"$($pythonMajorMinor[0]).$($pythonMajorMinor[1])"
    if ($pythonVersionNumber -lt 3.11) {
        Write-Host "❌ Python 3.11+ is required. Current version: $pythonVersion" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 is not installed. Please install Python 3.11+ from https://python.org/" -ForegroundColor Red
    exit 1
}

# Check gcloud CLI
try {
    gcloud --version | Out-Null
    Write-Host "✅ Google Cloud CLI installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud CLI is not installed. Please install from https://cloud.google.com/sdk/docs/install" -ForegroundColor Red
    exit 1
}

# Check gcloud authentication
try {
    $activeAccounts = gcloud auth list --filter=status:ACTIVE --format="value(account)"
    if (-not $activeAccounts) {
        Write-Host "❌ Not authenticated with Google Cloud. Please run: gcloud auth login" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Google Cloud authenticated" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud authentication failed" -ForegroundColor Red
    exit 1
}

# Set up environment variables
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env file with your Google Cloud project details" -ForegroundColor Yellow
}

# Enable required Google Cloud APIs
Write-Host "🔧 Enabling Google Cloud APIs..." -ForegroundColor Yellow
gcloud services enable aiplatform.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable generativelanguage.googleapis.com

Write-Host "✅ Google Cloud APIs enabled" -ForegroundColor Green

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
Set-Location "assist/server"
pip install -r requirements.txt

Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Build Chrome extension
Write-Host "🔨 Building Chrome extension..." -ForegroundColor Yellow
Set-Location "../chrome-ext"
npm install
npm run build

Write-Host "✅ Chrome extension built" -ForegroundColor Green

# Create directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "logs" -Force | Out-Null
New-Item -ItemType Directory -Path "data" -Force | Out-Null

Write-Host "✅ Directories created" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your Google Cloud project details" -ForegroundColor White
Write-Host "2. Run 'make dev' to start the development server" -ForegroundColor White
Write-Host "3. Load the Chrome extension from chrome-ext/dist directory" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see docs/README.md" -ForegroundColor Cyan
