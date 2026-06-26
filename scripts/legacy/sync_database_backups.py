"""
AUTOMATED DATABASE BACKUP SYNC
Downloads production predictions.db to both C: and D: drive backups
Runs daily via Windows Task Scheduler
"""

import subprocess
import shutil
import os
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
log_file = Path("C:/Users/nashr/max-ev-sports/database_sync.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
PRODUCTION_HOST = "root@148.230.87.135"
PRODUCTION_DB = "/root/sporttrader/backend/ml/predictions.db"
BACKUP_LOCATIONS = [
    "C:/Users/nashr/max-ev-sports/backend/ml/predictions_backup.db",
    "D:/predictions_backup.db"
]

def download_database():
    """Download database from production server"""
    logger.info("="*60)
    logger.info("STARTING DATABASE BACKUP SYNC")
    logger.info("="*60)

    temp_file = "C:/Users/nashr/temp_predictions_download.db"

    try:
        # Download from production using scp
        logger.info(f"Downloading from {PRODUCTION_HOST}...")
        cmd = f'scp {PRODUCTION_HOST}:{PRODUCTION_DB} {temp_file}'

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            logger.error(f"Download failed: {result.stderr}")
            return None

        # Verify file exists and has content
        if not os.path.exists(temp_file):
            logger.error("Downloaded file not found")
            return None

        file_size = os.path.getsize(temp_file)
        logger.info(f"Download complete: {file_size / (1024*1024):.2f} MB")

        return temp_file

    except subprocess.TimeoutExpired:
        logger.error("Download timed out after 60 seconds")
        return None
    except Exception as e:
        logger.error(f"Download error: {e}")
        return None

def verify_database(db_path):
    """Verify database integrity"""
    try:
        result = subprocess.run(
            f'sqlite3 {db_path} "PRAGMA integrity_check;"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        if "ok" in result.stdout.lower():
            logger.info(f"Database integrity verified: {db_path}")
            return True
        else:
            logger.error(f"Database integrity check failed: {result.stdout}")
            return False

    except Exception as e:
        logger.error(f"Integrity check error: {e}")
        return False

def get_database_stats(db_path):
    """Get database statistics"""
    try:
        # Get table counts
        result = subprocess.run(
            f'sqlite3 {db_path} "SELECT COUNT(*) FROM player_prop_predictions;"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            count = result.stdout.strip()
            logger.info(f"Database contains {count} player prop predictions")
            return count

    except Exception as e:
        logger.warning(f"Could not get stats: {e}")

    return "Unknown"

def sync_to_backups(source_file):
    """Copy database to all backup locations"""
    success_count = 0

    for backup_path in BACKUP_LOCATIONS:
        try:
            logger.info(f"Syncing to: {backup_path}")

            # Create directory if it doesn't exist
            backup_dir = os.path.dirname(backup_path)
            if backup_dir:
                os.makedirs(backup_dir, exist_ok=True)

            # Create timestamped backup of existing file (if exists)
            if os.path.exists(backup_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                old_backup = backup_path.replace(".db", f"_old_{timestamp}.db")
                shutil.copy2(backup_path, old_backup)
                logger.info(f"  Previous backup saved: {old_backup}")

            # Copy new database
            shutil.copy2(source_file, backup_path)

            # Verify
            if verify_database(backup_path):
                success_count += 1
                logger.info(f"  [SUCCESS] Synced to {backup_path}")
            else:
                logger.error(f"  [FAILED] Verification failed for {backup_path}")

        except Exception as e:
            logger.error(f"  [FAILED] Error syncing to {backup_path}: {e}")

    return success_count

def cleanup_old_backups():
    """Remove old backup files (keep last 7 days)"""
    for backup_path in BACKUP_LOCATIONS:
        try:
            backup_dir = os.path.dirname(backup_path)
            if not backup_dir or not os.path.exists(backup_dir):
                continue

            # Find old backup files
            pattern = os.path.basename(backup_path).replace(".db", "_old_*.db")
            old_files = []

            for file in os.listdir(backup_dir):
                if file.startswith(os.path.basename(backup_path).replace(".db", "_old_")):
                    file_path = os.path.join(backup_dir, file)
                    file_time = os.path.getmtime(file_path)
                    old_files.append((file_path, file_time))

            # Sort by time, keep newest 7
            old_files.sort(key=lambda x: x[1], reverse=True)

            deleted_count = 0
            for file_path, _ in old_files[7:]:  # Keep newest 7, delete rest
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except:
                    pass

            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old backup(s) from {backup_dir}")

        except Exception as e:
            logger.warning(f"Cleanup error for {backup_path}: {e}")

def main():
    """Main sync process"""
    start_time = datetime.now()

    # Download database
    temp_file = download_database()
    if not temp_file:
        logger.error("[FAILED] Could not download database")
        return False

    # Verify downloaded file
    if not verify_database(temp_file):
        logger.error("[FAILED] Downloaded database is corrupted")
        os.remove(temp_file)
        return False

    # Get stats
    get_database_stats(temp_file)

    # Sync to all backup locations
    success_count = sync_to_backups(temp_file)

    # Cleanup
    os.remove(temp_file)
    logger.info("Temporary file removed")

    # Cleanup old backups
    cleanup_old_backups()

    # Summary
    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info("="*60)

    if success_count == len(BACKUP_LOCATIONS):
        logger.info(f"[SUCCESS] All {success_count} backup locations synced")
        logger.info(f"Time elapsed: {elapsed:.1f}s")
        logger.info("="*60)
        return True
    else:
        logger.error(f"[PARTIAL] Only {success_count}/{len(BACKUP_LOCATIONS)} backups synced")
        logger.info(f"Time elapsed: {elapsed:.1f}s")
        logger.info("="*60)
        return False

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)
