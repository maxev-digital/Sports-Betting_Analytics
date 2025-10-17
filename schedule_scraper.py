#!/usr/bin/env python3
"""
NBA Schedule Scraper
Gets team schedules to detect rest days and back-to-back games
"""

import requests
from datetime import datetime, timedelta
import pandas as pd
import os

class NBAScheduleScraper:
    """Scrape NBA schedules to detect rest advantages"""
    
    def __init__(self):
        self.base_url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
        
    def get_schedule(self):
        """Get full NBA schedule"""
        print("📅 Fetching NBA schedule...")
        
        try:
            response = requests.get(self.base_url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            games = []
            
            for date_group in data['leagueSchedule']['gameDates']:
                game_date = date_group['gameDate']
                
                for game in date_group['games']:
                    games.append({
                        'game_id': game['gameId'],
                        'game_date': game_date,
                        'home_team': game['homeTeam']['teamName'],
                        'away_team': game['awayTeam']['teamName'],
                        'home_team_code': game['homeTeam']['teamTricode'],
                        'away_team_code': game['awayTeam']['teamTricode']
                    })
            
            df = pd.DataFrame(games)
            df['game_date'] = pd.to_datetime(df['game_date'])
            
            print(f"✓ Retrieved schedule: {len(df)} games")
            
            return df
            
        except Exception as e:
            print(f"⚠️  Schedule API failed: {e}")
            print("   Using basic schedule (no rest days)")
            return pd.DataFrame()
    
    def calculate_rest_days(self, team, game_date, schedule_df):
        """Calculate days of rest for a team before a game"""
        
        if schedule_df.empty:
            return None
        
        # Get all games for this team before the target game
        team_games = schedule_df[
            ((schedule_df['home_team'] == team) | (schedule_df['away_team'] == team)) &
            (schedule_df['game_date'] < game_date)
        ].sort_values('game_date', ascending=False)
        
        if len(team_games) == 0:
            return None  # First game of season
        
        # Most recent game before this one
        last_game_date = team_games.iloc[0]['game_date']
        
        # Calculate rest days
        days_rest = (game_date - last_game_date).days - 1
        
        return days_rest
    
    def analyze_upcoming_games(self, predictions_df):
        """Add rest day analysis to predictions"""
        print("\n🔍 Analyzing rest days for upcoming games...")
        
        schedule_df = self.get_schedule()
        
        if schedule_df.empty:
            print("⚠️  No schedule data available")
            predictions_df['home_days_rest'] = None
            predictions_df['away_days_rest'] = None
            predictions_df['rest_advantage'] = 'Unknown'
            return predictions_df
        
        results = []
        
        for _, pred in predictions_df.iterrows():
            game_date = pd.to_datetime(pred['game_date'])
            
            # Calculate rest for both teams
            home_rest = self.calculate_rest_days(pred['home_team'], game_date, schedule_df)
            away_rest = self.calculate_rest_days(pred['away_team'], game_date, schedule_df)
            
            # Determine advantage
            if home_rest is None or away_rest is None:
                rest_advantage = 'Unknown'
            elif home_rest == 0 and away_rest > 1:
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
            
            results.append({
                'home_days_rest': home_rest,
                'away_days_rest': away_rest,
                'rest_advantage': rest_advantage
            })
        
        # Add to predictions
        rest_df = pd.DataFrame(results)
        predictions_df = pd.concat([predictions_df, rest_df], axis=1)
        
        print(f"✓ Rest analysis complete")
        
        # Show summary
        b2b_count = len(predictions_df[predictions_df['rest_advantage'].str.contains('B2B', na=False)])
        advantage_count = len(predictions_df[predictions_df['rest_advantage'].str.contains('Rested|Fresh', na=False)])
        
        if b2b_count > 0:
            print(f"  ⚠️  {b2b_count} games with back-to-back situations")
        if advantage_count > 0:
            print(f"  🎯 {advantage_count} games with clear rest advantages")
        
        return predictions_df


if __name__ == "__main__":
    scraper = NBAScheduleScraper()
    schedule = scraper.get_schedule()
    
    if not schedule.empty:
        print(f"\n✓ Schedule loaded: {len(schedule)} games")
        print(f"  Date range: {schedule['game_date'].min()} to {schedule['game_date'].max()}")