# Selective Frontend Deployment - December 4, 2025
# Deploy all Dec 3 improvements EXCEPT ModelPerformance.tsx and PredictionsDatabase.tsx

$VPS_HOST = "root@148.230.87.135"
$LOCAL_FRONTEND = "C:\Users\nashr\max-ev-sports\frontend"
$VPS_FRONTEND = "/root/sporttrader/frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SELECTIVE FRONTEND DEPLOYMENT - DEC 4" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Deploying Dec 3 improvements..." -ForegroundColor Yellow
Write-Host "EXCLUDING: ModelPerformance.tsx, PredictionsDatabase.tsx (already correct on VPS)" -ForegroundColor Green
Write-Host ""

# List of Dec 3 files to deploy (from your modification dates)
$filesToDeploy = @(
    "src/pages/Props.tsx",
    "src/pages/Pricing.tsx",
    "src/pages/MaxEvEdges.tsx",
    "src/pages/PropsPerformance.tsx",
    "src/pages/Alerts.tsx",
    "src/pages/Odds.tsx",
    "src/pages/Settings.tsx",
    "src/pages/LiveGames.tsx",
    "src/pages/Login.tsx",
    "src/pages/SignUp.tsx",
    "src/pages/DfsCrusher.tsx",
    "src/config.ts",
    "src/components/BetSlipToast.tsx",
    "src/components/GameCard.tsx",
    "src/components/GlobalAlertMonitor.tsx",
    "src/components/Navigation.tsx",
    "src/components/PersonalBetAnalytics.tsx",
    "src/components/PricingToastSequence.tsx",
    "src/components/PropTypeTabs.tsx",
    "src/components/TierGate.tsx",
    "src/contexts/AuthContext.tsx"
)

Write-Host "Files to deploy:" -ForegroundColor Yellow
foreach ($f in $filesToDeploy) {
    Write-Host "  - $f" -ForegroundColor Gray
}
Write-Host ""

# Deploy each file
$successCount = 0
$errorCount = 0

foreach ($file in $filesToDeploy) {
    $localPath = Join-Path $LOCAL_FRONTEND $file
    $remotePath = "$VPS_FRONTEND/$($file -replace '\\', '/')"

    if (Test-Path $localPath) {
        Write-Host "Deploying: $file" -ForegroundColor Cyan

        # Use scp to copy file
        & scp $localPath "${VPS_HOST}:${remotePath}"

        if ($LASTEXITCODE -eq 0) {
            Write-Host "  SUCCESS" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "  FAILED" -ForegroundColor Red
            $errorCount++
        }
    } else {
        Write-Host "  File not found locally: $localPath" -ForegroundColor Yellow
        $errorCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYING BUILT FRONTEND (dist/)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Deploy the entire dist folder (compiled frontend)
Write-Host "Deploying compiled frontend from dist/..." -ForegroundColor Yellow
& scp -r "$LOCAL_FRONTEND\dist\*" "${VPS_HOST}:${VPS_FRONTEND}/dist/"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Built frontend deployed successfully" -ForegroundColor Green
} else {
    Write-Host "Failed to deploy built frontend" -ForegroundColor Red
    $errorCount++
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Source files deployed: $successCount" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "Errors: $errorCount" -ForegroundColor Red
} else {
    Write-Host "Errors: $errorCount" -ForegroundColor Green
}
Write-Host ""
Write-Host "PROTECTED FILES (not deployed):" -ForegroundColor Yellow
Write-Host "  - ModelPerformance.tsx (VPS version kept)" -ForegroundColor Green
Write-Host "  - PredictionsDatabase.tsx (VPS version kept)" -ForegroundColor Green
Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Test at https://max-ev-sports.com" -ForegroundColor Yellow
