# GHOST PASS GitHub Push Script
# Run this script in PowerShell to push the code to GitHub

Write-Host "🚀 GHOST PASS GitHub Push Script" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host ""

# Function to run commands with error handling
function Invoke-GitCommand {
    param(
        [string]$Command,
        [string]$Description
    )
    
    Write-Host "🔄 $Description..." -ForegroundColor Yellow
    try {
        $result = Invoke-Expression $Command 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host $result -ForegroundColor White
            return $true
        } else {
            Write-Host "❌ Error running: $Command" -ForegroundColor Red
            Write-Host $result -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ Exception: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Check if git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not available. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing git repository..." -ForegroundColor Yellow
    if (-not (Invoke-GitCommand "git init" "Initializing git repository")) {
        exit 1
    }
}

# Stage all files
if (-not (Invoke-GitCommand "git add ." "Staging all files")) {
    exit 1
}

# Check status
if (-not (Invoke-GitCommand "git status" "Checking git status")) {
    exit 1
}

# Commit changes
$commitMessage = "🚀 Cleaned up GhostPass, finalized code & docs"
if (-not (Invoke-GitCommand "git commit -m `"$commitMessage`"" "Committing changes")) {
    exit 1
}

# Get GitHub username
Write-Host ""
Write-Host "🔗 Setting up GitHub remote..." -ForegroundColor Yellow
$username = Read-Host "Enter your GitHub username"
if (-not $username) {
    Write-Host "❌ Username is required." -ForegroundColor Red
    exit 1
}

# Add remote
$remoteUrl = "https://github.com/$username/ghostpass.git"
if (-not (Invoke-GitCommand "git remote add origin $remoteUrl" "Adding remote repository")) {
    # If remote already exists, set the URL
    Write-Host "🔄 Remote already exists, updating URL..." -ForegroundColor Yellow
    Invoke-GitCommand "git remote set-url origin $remoteUrl" "Updating remote URL"
}

# Verify remote
if (-not (Invoke-GitCommand "git remote -v" "Verifying remote")) {
    exit 1
}

# Push to GitHub
Write-Host ""
Write-Host "⬆️ Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Note: You may be prompted for your GitHub credentials." -ForegroundColor Cyan

if (-not (Invoke-GitCommand "git push -u origin main" "Pushing to GitHub")) {
    Write-Host ""
    Write-Host "❌ Push failed. Common issues:" -ForegroundColor Red
    Write-Host "1. Repository doesn't exist on GitHub - create it first" -ForegroundColor Yellow
    Write-Host "2. Authentication failed - check your credentials" -ForegroundColor Yellow
    Write-Host "3. Network issues - check your internet connection" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create repository on GitHub:" -ForegroundColor Cyan
    Write-Host "1. Go to https://github.com/new" -ForegroundColor White
    Write-Host "2. Repository name: ghostpass" -ForegroundColor White
    Write-Host "3. Make it public" -ForegroundColor White
    Write-Host "4. Don't initialize with README (we already have one)" -ForegroundColor White
    Write-Host "5. Click Create repository" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "✅ Push completed successfully!" -ForegroundColor Green
Write-Host "🎉 GHOST PASS is now live on GitHub!" -ForegroundColor Green
Write-Host "📍 Repository: https://github.com/$username/ghostpass" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to your GitHub repository" -ForegroundColor White
Write-Host "2. Create a new release (v0.1.0)" -ForegroundColor White
Write-Host "3. Add release notes from CHANGELOG.md" -ForegroundColor White
Write-Host "4. Build executables with: python build.py" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 