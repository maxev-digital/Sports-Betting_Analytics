# Complete VPS to Local Sync - December 4, 2025
# Sync ALL current VPS files to local, then commit to git

$VPS_HOST = "root@148.230.87.135"
$VPS_PATH = "/root/sporttrader"
$LOCAL_PATH = "C:\Users\nashr\max-ev-sports"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VPS TO LOCAL COMPLETE SYNC" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will sync ALL files from VPS to local" -ForegroundColor Yellow
Write-Host "VPS: $VPS_HOST : $VPS_PATH" -ForegroundColor Gray
Write-Host "Local: $LOCAL_PATH" -ForegroundColor Gray
Write-Host ""

# Critical directories to sync
$directories = @(
    "backend/routes",
    "backend/ml/props",
    "backend/ml/dfs",
    "backend/ml/feature_engineering",
    "backend/ml/training",
    "backend/ml/pytorch_models",
    "backend/ml/predictions",
    "backend/ml/data_loaders",
    "backend/scrapers/props",
    "backend/scrapers/nhl",
    "backend/scrapers/ncaab",
    "frontend/src/pages",
    "frontend/src/components",
    "frontend/src/contexts",
    "frontend/src"
)

# Critical individual files
$files = @(
    "backend/main.py",
    "backend/config.py",
    "backend/run_daily_props_workflow.py",
    "backend/generate_all_predictions_multi_bet.py",
    "backend/nhl_stats_client.py",
    "frontend/src/config.ts",
    "frontend/src/App.tsx",
    "frontend/vite.config.ts"
)

Write-Host "Syncing directories..." -ForegroundColor Yellow
$dirCount = 0

foreach ($dir in $directories) {
    $vpsDir = "$VPS_PATH/$($dir -replace '\\', '/')"
    $localDir = Join-Path $LOCAL_PATH ($dir -replace '/', '\')

    Write-Host "  Syncing: $dir" -ForegroundColor Cyan

    # Create local directory if doesn't exist
    if (-not (Test-Path $localDir)) {
        New-Item -ItemType Directory -Path $localDir -Force | Out-Null
    }

    # Use rsync-style scp (copy all files recursively)
    & scp -r "${VPS_HOST}:${vpsDir}/*" "$localDir\"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "    SUCCESS" -ForegroundColor Green
        $dirCount++
    } else {
        Write-Host "    FAILED (may be empty or not exist)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Syncing individual files..." -ForegroundColor Yellow
$fileCount = 0

foreach ($file in $files) {
    $vpsFile = "$VPS_PATH/$($file -replace '\\', '/')"
    $localFile = Join-Path $LOCAL_PATH ($file -replace '/', '\')
    $localDir = Split-Path $localFile -Parent

    Write-Host "  Syncing: $file" -ForegroundColor Cyan

    # Create directory if doesn't exist
    if (-not (Test-Path $localDir)) {
        New-Item -ItemType Directory -Path $localDir -Force | Out-Null
    }

    & scp "${VPS_HOST}:${vpsFile}" "$localFile"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "    SUCCESS" -ForegroundColor Green
        $fileCount++
    } else {
        Write-Host "    FAILED" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SYNC SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Directories synced: $dirCount/$($directories.Count)" -ForegroundColor Green
Write-Host "Files synced: $fileCount/$($files.Count)" -ForegroundColor Green
Write-Host ""
Write-Host "All VPS files synced to local!" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Review changes with 'git status'" -ForegroundColor Yellow
