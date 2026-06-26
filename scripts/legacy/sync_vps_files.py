#!/usr/bin/env python3
"""
Sync all recently modified files from VPS to local machine
"""
import subprocess
import os

# VPS connection
VPS_HOST = "root@148.230.87.135"
VPS_BASE = "/root/sporttrader"
LOCAL_BASE = r"C:\Users\nashr\max-ev-sports"

# List of all files modified in last 3 days (from find command)
FILES_TO_SYNC = [
    "./frontend/src/config.ts",
    "./backend/run_enhanced_predictions_all_sports.py",
    "./backend/routes/model_performance.py",
    "./backend/routes/ui_endpoints.py",
    "./backend/routes/predictions.py",
    "./backend/routes/ui_props.py",
    "./backend/routes/props_performance.py",
    "./backend/predict_nba_moneyline.py",
    "./backend/ml/pytorch_models/ensemble_weighter.py",
    "./backend/ml/pytorch_models/__init__.py",
    "./backend/ml/pytorch_models/catboost_model.py",
    "./backend/ml/pytorch_models/tabular_net.py",
    "./backend/ml/data_loaders/ncaab_data_loader.py",
    "./backend/ml/props/correlation_engine.py",
    "./backend/ml/props/stats_scraper_nhl_moneypuck.py",
    "./backend/ml/props/stats_scraper_nba_balldontlie.py",
    "./backend/ml/props/enhanced_feature_engineering_nhl.py",
    "./backend/ml/props/stats_scraper_nba_espn.py",
    "./backend/ml/props/stats_scraper_nfl.py",
    "./backend/ml/props/enhanced_feature_engineering_nfl.py",
    "./backend/ml/props/stats_scraper_nba.py",
    "./backend/ml/props/stats_scraper_nhl.py",
    "./backend/ml/props/run_all_stats_scrapers.py",
    "./backend/ml/props/predictor.py",
    "./backend/ml/props/setup_unified_schema.py",
    "./backend/ml/props/run_all_stats_scrapers_v2.py",
    "./backend/ml/props/enhanced_feature_engineering.py",
    "./backend/ml/feature_engineering/ncaaf_features.py",
    "./backend/ml/feature_engineering/nba_features.py",
    "./backend/ml/feature_engineering/nfl_features.py",
    "./backend/ml/feature_engineering/ncaab_features.py",
    "./backend/ml/feature_engineering/nhl_features.py",
    "./backend/ml/training/train_nba_enhanced.py",
    "./backend/ml/training/enhanced_multi_model_trainer.py",
    "./backend/ml/training/train_all_enhanced.py",
    "./backend/ml/training/train_from_db_universal.py",
    "./backend/ml/predictions/daily_props_predictor_fast.py",
    "./backend/ml/dfs/correlation_engine.py",
    "./backend/ml/dfs/generate_dfs_crusher_from_db.py",
    "./backend/ml/dfs/dfs_scanner.py",
    "./backend/ml/dfs/scrapers/odds_api_dfs.py",
    "./backend/ml/dfs/scrapers/sleeper.py",
    "./backend/ml/dfs/scrapers/underdog.py",
    "./backend/ml/dfs/scrapers/__init__.py",
    "./backend/ml/dfs/scrapers/fliff.py",
    "./backend/ml/dfs/scrapers/parlayplay.py",
    "./backend/ml/dfs/scrapers/prizepicks.py",
    "./backend/predict_nfl_moneyline.py",
    "./backend/test_enhanced_training.py",
    "./backend/predict_nhl_spreads.py",
    "./backend/run_multi_sport_props.py",
    "./backend/run_all_predictions.py",
    "./backend/run_ENHANCED_ML.py",
    "./backend/add_market_lines_to_training_v2.py",
    "./backend/run_ml_predictions_all_sports_v2.py",
    "./backend/daily_systems_check.py",
    "./backend/predict_nba_spreads.py",
    "./backend/predict_ncaaf_moneyline.py",
    "./backend/predict_ncaab_totals.py",
    "./backend/generate_scripts.py",
    "./backend/run_ml_predictions_ALL_BET_TYPES_BACKUP_1764771571.py",
    "./backend/run_ml_predictions_to_db.py",
    "./backend/run_ml_predictions_ALL_BET_TYPES_BROKEN_1764772060.py",
    "./backend/run_ENHANCED_predictions.py",
    "./backend/train_all_105_models.py",
    "./backend/predict_nhl_totals.py",
    "./backend/generate_all_predictions_multi_bet.py",
    "./backend/run_ml_predictions_ALL_BET_TYPES_BEFORE_MARKET_FIX.py",
    "./backend/run_ml_predictions_all_sports.py",
    "./backend/run_ml_predictions_ALL_BET_TYPES_FIXED.py",
    "./backend/run_kenpom_fallback.py",
    "./backend/run_ml_predictions_ALL_BET_TYPES.py",
    "./backend/train_all_105_models_fixed.py",
    "./backend/run_props_fast.py",
    "./backend/add_market_lines_to_training.py",
    "./backend/fetch_nhl_team_stats_now.py",
    "./backend/main.py",
    "./backend/daily_systems_check_ORIGINAL.py",
    "./backend/nhl_stats_client.py",
    "./backend/run_barttorvik_scraper.py",
    "./backend/scrapers/espn_nhl_scraper.py",
    "./backend/scrapers/ncaab/barttorvik_scraper.py",
    "./backend/scrapers/props/results_tracker_fixed.py",
    "./backend/scrapers/props/results_tracker.py",
    "./backend/scrapers/props/balldontlie_client.py",
    "./backend/scrapers/nhl/espn_nhl_team_stats.py",
    "./backend/scrapers/nhl/espn_nhl_team_stats_fixed.py",
    "./backend/predict_nfl_spreads.py",
    "./backend/comprehensive_daily_systems_check.py",
    "./backend/predict_nba_totals.py",
    "./backend/grade_predictions_db.py",
    "./backend/predict_ncaaf_spreads.py",
    "./backend/predict_nfl_totals.py",
    "./backend/predict_nhl_moneyline.py",
    "./backend/run_ml_predictions_ALL_BET_TYPES_OLD.py",
    "./backend/predict_ncaaf_totals.py",
    "./backend/train_all_models_individually.py",
    "./backend/run_complete_predictions_ALL_MODELS.py",
    "./backend/run_ml_predictions_all_sports_ENHANCED.py",
]

