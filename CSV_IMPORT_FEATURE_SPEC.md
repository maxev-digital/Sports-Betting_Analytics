# BET HISTORY CSV IMPORT FEATURE SPECIFICATION

**Feature:** Allow users to upload existing bet history CSV files
**Priority:** High - Removes friction for new users with existing tracking systems
**Target Release:** Q1 2026 (Post-Launch Enhancement)

---

## 📋 Feature Overview

### User Story
"As a new user with existing bet tracking data, I want to upload my historical bets so that I can have complete betting history in one place without manual re-entry."

### Business Value
- **Reduces onboarding friction** - Users don't lose historical data
- **Increases conversions** - Easier to switch platforms
- **Improves engagement** - Complete data = better insights
- **Competitive advantage** - Most platforms don't offer this

---

## 🎯 Functional Requirements

### 1. File Upload Interface

**Location:** User Settings → Bet History → Import CSV

**Upload Component:**
- Drag-and-drop file area
- File browser button
- File type validation (CSV, XLS, XLSX)
- File size limit: 10MB max (~50,000 bets)
- Preview before import (first 10 rows)
- Column mapping interface
- Progress indicator during upload

### 2. Supported CSV Formats

#### Standard Format (Priority 1)
```csv
Date,Sport,Bet Type,Team/Player,Odds,Stake,Result,Profit/Loss,Sportsbook
2025-11-01,NBA,Spread,Lakers -5.5,-110,100,Win,90.91,DraftKings
2025-11-02,NFL,Total,Over 47.5,-105,50,Loss,-50.00,FanDuel
2025-11-03,NHL,Moneyline,Bruins ML,+150,75,Win,112.50,BetMGM
```

#### Action Network Export (Priority 1)
```csv
Date,League,Type,Pick,Line,Units,Result,Net Profit,Book
11/1/2025,NBA,Spread,LAL -5.5,-110,1,W,+0.91,DraftKings
```

#### Pikkit Export (Priority 2)
```csv
Placed Date,Sport,Market Type,Selection,American Odds,Stake,Status,Payout,Bookmaker
2025-11-01,Basketball,Point Spread,Los Angeles Lakers -5.5,-110,$100.00,Won,$190.91,DraftKings
```

#### Custom/Generic Format (Priority 2)
- Flexible column mapping
- User defines which column = which field
- Save mapping templates for reuse

### 3. Required Data Fields

**Mandatory Fields:**
- Date/Time
- Sport
- Bet amount/stake
- Odds
- Result (Win/Loss/Push/Pending)

**Optional Fields:**
- Sportsbook name
- Bet type (Spread/Total/Moneyline/Props)
- Team/Player name
- Profit/Loss amount
- Notes/Tags

**Auto-Generated Fields:**
- Import date
- Import batch ID
- User ID

### 4. Data Validation & Parsing

**Date Parsing:**
- Support multiple formats: MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD
- Auto-detect format from first 5 rows
- Allow user to specify if ambiguous

**Sport Mapping:**
- Map variations: "NBA" / "Basketball" / "basketball_nba" → NBA
- Support abbreviations and full names
- Show unmatched sports for manual mapping

**Odds Format Conversion:**
- American: -110, +150
- Decimal: 1.91, 2.50
- Fractional: 10/11, 3/2
- Auto-convert to American (platform standard)

**Result Parsing:**
- Variations: W/L/P, Win/Loss/Push, Won/Lost, 1/0/-1
- Case-insensitive
- Default pending if unclear

**Currency:**
- Strip $ signs and commas
- Support multiple currencies (convert to USD)
- Detect from column or ask user

### 5. Column Mapping Interface

**Smart Auto-Mapping:**
- Analyze column headers
- Match to known patterns
- Confidence score for each match

**Manual Mapping UI:**
```
CSV Column          →    Platform Field
─────────────────────────────────────────
[Date]              →    [Bet Date ▼]
[League]            →    [Sport ▼]
[Type]              →    [Bet Type ▼]
[Pick]              →    [Selection ▼]
[Line]              →    [Odds ▼]
[Units]             →    [Stake ▼]
[Result]            →    [Result ▼]
[Book]              →    [Sportsbook ▼]
[Net Profit]        →    [Profit/Loss ▼]
```

**Features:**
- Dropdown selection for each field
- "Skip this column" option
- Preview transformed data
- Save mapping template

### 6. Import Processing

**Backend Processing Flow:**
1. Receive CSV file
2. Parse into pandas DataFrame
3. Validate required fields
4. Map columns
5. Normalize data (dates, odds, sports)
6. Detect duplicates (date + selection + stake match)
7. Calculate missing fields (profit if result + odds present)
8. Assign to user account
9. Update user statistics
10. Return import summary

