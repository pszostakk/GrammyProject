# Quick CDK Deploy Script
# Builds Docker image, runs frontend build, and deploys with CDK

param(
    [switch]$NoPrompt
)

Write-Host "🚀 Starting Quick CDK Deploy..." -ForegroundColor Cyan

# Step 1: Build Docker image
Write-Host "`n📦 Building Docker image..." -ForegroundColor Yellow
Push-Location frontend
docker build -t grammy .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Step 2: Run container and build frontend
Write-Host "`n🏗️  Running frontend build in Docker..." -ForegroundColor Yellow
$frontendPath = (Get-Location).Path
docker run --rm -v "${frontendPath}/dist:/out" grammy sh -c "npm run build && cp -r dist/* /out"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host "✅ Frontend built successfully" -ForegroundColor Green
Pop-Location

# Step 3: Deploy with CDK
Write-Host "`n🌥️  Running CDK deploy..." -ForegroundColor Yellow
Push-Location infrastructure/grammy

if ($NoPrompt) {
    cdk deploy --require-approval=never
} else {
    cdk deploy
}

$deployResult = $LASTEXITCODE
Pop-Location

if ($deployResult -eq 0) {
    Write-Host "`n✅ Deployment completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n❌ CDK deploy failed" -ForegroundColor Red
    exit 1
}
