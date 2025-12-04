#!/usr/bin/bash
# TRAIN_NOW.sh
# Train all 5 sports with enhanced 7-model architecture
# Run this to complete the full deployment

set -e

echo "=========================================="
echo "TRAINING ALL SPORTS - ENHANCED 7-MODEL SYSTEM"
echo "=========================================="
echo "This will train:"
echo "  - NBA (7 models)"
echo "  - NCAAB (7 models)"
echo "  - NHL (7 models)"
echo "  - NFL (7 models)"
echo "  - NCAAF (7 models)"
echo ""
echo "Total: 35 models (7 per sport)"
echo "Estimated time: 30-60 minutes"
echo "=========================================="
echo ""

VPS_HOST="root@148.230.87.135"
VPS_DIR="/root/sporttrader/backend"

# First, let's check what data we have
echo "[Pre-check] Verifying data availability..."
ssh $VPS_HOST "ls -lh $VPS_DIR/data/raw/nba/ | head -5"
ssh $VPS_HOST "ls -lh $VPS_DIR/data/raw/ncaab/ | head -5"

echo ""
echo "Starting training in 5 seconds... (Ctrl+C to cancel)"
sleep 5

# Train NBA
echo ""
echo "========================================"
echo "[1/5] Training NBA with 7 models..."
echo "========================================"
ssh $VPS_HOST "cd $VPS_DIR && source venv/bin/activate && python3 << 'PYEOF'
import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.append('/root/sporttrader/backend')

from ml.training.enhanced_multi_model_trainer import EnhancedMultiModelTrainer
from ml.data_loaders.nba_data_loader import load_nba_training_data

print('Loading NBA training data...')
df = load_nba_training_data()

if df.empty:
    print('ERROR: No NBA training data found!')
    sys.exit(1)

print(f'Data loaded: {len(df)} games')

# Prepare X and y from DataFrame
# Remove non-numeric columns and target variable
exclude_cols = ['actual_total', 'game_id', 'date', 'season', 'home_team', 'away_team', 'game_date', 'timestamp']
feature_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
X_train = df[feature_cols].values
y_train = df['actual_total'].values if 'actual_total' in df.columns else df.iloc[:, -1].values

print(f'Features: {X_train.shape[1]}, Samples: {len(X_train)}')

print('Training all 7 models for NBA...')
trainer = EnhancedMultiModelTrainer(sport='nba', bet_type='totals')
models = trainer.train_all_models(X_train, y_train)

print(f'NBA COMPLETE: {len(models)} models trained')
PYEOF
"

# Train NCAAB
echo ""
echo "========================================"
echo "[2/5] Training NCAAB with 7 models..."
echo "========================================"
ssh $VPS_HOST "cd $VPS_DIR && source venv/bin/activate && python3 << 'PYEOF'
import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.append('/root/sporttrader/backend')

from ml.training.enhanced_multi_model_trainer import EnhancedMultiModelTrainer
from ml.data_loaders.ncaab_data_loader import load_ncaab_training_data

print('Loading NCAAB training data...')
df = load_ncaab_training_data()

if df.empty:
    print('WARNING: No NCAAB training data found - skipping')
    import sys
    sys.exit(0)

print(f'Data loaded: {len(df)} games')

# Prepare X and y from DataFrame
# Remove non-numeric columns and target variable
exclude_cols = ['actual_total', 'game_id', 'date', 'season', 'home_team', 'away_team', 'game_date', 'timestamp']
feature_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
X_train = df[feature_cols].values
y_train = df['actual_total'].values if 'actual_total' in df.columns else df.iloc[:, -1].values

print(f'Features: {X_train.shape[1]}, Samples: {len(X_train)}')

print('Training all 7 models for NCAAB...')
trainer = EnhancedMultiModelTrainer(sport='ncaab', bet_type='totals')
models = trainer.train_all_models(X_train, y_train)

print(f'NCAAB COMPLETE: {len(models)} models trained')
PYEOF
"

# Train NHL
echo ""
echo "========================================"
echo "[3/5] Training NHL with 7 models..."
echo "========================================"
ssh $VPS_HOST "cd $VPS_DIR && source venv/bin/activate && python3 << 'PYEOF'
import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.append('/root/sporttrader/backend')

from ml.training.enhanced_multi_model_trainer import EnhancedMultiModelTrainer

print('Loading NHL training data...')
# Check if NHL data loader exists
try:
    from ml.data_loaders.nhl_data_loader import load_nhl_training_data
    df = load_nhl_training_data()
except ImportError:
    print('WARNING: NHL data loader not found - skipping')
    sys.exit(0)

if df.empty:
    print('WARNING: No NHL training data found - skipping')
    sys.exit(0)

print(f'Data loaded: {len(df)} games')

