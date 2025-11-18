"""
System Cleanup Script
Archives old/duplicate files to avoid mixing versions

Moves files to D:/Max_EV_Sports/archive/
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Timestamp for archive folder
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
ARCHIVE_ROOT = Path('D:/Max_EV_Sports/archive') / f'cleanup_{TIMESTAMP}'
BACKEND_ROOT = Path('backend')

# Files to archive (not delete - keep for reference)
FILES_TO_ARCHIVE = {
    'Legacy Prediction Scripts': [
        'run_daily_predictions.py',
        'run_ncaab_predictions.py',
        'config.py',
        'config_calibrated.py',
    ],
    'Old Main Files': [
        'backend/main_updated.py',
        'backend/main_temp.py',
        'backend/main_prod.py',
        'backend/main_fixed.py',
    ],
    'Legacy Models': [
        'backend/models/nba/totals_predictor.py',
        'backend/models/ncaab/totals_predictor.py',
    ],
    'Test Scripts (Sample)': [
        # We'll move all test_*.py, check_*.py, debug_*.py files
    ],
    'Backup CSVs (Old)': [
        # We'll move .backup files older than 30 days
    ]
}

def create_archive_structure():
    """Create archive directory structure"""
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"Archive directory: {ARCHIVE_ROOT}")
    return ARCHIVE_ROOT

def archive_file(source: Path, category: str):
    """Move file to archive"""
    if not source.exists():
        print(f"  [SKIP] Not found: {source}")
        return False

    # Create category folder in archive
    dest_folder = ARCHIVE_ROOT / category
    dest_folder.mkdir(parents=True, exist_ok=True)

    # Move file
    dest = dest_folder / source.name
    try:
        shutil.move(str(source), str(dest))
        print(f"  [OK] Archived: {source.name} -> {category}/")
        return True
    except Exception as e:
        print(f"  [ERROR] Error archiving {source}: {e}")
        return False

def find_and_archive_pattern(pattern: str, category: str, max_files: int = 100):
    """Find files matching pattern and archive them"""
    files = list(BACKEND_ROOT.rglob(pattern))
    count = 0

    for file in files[:max_files]:
        if archive_file(file, category):
            count += 1

    return count

def archive_old_backups():
    """Archive .backup files older than 30 days"""
    tracking_dir = BACKEND_ROOT / 'data' / 'tracking'
    if not tracking_dir.exists():
        return 0

    count = 0
    for backup_file in tracking_dir.glob('*.backup*'):
        # Check age
        age_days = (datetime.now() - datetime.fromtimestamp(backup_file.stat().st_mtime)).days
        if age_days > 30:
            if archive_file(backup_file, 'Old_Backups'):
                count += 1

    return count

def archive_duplicate_nested_structure():
    """Archive the duplicate nested backend structure in scrapers/ncaab/nba/"""
    nested_backend = BACKEND_ROOT / 'scrapers' / 'ncaab' / 'nba' / 'backend'

    if nested_backend.exists():
        dest = ARCHIVE_ROOT / 'Duplicate_Nested_Structure' / 'nba_backend'
        dest.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.move(str(nested_backend), str(dest))
            print(f"  [OK] Archived: Duplicate nested backend structure")
            return 1
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            return 0

    return 0

def generate_cleanup_report():
    """Generate a report of what was archived"""
    report_path = ARCHIVE_ROOT / 'CLEANUP_REPORT.txt'

    with open(report_path, 'w') as f:
        f.write(f"MAX-EV SPORTS - CLEANUP REPORT\n")
        f.write(f"{'='*70}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Archive Location: {ARCHIVE_ROOT}\n")
        f.write(f"\n")
        f.write(f"Files archived to avoid version mixing and keep system clean.\n")
        f.write(f"All archived files are preserved and can be restored if needed.\n")
        f.write(f"\n")
        f.write(f"{'='*70}\n")
        f.write(f"ARCHIVED CATEGORIES:\n")
        f.write(f"{'='*70}\n")

        for category in ARCHIVE_ROOT.iterdir():
            if category.is_dir():
                files = list(category.rglob('*'))
                file_count = len([f for f in files if f.is_file()])
                f.write(f"\n{category.name}: {file_count} files\n")
                for file in files:
                    if file.is_file():
                        f.write(f"  - {file.name}\n")

    print(f"\nReport saved: {report_path}")

def main():
    """Run cleanup process"""
    print("\n" + "="*70)
    print("MAX-EV SPORTS - SYSTEM CLEANUP")
    print("="*70)
    print("\nGoal: Archive old files to avoid version mixing")
    print("All files will be moved to archive (not deleted)\n")

    archive_dir = create_archive_structure()

    total_archived = 0

    # 1. Archive legacy prediction scripts
    print("\n[1/6] Archiving Legacy Prediction Scripts...")
    for file in FILES_TO_ARCHIVE['Legacy Prediction Scripts']:
        if archive_file(Path(file), 'Legacy_Scripts'):
            total_archived += 1

    # 2. Archive old main files
    print("\n[2/6] Archiving Old Main Files...")
    for file in FILES_TO_ARCHIVE['Old Main Files']:
        if archive_file(Path(file), 'Old_Main_Files'):
            total_archived += 1

    # 3. Archive legacy models
    print("\n[3/6] Archiving Legacy Model Files...")
    for file in FILES_TO_ARCHIVE['Legacy Models']:
        if archive_file(Path(file), 'Legacy_Models'):
            total_archived += 1

    # 4. Archive test/debug/check scripts
    print("\n[4/6] Archiving Test/Debug Scripts...")
    total_archived += find_and_archive_pattern('test_*.py', 'Test_Scripts', max_files=50)
    total_archived += find_and_archive_pattern('check_*.py', 'Debug_Scripts', max_files=50)
    total_archived += find_and_archive_pattern('debug_*.py', 'Debug_Scripts', max_files=50)
    total_archived += find_and_archive_pattern('fix_*.py', 'Fix_Scripts', max_files=50)

    # 5. Archive old backup files
    print("\n[5/6] Archiving Old Backup Files (>30 days)...")
    total_archived += archive_old_backups()

    # 6. Archive duplicate nested structure
    print("\n[6/6] Archiving Duplicate Nested Structure...")
    total_archived += archive_duplicate_nested_structure()

    # Generate report
    generate_cleanup_report()

    print("\n" + "="*70)
    print(f"CLEANUP COMPLETE!")
    print(f"   Total files archived: {total_archived}")
    print(f"   Archive location: {archive_dir}")
    print("="*70)
    print("\nAll files are preserved in archive and can be restored if needed.")
    print("System is now clean with no version mixing!\n")

if __name__ == '__main__':
    main()
