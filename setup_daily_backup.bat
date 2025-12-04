@echo off
REM ============================================
REM SETUP DAILY DATABASE BACKUP TASK
REM Creates Windows Task Scheduler job
REM ============================================

echo ============================================
echo SETTING UP DAILY DATABASE BACKUP
echo ============================================
echo.

REM Delete existing task if it exists
schtasks /Delete /TN "SyncPredictionsDatabase" /F >nul 2>&1

REM Create new task - runs daily at 2:00 AM
schtasks /Create /TN "SyncPredictionsDatabase" /TR "python C:\Users\nashr\max-ev-sports\sync_database_backups.py" /SC DAILY /ST 02:00 /RU "%USERNAME%" /RL HIGHEST /F

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Task created successfully
    echo.
    echo Task Name: SyncPredictionsDatabase
    echo Schedule: Daily at 2:00 AM
    echo Action: Download and sync predictions.db to C: and D: drives
    echo.
    echo Backup Locations:
    echo   1. C:\Users\nashr\max-ev-sports\backend\ml\predictions_backup.db
    echo   2. D:\predictions_backup.db
    echo.
    echo Log File: C:\Users\nashr\max-ev-sports\database_sync.log
    echo.
    echo ============================================
    echo To run the backup now, execute:
    echo   python C:\Users\nashr\max-ev-sports\sync_database_backups.py
    echo.
    echo To check task status:
    echo   schtasks /Query /TN "SyncPredictionsDatabase"
    echo ============================================
) else (
    echo [ERROR] Failed to create task
    echo Please run this script as Administrator
)

pause