# Prepare X and y from DataFrame
exclude_cols = ['actual_total', 'game_id', 'date', 'season', 'home_team', 'away_team', 'game_date', 'timestamp']
feature_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
X_train = df[feature_cols].values
y_train = df['actual_total'].values if 'actual_total' in df.columns else df.iloc[:, -1].values

print(f'Features: {X_train.shape[1]}, Samples: {len(X_train)}')

print('Training all 7 models for NHL...')
trainer = EnhancedMultiModelTrainer(sport='nhl', bet_type='totals')
models = trainer.train_all_models(X_train, y_train)

print(f'NHL COMPLETE: {len(models)} models trained')
PYEOF
"

# Train NFL
echo ""
echo "========================================"
echo "[4/5] Training NFL with 7 models..."
echo "========================================"
ssh $VPS_HOST "cd $VPS_DIR && source venv/bin/activate && python3 << 'PYEOF'
import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.append('/root/sporttrader/backend')

from ml.training.enhanced_multi_model_trainer import EnhancedMultiModelTrainer

print('Loading NFL training data...')
# Check if NFL data loader exists
try:
    from ml.data_loaders.nfl_data_loader import load_nfl_training_data
    df = load_nfl_training_data()
except ImportError:
    print('WARNING: NFL data loader not found - skipping')
    sys.exit(0)

if df.empty:
    print('WARNING: No NFL training data found - skipping')
    sys.exit(0)

print(f'Data loaded: {len(df)} games')

# Prepare X and y from DataFrame
exclude_cols = ['actual_total', 'game_id', 'date', 'season', 'home_team', 'away_team', 'game_date', 'timestamp']
feature_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
X_train = df[feature_cols].values
y_train = df['actual_total'].values if 'actual_total' in df.columns else df.iloc[:, -1].values

print(f'Features: {X_train.shape[1]}, Samples: {len(X_train)}')

print('Training all 7 models for NFL...')
trainer = EnhancedMultiModelTrainer(sport='nfl', bet_type='totals')
models = trainer.train_all_models(X_train, y_train)

print(f'NFL COMPLETE: {len(models)} models trained')
PYEOF
"

# Train NCAAF
echo ""
echo "========================================"
echo "[5/5] Training NCAAF with 7 models..."
echo "========================================"
ssh $VPS_HOST "cd $VPS_DIR && source venv/bin/activate && python3 << 'PYEOF'
import sys
import numpy as np
import pandas as pd
from pathlib import Path
sys.path.append('/root/sporttrader/backend')

from ml.training.enhanced_multi_model_trainer import EnhancedMultiModelTrainer

print('Loading NCAAF training data...')
# Check if NCAAF data loader exists
try:
    from ml.data_loaders.ncaaf_data_loader import load_ncaaf_training_data
    df = load_ncaaf_training_data()
except ImportError:
    print('WARNING: NCAAF data loader not found - skipping')
    sys.exit(0)

if df.empty:
    print('WARNING: No NCAAF training data found - skipping')
    sys.exit(0)

print(f'Data loaded: {len(df)} games')

# Prepare X and y from DataFrame
exclude_cols = ['actual_total', 'game_id', 'date', 'season', 'home_team', 'away_team', 'game_date', 'timestamp']
feature_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
X_train = df[feature_cols].values
y_train = df['actual_total'].values if 'actual_total' in df.columns else df.iloc[:, -1].values

print(f'Features: {X_train.shape[1]}, Samples: {len(X_train)}')

print('Training all 7 models for NCAAF...')
trainer = EnhancedMultiModelTrainer(sport='ncaaf', bet_type='totals')
models = trainer.train_all_models(X_train, y_train)

print(f'NCAAF COMPLETE: {len(models)} models trained')
PYEOF
"

echo ""
echo "=========================================="
echo "TRAINING COMPLETE!"
echo "=========================================="
echo ""
echo "Models created:"
ssh $VPS_HOST "ls -lh $VPS_DIR/ml/models/*_pytorch_* 2>/dev/null | wc -l || echo '0'" | xargs echo "  PyTorch models:"
ssh $VPS_HOST "ls -lh $VPS_DIR/ml/models/*.cbm 2>/dev/null | wc -l || echo '0'" | xargs echo "  CatBoost models:"
ssh $VPS_HOST "ls -lh $VPS_DIR/ml/models/*_neural_ensemble_* 2>/dev/null | wc -l || echo '0'" | xargs echo "  Ensemble models:"

echo ""
echo "Next steps:"
echo "  1. Verify models exist: ssh root@148.230.87.135 'ls -lh /root/sporttrader/backend/ml/models/*.pt'"
echo "  2. Update prediction scripts to use 7 models"
echo "  3. Test predictions with new models"
echo ""
echo "=========================================="