**Duplicate Detection:**
- Check against existing bets
- Match criteria: Date, Selection, Stake, Odds (within 5 points)
- User options:
  - Skip duplicates (default)
  - Import all (create duplicates)
  - Merge/Update existing

**Batch Processing:**
- Process in chunks of 1,000 bets
- Background job for large files
- Real-time progress updates via WebSocket

### 7. Import Summary & Review

**Summary Display:**
```
✅ Import Completed Successfully

📊 Summary:
- Total Rows: 1,247
- Successfully Imported: 1,189
- Duplicates Skipped: 52
- Errors: 6

📈 Stats Updated:
- Total Bets: 1,189 new
- Win/Loss Record: 657-498-34 (W-L-P)
- Total Wagered: $118,900
- Total Profit: +$8,456
- ROI: +7.1%

❌ Errors (6 bets):
Row 45: Invalid date format
Row 203: Unrecognized sport "ESports"
Row 556: Missing odds
Row 891: Invalid result value
Row 1100: Negative stake amount
Row 1238: Missing date

[Download Error Report] [View Imported Bets]
```

**Post-Import Actions:**
- Download error report CSV
- View newly imported bets
- Edit/fix errored rows manually
- Re-import with corrections

---

## 🎨 UI/UX Design

### Import Page Layout

```
┌─────────────────────────────────────────────┐
│  Import Bet History                          │
│                                               │
│  ┌───────────────────────────────────────┐  │
│  │                                         │  │
│  │       📁 Drag & Drop CSV File Here     │  │
│  │           or click to browse           │  │
│  │                                         │  │
│  │   Supported: CSV, XLS, XLSX (Max 10MB)│  │
│  └───────────────────────────────────────┘  │
│                                               │
│  ⚙️ Quick Import Presets:                    │
│  [ Action Network ] [ Pikkit ] [ Custom ]    │
│                                               │
│  📚 Import History:                           │
│  • Nov 11, 2025 - 1,189 bets (Action Network)│
│  • Oct 5, 2025 - 523 bets (Custom CSV)       │
│                                               │
│  ❓ Need Help? [View Import Guide]           │
└─────────────────────────────────────────────┘
```

### Column Mapping Step

```
┌─────────────────────────────────────────────┐
│  Step 2: Map CSV Columns                     │
│                                               │
│  File: my_bets_2025.csv (1,247 rows)        │
│                                               │
│  CSV Column        →  Platform Field         │
│  ─────────────────────────────────────────  │
│  Date              →  [Bet Date ▼]          │
│  League            →  [Sport ▼]             │
│  Type              →  [Bet Type ▼]          │
│  Pick              →  [Selection ▼]         │
│  Line              →  [Odds ▼]              │
│  Units             →  [Stake ▼]             │
│  Result            →  [Result ▼]            │
│  Book              →  [Sportsbook ▼]        │
│  Net Profit        →  [Profit/Loss ▼]      │
│                                               │
│  ⚡ Auto-mapped with 95% confidence          │
│  💾 [Save as Template]                       │
│                                               │
│  [← Back]              [Preview →]           │
└─────────────────────────────────────────────┘
```

### Preview & Confirm Step

```
┌─────────────────────────────────────────────┐
│  Step 3: Preview & Confirm                   │
│                                               │
│  Showing first 10 of 1,247 bets:            │
│                                               │
│  Date      Sport  Type    Selection    Odds │
│  ──────────────────────────────────────────│
│  11/1/25   NBA    Spread  Lakers -5.5  -110 │
│  11/1/25   NFL    Total   Over 47.5    -105 │
│  11/2/25   NHL    ML      Bruins ML    +150 │
│  ...                                          │
│                                               │
│  ⚠️ Detected Issues:                         │
│  • 6 rows have errors (will be skipped)     │
│  • 52 potential duplicates found            │
│                                               │
│  Duplicate Handling:                         │
│  ○ Skip duplicates (recommended)             │
│  ○ Import all                                │
│                                               │
│  [← Back]         [Import 1,189 Bets →]     │
└─────────────────────────────────────────────┘
```

---

## 🔧 Technical Implementation

### Backend API Endpoints

#### 1. Upload CSV File
```python
POST /api/user/bet-history/import/upload
Content-Type: multipart/form-data

Request:
- file: CSV/XLS/XLSX file
- mapping_template_id: (optional) saved template

Response:
{
  "upload_id": "uuid",
  "filename": "my_bets.csv",
  "rows": 1247,
  "columns": ["Date", "League", "Type", "Pick", ...],
  "preview": [...first 10 rows...],
  "auto_mapping": {
    "Date": "bet_date",
    "League": "sport",
    ...
  },
  "confidence": 0.95
}
```