# All databases to sync
DATABASES = [
    "backend/ml/predictions.db",
    "backend/settings.db",
    "backend/users.db",
    "backend/subscriptions.db",
    "backend/sporttrader.db",
    "backend/user_settings.db",
    "backend/ml_predictions.db",
    "backend/sportstrader.db",
    "backend/nba_props.db",
    "backend/fade_positions.db",
    "backend/plays_tracking.db",
    "backend/database/sports_betting.db",
    "backend/database/users.db",
    "backend/database/backtests.db",
    "backend/database/subscriptions.db",
    "backend/data/fade_pregame_odds.db",
]

def download_file(vps_file, local_file):
    """Download a single file using scp"""
    vps_path = f"{VPS_HOST}:{VPS_BASE}/{vps_file}"
    local_path = os.path.join(LOCAL_BASE, local_file.replace("./", ""))

    # Create directory if needed
    local_dir = os.path.dirname(local_path)
    os.makedirs(local_dir, exist_ok=True)

    # Download file
    cmd = ["scp", vps_path, local_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("SYNCING VPS TO LOCAL MACHINE")
    print("=" * 70)

    # Download all modified files
    print(f"\n[1/2] Downloading {len(FILES_TO_SYNC)} recently modified files...")
    success_count = 0
    failed_files = []

    for i, file_path in enumerate(FILES_TO_SYNC, 1):
        success, error = download_file(file_path, file_path)
        if success:
            success_count += 1
            print(f"  [{i}/{len(FILES_TO_SYNC)}] OK {file_path}")
        else:
            failed_files.append((file_path, error))
            print(f"  [{i}/{len(FILES_TO_SYNC)}] FAIL {file_path} - {error}")

    print(f"\nFiles synced: {success_count}/{len(FILES_TO_SYNC)}")

    # Download all databases
    print(f"\n[2/2] Downloading {len(DATABASES)} databases...")
    db_success = 0
    failed_dbs = []

    for i, db_path in enumerate(DATABASES, 1):
        success, error = download_file(db_path, db_path)
        if success:
            db_success += 1
            print(f"  [{i}/{len(DATABASES)}] OK {db_path}")
        else:
            failed_dbs.append((db_path, error))
            print(f"  [{i}/{len(DATABASES)}] FAIL {db_path} - {error}")

    print(f"\nDatabases synced: {db_success}/{len(DATABASES)}")

    # Summary
    print("\n" + "=" * 70)
    print("SYNC COMPLETE")
    print("=" * 70)
    print(f"Total files synced: {success_count + db_success}/{len(FILES_TO_SYNC) + len(DATABASES)}")

    if failed_files or failed_dbs:
        print(f"\n⚠ Failed: {len(failed_files) + len(failed_dbs)} items")
        if failed_files:
            print("\nFailed files:")
            for f, e in failed_files[:5]:  # Show first 5
                print(f"  - {f}")
        if failed_dbs:
            print("\nFailed databases:")
            for f, e in failed_dbs:
                print(f"  - {f}")
    else:
        print("\nAll files and databases synced successfully!")

if __name__ == "__main__":
    main()
