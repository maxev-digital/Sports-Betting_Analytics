#!/usr/bin/env python3
"""
Train ALL 105 Models from Database
7 model types × 3 bet types × 5 sports = 105 total models
"""
import sqlite3
import pandas as pd
import numpy as np
import joblib
import torch
import torch.nn as nn
from pathlib import Path
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, accuracy_score
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor, CatBoostClassifier
import sys
sys.path.append('/root/sporttrader/backend')
from ml.pytorch_models.tabular_net import TabularNetTrainer
from ml.pytorch_models.ensemble_weighter import EnsembleWeighter
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = '/root/sporttrader/backend/ml/predictions.db'
MODEL_DIR = Path('/root/sporttrader/backend/ml/models')

def train_sport_models(sport: str):
    """Train all 21 models for a sport (7 types × 3 bet types)"""
    logger.info('='*70)
    logger.info(f'TRAINING {sport.upper()} - 21 MODELS')
    logger.info('='*70)

    # Load data from database
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f'SELECT * FROM {sport}_training_data', conn)
    conn.close()

    logger.info(f'Loaded {len(df):,} games from database')

    if len(df) < 100:
        logger.warning(f'Not enough data for {sport} (need at least 100 games)')
        return

    # Get feature columns
    feature_cols = [c for c in df.columns if ('home_' in c or 'away_' in c)
                    and c not in ['home_score', 'away_score', 'home_win', 'home_margin']]

    logger.info(f'Using {len(feature_cols)} features')

    bet_types = ['totals', 'spreads', 'moneyline']

    for bet_type in bet_types:
        logger.info(f'\nTraining {bet_type}...')

        X = df[feature_cols].values

        # Set target variable
        if bet_type == 'totals':
            y = df['total'].values
            is_classifier = False
        elif bet_type == 'spreads':
            y = df['home_margin'].values
            is_classifier = False
        else:  # moneyline
            y = df['home_win'].values
            is_classifier = True

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        models = {}
        predictions = {}

        # 1. Random Forest
        logger.info(f'  Training Random Forest...')
        if is_classifier:
            models['random_forest'] = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        else:
            models['random_forest'] = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        models['random_forest'].fit(X_train, y_train)
        predictions['random_forest'] = models['random_forest'].predict(X_test)

        # 2. XGBoost
        logger.info(f'  Training XGBoost...')
        if is_classifier:
            models['xgboost'] = xgb.XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        else:
            models['xgboost'] = xgb.XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        models['xgboost'].fit(X_train, y_train)
        predictions['xgboost'] = models['xgboost'].predict(X_test)

        # 3. LightGBM
        logger.info(f'  Training LightGBM...')
        if is_classifier:
            models['lightgbm'] = lgb.LGBMClassifier(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1)
        else:
            models['lightgbm'] = lgb.LGBMRegressor(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1)
        models['lightgbm'].fit(X_train, y_train)
        predictions['lightgbm'] = models['lightgbm'].predict(X_test)

        # 4. Linear/Logistic Regression
        logger.info(f'  Training Linear Regression...')
        if is_classifier:
            models['linear'] = LogisticRegression(random_state=42, max_iter=1000)
        else:
            models['linear'] = LinearRegression()
        models['linear'].fit(X_train, y_train)
        predictions['linear'] = models['linear'].predict(X_test)

        # 5. CatBoost
        logger.info(f'  Training CatBoost...')
        if is_classifier:
            models['catboost'] = CatBoostClassifier(iterations=100, random_state=42, verbose=0)
        else:
            models['catboost'] = CatBoostRegressor(iterations=100, random_state=42, verbose=0)
        models['catboost'].fit(X_train, y_train)
        predictions['catboost'] = models['catboost'].predict(X_test)

        # 6. PyTorch TabularNet
        logger.info(f'  Training PyTorch TabularNet...')
        pytorch_trainer = TabularNetTrainer(input_dim=X_train.shape[1])
        pytorch_trainer.train(X_train, y_train, epochs=50)
        predictions['pytorch'] = pytorch_trainer.predict(X_test)
        models['pytorch'] = pytorch_trainer

        # 7. Neural Ensemble
        logger.info(f'  Training Neural Ensemble...')
        base_preds = np.column_stack([
            predictions['random_forest'],
            predictions['xgboost'],
            predictions['lightgbm'],
            predictions['linear'],
            predictions['catboost'],
            predictions['pytorch']
        ])

        ensemble = EnsembleWeighter(n_models=6)
        X_tensor = torch.FloatTensor(base_preds)
        n_models = base_preds.shape[1]
        model_accs = torch.ones_like(X_tensor) / n_models
        y_tensor = torch.FloatTensor(y_test)
        optimizer = torch.optim.Adam(ensemble.parameters(), lr=0.01)

        for epoch in range(50):
            optimizer.zero_grad()
            preds, _ = ensemble(X_tensor, model_accs)
            if is_classifier:
                loss = nn.BCEWithLogitsLoss()(preds, y_tensor)
            else:
                loss = nn.MSELoss()(preds, y_tensor)
            loss.backward()
            optimizer.step()

        with torch.no_grad():
            final_preds, _ = ensemble(X_tensor, model_accs)
            predictions['ensemble'] = final_preds.numpy()

        models['ensemble'] = ensemble

        # Calculate performance
        if is_classifier:
            for name in predictions:
                preds = predictions[name]
                if len(preds.shape) > 1:
                    preds = preds.flatten()
                preds = (preds > 0.5).astype(int) if name == 'ensemble' else preds
                acc = accuracy_score(y_test, preds)
                logger.info(f'    {name}: Accuracy={acc:.3f}')
        else:
            for name in predictions:
                mae = mean_absolute_error(y_test, predictions[name])
                logger.info(f'    {name}: MAE={mae:.3f}')

        # Save all models
        logger.info(f'  Saving models...')
        for name, model in models.items():
            if name == 'pytorch':
                torch.save(model.model.state_dict(), MODEL_DIR / f'{sport}_pytorch_{bet_type}_latest.pt')
            elif name == 'ensemble':
                torch.save(model.state_dict(), MODEL_DIR / f'{sport}_ensemble_{bet_type}_latest.pt')
            elif name == 'catboost':
                model.save_model(str(MODEL_DIR / f'{sport}_catboost_{bet_type}_enhanced.joblib'))
            else:
                joblib.dump(model, MODEL_DIR / f'{sport}_{name}_{bet_type}_enhanced.joblib')

        # Save scaler
        joblib.dump(scaler, MODEL_DIR / f'{sport}_scaler_{bet_type}_enhanced.joblib')

        logger.info(f'  ✓ Completed {sport} {bet_type} - 7 models saved')

def main():
    logger.info('')
    logger.info('='*70)
    logger.info('TRAINING ALL 105 MODELS FROM DATABASE')
    logger.info('7 model types × 3 bet types × 5 sports = 105 total models')
    logger.info('='*70)
    logger.info('')

    sports = ['nba', 'ncaab', 'nhl', 'nfl', 'ncaaf']

    for sport in sports:
        try:
            train_sport_models(sport)
        except Exception as e:
            logger.error(f'Error training {sport}: {e}', exc_info=True)
            continue

    # Count final models
    logger.info('')
    logger.info('='*70)
    logger.info('TRAINING COMPLETE')
    logger.info('='*70)

    total_models = 0
    for sport in sports:
        sport_models = list(MODEL_DIR.glob(f'{sport}_*_enhanced.joblib')) + list(MODEL_DIR.glob(f'{sport}_*_latest.pt'))
        count = len(sport_models)
        total_models += count
        logger.info(f'{sport.upper()}: {count} models')

    logger.info(f'\nTOTAL MODELS: {total_models}')
    logger.info('Expected: 105 (21 per sport × 5 sports)')

if __name__ == '__main__':
    main()