#### 2. Confirm Mapping
```python
POST /api/user/bet-history/import/map
Content-Type: application/json

Request:
{
  "upload_id": "uuid",
  "column_mapping": {
    "Date": "bet_date",
    "League": "sport",
    ...
  },
  "duplicate_handling": "skip",
  "save_template": true,
  "template_name": "Action Network Format"
}

Response:
{
  "job_id": "uuid",
  "status": "processing",
  "estimated_time": 30  // seconds
}
```

#### 3. Check Import Status
```python
GET /api/user/bet-history/import/status/{job_id}

Response:
{
  "status": "completed",
  "progress": 100,
  "rows_processed": 1247,
  "imported": 1189,
  "duplicates_skipped": 52,
  "errors": 6,
  "error_details": [...],
  "stats_update": {
    "total_bets": 1189,
    "total_wagered": 118900,
    "total_profit": 8456,
    "roi": 0.071
  }
}
```

#### 4. Get Import History
```python
GET /api/user/bet-history/imports

Response:
{
  "imports": [
    {
      "id": "uuid",
      "filename": "my_bets.csv",
      "imported_at": "2025-11-11T10:30:00Z",
      "rows_imported": 1189,
      "template_used": "Action Network"
    },
    ...
  ]
}
```

#### 5. Mapping Templates
```python
GET /api/user/bet-history/import/templates
POST /api/user/bet-history/import/templates
DELETE /api/user/bet-history/import/templates/{id}
```

### Database Schema

#### imports_history Table
```sql
CREATE TABLE imports_history (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    filename VARCHAR(255),
    upload_date TIMESTAMP,
    rows_total INT,
    rows_imported INT,
    rows_skipped INT,
    rows_errors INT,
    template_used VARCHAR(100),
    status VARCHAR(50),  -- processing, completed, failed
    error_log TEXT
);
```

#### mapping_templates Table
```sql
CREATE TABLE mapping_templates (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(100),
    column_mapping JSONB,
    created_at TIMESTAMP,
    is_public BOOLEAN DEFAULT FALSE
);
```

### Python Implementation

```python
# backend/routes/bet_import.py

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
import uuid

class BetHistoryImporter:

    def __init__(self, user_id: str):
        self.user_id = user_id

    def parse_csv(self, file_path: str) -> pd.DataFrame:
        """Parse CSV with flexible encoding detection"""
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='latin-1')
        return df

    def auto_map_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Intelligently map CSV columns to platform fields"""

        column_patterns = {
            'bet_date': ['date', 'placed date', 'bet date', 'datetime'],
            'sport': ['sport', 'league', 'game type'],
            'bet_type': ['type', 'market type', 'bet type'],
            'selection': ['pick', 'selection', 'team', 'player'],
            'odds': ['odds', 'line', 'price', 'american odds'],
            'stake': ['stake', 'units', 'amount', 'wager'],
            'result': ['result', 'status', 'outcome'],
            'sportsbook': ['book', 'bookmaker', 'sportsbook'],
            'profit_loss': ['profit', 'net profit', 'p/l', 'payout']
        }

        mapping = {}
        confidence = 0

        for csv_col in df.columns:
            csv_col_lower = csv_col.lower().strip()
            for field, patterns in column_patterns.items():
                if any(pattern in csv_col_lower for pattern in patterns):
                    mapping[csv_col] = field
                    confidence += 1
                    break

        confidence_score = confidence / len(column_patterns)
        return mapping, confidence_score

    def normalize_sport(self, sport_str: str) -> str:
        """Normalize sport names"""
        sport_mapping = {
            'nba': 'NBA',
            'basketball': 'NBA',
            'basketball_nba': 'NBA',
            'nfl': 'NFL',
            'football': 'NFL',
            'americanfootball_nfl': 'NFL',
            'nhl': 'NHL',
            'hockey': 'NHL',
            'icehockey_nhl': 'NHL',
            # ... more mappings
        }
        return sport_mapping.get(sport_str.lower().strip(), sport_str)

    def parse_odds(self, odds_str: str) -> int:
        """Convert odds to American format"""
        if isinstance(odds_str, (int, float)):
            return int(odds_str)

        # American (-110, +150)
        if '+' in str(odds_str) or '-' in str(odds_str):
            return int(odds_str.replace('+', ''))

        # Decimal (1.91, 2.50)
        try:
            decimal = float(odds_str)
            if decimal >= 2.0:
                return int((decimal - 1) * 100)
            else:
                return int(-100 / (decimal - 1))
        except:
            pass

        # Fractional (10/11, 3/2)
        if '/' in str(odds_str):
            num, den = map(float, odds_str.split('/'))
            decimal = (num / den) + 1
            if decimal >= 2.0:
                return int((decimal - 1) * 100)
            else:
                return int(-100 / (decimal - 1))

        return None

    def detect_duplicates(self, new_bets: pd.DataFrame) -> List[int]:
        """Detect duplicate bets"""
        # Query existing bets for this user
        existing_bets = get_user_bets(self.user_id)

        duplicates = []
        for idx, new_bet in new_bets.iterrows():
            # Match on date + selection + stake
            matches = existing_bets[
                (existing_bets['bet_date'] == new_bet['bet_date']) &
                (existing_bets['selection'] == new_bet['selection']) &
                (abs(existing_bets['stake'] - new_bet['stake']) < 0.01)
            ]
            if len(matches) > 0:
                duplicates.append(idx)

        return duplicates

    def import_bets(self, df: pd.DataFrame, mapping: Dict) -> Dict:
        """Import bets with validation"""

        stats = {
            'total': len(df),
            'imported': 0,
            'skipped': 0,
            'errors': 0,
            'error_details': []
        }

        for idx, row in df.iterrows():
            try:
                bet_data = {
                    'user_id': self.user_id,
                    'bet_date': pd.to_datetime(row[mapping['bet_date']]),
                    'sport': self.normalize_sport(row[mapping['sport']]),
                    'odds': self.parse_odds(row[mapping['odds']]),
                    'stake': float(row[mapping['stake']]),
                    # ... map other fields
                }

                # Validate required fields
                if not all(bet_data.values()):
                    raise ValueError("Missing required field")

                # Save to database
                save_bet(bet_data)
                stats['imported'] += 1

            except Exception as e:
                stats['errors'] += 1
                stats['error_details'].append({
                    'row': idx + 1,
                    'error': str(e)
                })

        return stats
```

