#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER SCRIPT - Complete NBA Daily Workflow
Runs everything in one command with rest days analysis
"""

import sys
import os
import io

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.append('backend')

from datetime import datetime, timedelta, timezone
import pandas as pd

# Import all modules
from scrapers.nba.nba_api_stats import NBAScraper
from scrapers.odds.sportsdataio_scraper import SportsDataIOScraper
from scrapers.nba.schedule_scraper import NBAScheduleScraper
from models.nba.totals_predictor import NBATotalsPredictor
from utils.performance_tracker import PerformanceTracker
from sheets_integration.nba_sheets_uploader import NBAGoogleSheetsUploader

# Import auto-logger for persistent database tracking
sys.path.append('backend/scrapers/nba/backend')
from auto_play_logger import AutoPlayLogger

def run_complete_workflow():
    """Complete daily workflow with rest days analysis"""
    
    print("\n" + "="*70)
    print("🏀 NBA DAILY PREDICTIONS - COMPLETE WORKFLOW")
    print("="*70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # === STEP 1: SCRAPE NBA TEAM STATS ===
    print("[1/6] Scraping NBA team stats...")
    print("-"*70)
    
    nba_scraper = NBAScraper()
    team_stats = nba_scraper.run_full_scrape()
    
    if team_stats is None:
        print("❌ Failed to get team stats")
        return
    
    # === STEP 2: GET BETTING ODDS ===
    print("\n[2/6] Fetching betting odds...")
    print("-"*70)

    odds_scraper = SportsDataIOScraper()
    # Fetch odds for next 14 days using Sports Data IO
    # NBA 2025 season runs from Oct 2024 - Apr 2025
    odds_df = odds_scraper.get_nba_odds(date='2024-11-07', days_ahead=14)
    
    if odds_df.empty:
        print("⚠️  No games found")
        return
    
    # Sports Data IO already fetched 14 days - filter to upcoming games only
    current_time = datetime.now()

    upcoming_odds = odds_df[
        odds_df['commence_time'] >= current_time
    ].copy()

    if upcoming_odds.empty:
        print("⚠️  No upcoming games found")
        return

    # Format game date/time for display
    upcoming_odds['game_datetime_local'] = upcoming_odds['commence_time']
    upcoming_odds['game_date'] = upcoming_odds['game_datetime_local'].dt.date
    upcoming_odds['game_time'] = upcoming_odds['game_datetime_local'].dt.strftime('%I:%M %p')
    upcoming_odds['day_of_week'] = upcoming_odds['game_datetime_local'].dt.strftime('%A')
    
    print(f"✓ Found {upcoming_odds['game_id'].nunique()} games in next 14 days")
    
    # === STEP 3: GET SCHEDULE FOR REST DAYS ===
    print("\n[3/6] Analyzing rest days & back-to-backs...")
    print("-"*70)
    
    schedule_scraper = NBAScheduleScraper()
    schedule_df = schedule_scraper.get_schedule()
    
    # === STEP 4: GENERATE PREDICTIONS WITH REST DAYS ===
    print("\n[4/6] Generating predictions with rest day adjustments...")
    print("-"*70)
    
    predictor = NBATotalsPredictor(team_stats)
    
    predictions = []
    unique_games = upcoming_odds[['game_id', 'home_team', 'away_team', 'game_date', 'game_time', 'day_of_week']].drop_duplicates()
    
    for _, game in unique_games.iterrows():
        game_id = game['game_id']
        home_team = game['home_team']
        away_team = game['away_team']
        game_date_dt = pd.to_datetime(game['game_date'])
        
        # Get consensus market total
        market_total = odds_scraper.get_consensus_total(game_id, upcoming_odds)
        
        if market_total is None:
            continue
        
        # Calculate rest days
        home_rest = None
        away_rest = None
        rest_advantage = 'Unknown'
        
        if not schedule_df.empty:
            home_rest = schedule_scraper.calculate_rest_days(home_team, game_date_dt, schedule_df)
            away_rest = schedule_scraper.calculate_rest_days(away_team, game_date_dt, schedule_df)
            
            # Determine advantage
            if home_rest is not None and away_rest is not None:
                if home_rest == 0 and away_rest > 1:
                    rest_advantage = 'Away Rested'
                elif away_rest == 0 and home_rest > 1:
                    rest_advantage = 'Home Rested'
                elif home_rest == 0 and away_rest == 0:
                    rest_advantage = 'Both B2B'
                elif home_rest >= 3 and away_rest <= 1:
                    rest_advantage = 'Home Fresh'
                elif away_rest >= 3 and home_rest <= 1:
                    rest_advantage = 'Away Fresh'
                else:
                    rest_advantage = 'Even'
        
        # Generate prediction with rest context
        game_context = {
            'home_days_rest': home_rest,
            'away_days_rest': away_rest
        }
        
        result = predictor.predict_game_total(home_team, away_team, game_context)
        
        if 'error' in result:
            print(f"  ⚠️  Skipping {away_team} @ {home_team}: {result['error']}")
            continue
        
        # Calculate edge
        edge = predictor.calculate_edge(result['predicted_total'], market_total)
        
        # Days until game
        days_until = (game['game_date'] - datetime.now().date()).days
        
        predictions.append({
            'game_date': str(game['game_date']),
            'day_of_week': game['day_of_week'],
            'game_time': game['game_time'],
            'days_until': days_until,
            'game_id': game_id,
            'away_team': away_team,
            'home_team': home_team,
            'home_days_rest': home_rest if home_rest is not None else 'Unknown',
            'away_days_rest': away_rest if away_rest is not None else 'Unknown',
            'rest_advantage': rest_advantage,
            'away_pace': result['breakdown']['away_pace'],
            'home_pace': result['breakdown']['home_pace'],
            'expected_pace': result['expected_pace'],
            'pace_adjustment': result['breakdown']['pace_adjustment'],
            'rest_factors': ', '.join(result['breakdown']['rest_factors']),
            'away_off_rating': result['breakdown']['away_off_rating'],
            'home_off_rating': result['breakdown']['home_off_rating'],
            'away_def_rating': result['breakdown']['away_def_rating'],
            'home_def_rating': result['breakdown']['home_def_rating'],
            'away_expected_pts': result['away_expected_points'],
            'home_expected_pts': result['home_expected_points'],
            'predicted_total': result['predicted_total'],
            'market_total': market_total,
            'edge': edge['edge'],
            'recommendation': edge['side'],
            'confidence': edge['confidence'],
            'bet': 'YES' if edge['bet'] else 'NO'
        })
    
    if not predictions:
        print("⚠️  No valid predictions generated")
        return
    
    predictions_df = pd.DataFrame(predictions)
    predictions_df = predictions_df.sort_values(['game_date', 'edge'], ascending=[True, False])
    
    # Save predictions
    output_dir = 'backend/data/predictions'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/nba_predictions_{timestamp}.csv'
    predictions_df.to_csv(filename, index=False)
    
    latest_file = f'{output_dir}/nba_predictions_latest.csv'
    predictions_df.to_csv(latest_file, index=False)
    
    print(f"✓ Generated {len(predictions_df)} predictions")
    print(f"📁 Saved: {latest_file}")
    
    # Show games with rest advantages
    rest_games = predictions_df[predictions_df['rest_advantage'] != 'Even']
    if len(rest_games) > 0:
        print(f"\n🎯 {len(rest_games)} games with rest factors:")
        for _, game in rest_games.head(5).iterrows():
            print(f"  {game['away_team']} @ {game['home_team']}")
            print(f"    Rest: {game['rest_advantage']} | {game['rest_factors']}")

    # === STEP 4.5: AUTO-LOG TO DATABASE ===
    print("\n[4.5/7] Auto-logging plays to persistent database...")
    print("-"*70)

    auto_logger = AutoPlayLogger()
    logged_count = 0

    # Only log bets that we're actually making (HIGH/MEDIUM confidence)
    bets_to_log = predictions_df[predictions_df['bet'] == 'YES']

    for _, pred in bets_to_log.iterrows():
        try:
            # Get bookmaker data for this game
            game_odds_data = upcoming_odds[upcoming_odds['game_id'] == pred['game_id']]

            # Build bookmaker list from odds data
            bookmaker_data = []
            if not game_odds_data.empty:
                for _, odds_row in game_odds_data.iterrows():
                    bookmaker_data.append({
                        'title': odds_row.get('sportsbook', 'Unknown'),
                        'markets': [{
                            'key': 'totals',
                            'outcomes': [
                                {'name': 'Over', 'point': pred['market_total'], 'price': -110},
                                {'name': 'Under', 'point': pred['market_total'], 'price': -110}
                            ]
                        }]
                    })

            # Calculate our probability from the prediction
            our_probability = 0.55  # Default, adjust based on edge
            if pred['edge'] > 5:
                our_probability = 0.58
            elif pred['edge'] > 3:
                our_probability = 0.56

            # Market probability (assuming -110 both sides = 52.4% each)
            market_prob = 0.524

            # Format game time
            game_datetime = f"{pred['game_date']}T{pred['game_time'].replace(' ', '')}"

            # Log the play
            play_id = auto_logger.log_prediction(
                game_id=pred['game_id'],
                sport='NBA',
                home_team=pred['home_team'],
                away_team=pred['away_team'],
                game_time=game_datetime,
                strategy_name='pace_based',  # This is your primary NBA strategy
                play_type='TOTALS',
                recommended_side=pred['recommendation'],
                recommended_line=pred['market_total'],
                confidence_level=pred['confidence'],
                our_probability=our_probability,
                market_odds={'over': -110, 'under': -110},
                edge_percentage=pred['edge'],
                expected_value=pred['edge'] * 0.1,  # Rough EV calculation
                bookmaker_data=bookmaker_data,
                momentum_indicator=pred['rest_advantage'] if pred['rest_advantage'] != 'Even' else None,
                trend_data={
                    'expected_pace': float(pred['expected_pace']),
                    'pace_adjustment': float(pred['pace_adjustment']),
                    'rest_factors': pred['rest_factors'],
                    'home_rest_days': pred['home_days_rest'],
                    'away_rest_days': pred['away_days_rest']
                },
                notes=f"Rest: {pred['rest_advantage']}, Edge: {pred['edge']:.1f}"
            )

            if play_id:
                logged_count += 1
                print(f"  ✓ Logged: {pred['away_team']} @ {pred['home_team']} - {pred['recommendation']} {pred['market_total']}")
            else:
                print(f"  ⚠️  Failed to log: {pred['away_team']} @ {pred['home_team']}")

        except Exception as e:
            print(f"  ❌ Error logging {pred['away_team']} @ {pred['home_team']}: {str(e)}")

    print(f"✓ Successfully logged {logged_count}/{len(bets_to_log)} plays to database")

    # === STEP 5: LOG PREDICTIONS (OLD TRACKER) ===
    print("\n[5/7] Logging predictions for CSV tracking...")
    print("-"*70)
    
    tracker = PerformanceTracker()
    tracker.log_predictions(latest_file)
    
    # === STEP 6: UPLOAD TO GOOGLE SHEETS ===
    print("\n[6/6] Uploading to Google Sheets...")
    print("-"*70)
    
    try:
        sheet_id = '1bFNPXj2wOOBid8d-dnHbKmSs5U90a66X29-PFRmkgvo'
        
        uploader = NBAGoogleSheetsUploader()
        uploader.authenticate()
        uploader.open_sheet_by_id(sheet_id)
        url = uploader.upload_predictions(latest_file)
        
        print(f"✓ Upload complete!")
        print(f"📊 View sheet: {url}")
        
    except Exception as e:
        print(f"⚠️  Google Sheets upload failed: {e}")
        print("   Predictions still saved to CSV")
    
    # === SUMMARY ===
    print("\n" + "="*70)
    print("✅ WORKFLOW COMPLETE")
    print("="*70)
    print(f"📊 Total games: {len(predictions_df)}")
    print(f"🎯 HIGH confidence: {len(predictions_df[predictions_df['confidence']=='HIGH'])}")
    print(f"⚠️  Back-to-back games: {len(predictions_df[predictions_df['rest_advantage'].str.contains('B2B', na=False)])}")
    print(f"✅ Recommended bets: {len(predictions_df[predictions_df['bet']=='YES'])}")
    
    # Top 3 bets
    top_bets = predictions_df[predictions_df['bet']=='YES'].nlargest(3, 'edge')
    if len(top_bets) > 0:
        print(f"\n🏆 TOP 3 BETS:")
        for _, bet in top_bets.iterrows():
            print(f"  {bet['away_team']} @ {bet['home_team']}")
            print(f"    {bet['recommendation']} {bet['market_total']} (Edge: {bet['edge']}) - {bet['confidence']}")
            if bet['rest_advantage'] != 'Even':
                print(f"    Rest: {bet['rest_advantage']}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    run_complete_workflow()