---

## 📊 Success Metrics

### User Metrics
- **Import completion rate:** Target 85%+
- **Average import size:** 500-2000 bets
- **Import time:** <30 seconds for 1,000 bets
- **Error rate:** <5% of rows

### Business Metrics
- **Onboarding conversion:** +15% from CSV import availability
- **Feature usage:** 40% of new users import within 7 days
- **User satisfaction:** 4.5/5 stars on import feature

---

## 🚧 Implementation Phases

### Phase 1: MVP (2 weeks)
- Basic CSV upload
- Standard format support
- Manual column mapping
- Simple validation
- Import summary

### Phase 2: Enhanced (2 weeks)
- Auto-mapping with confidence scores
- Action Network/Pikkit format support
- Duplicate detection
- Error reporting with details
- Background processing for large files

### Phase 3: Advanced (2 weeks)
- Mapping template save/reuse
- XLS/XLSX support
- Advanced validation rules
- Import history tracking
- Batch import API

### Phase 4: Polish (1 week)
- UI/UX improvements
- Import guide documentation
- Video tutorial
- Support for more export formats
- Performance optimization

---

## 🔒 Security & Privacy

- **File Scanning:** Virus scan all uploaded files
- **Data Validation:** Sanitize all inputs
- **User Isolation:** Strict user_id enforcement
- **File Cleanup:** Delete uploaded files after processing
- **Rate Limiting:** Max 5 imports per day per user
- **File Size Limit:** 10MB max
- **Data Encryption:** Encrypt bets at rest

---

## 📚 User Documentation

### Import Guide Sections
1. **Exporting from Other Platforms**
   - Action Network export steps
   - Pikkit export steps
   - Excel tracking sheet setup

2. **Preparing Your CSV**
   - Required columns
   - Date format recommendations
   - Odds format tips

3. **Mapping Columns**
   - What each field means
   - When to skip columns
   - Saving templates

4. **Troubleshooting**
   - Common errors and fixes
   - Date format issues
   - Duplicate handling

5. **Video Tutorial**
   - 5-minute walkthrough
   - Real example import

---

## ✅ Testing Plan

### Unit Tests
- CSV parsing (various formats)
- Date parsing (all formats)
- Odds conversion (American/Decimal/Fractional)
- Sport normalization
- Duplicate detection

### Integration Tests
- Full import flow
- Error handling
- Database transactions
- Stats update accuracy

### User Acceptance Tests
- Import Action Network export
- Import Pikkit export
- Import custom CSV
- Handle large file (10,000 bets)
- Handle malformed data

---

**Status:** Specification Complete - Ready for Development
**Estimated Development Time:** 6-7 weeks
**Target Release:** Q1 2026
