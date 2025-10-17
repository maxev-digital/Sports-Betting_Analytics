#!/usr/bin/env python3
"""
NBA Official API Scraper - FIXED VERSION
Collects ONLY 30 NBA team stats
"""

from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams
import pandas as pd
from datetime import datetime
import os

class NBAScraper:
    def __init__(self):
        self.all_teams = teams.get_teams()
        self.nba_team_ids = [team['id'] for team in self.all_teams]
        self.current_season = '2024-25'
        
    def get_team_stats(self):
        """Get comprehensive team stats from NBA API"""
        print("Fetching NBA team stats...")
        
        try:
            # Get basic stats
            team_stats = leaguedashteamstats.LeagueDashTeamStats(
                season=self.current_season,
                per_mode_detailed='PerGame'
            )
            
            df = team_stats.get_data_frames()[0]
            
            # Get advanced stats
            advanced_stats = leaguedashteamstats.LeagueDashTeamStats(
                season=self.current_season,
                measure_type_detailed_defense='Advanced'
            )
            
            df_advanced = advanced_stats.get_data_frames()[0]
            
            # Merge basic and advanced stats
            result_df = pd.DataFrame()
            result_df['team_id'] = df['TEAM_ID']
            result_df['team_name'] = df['TEAM_NAME']
            result_df['games_played'] = df['GP']
            result_df['wins'] = df['W']
            result_df['losses'] = df['L']
            
            # From advanced stats
            result_df['pace'] = df_advanced['PACE']
            result_df['off_rating'] = df_advanced['OFF_RATING']
            result_df['def_rating'] = df_advanced['DEF_RATING']
            result_df['net_rating'] = df_advanced['NET_RATING']
            
            # From basic stats
            result_df['pts_per_game'] = df['PTS']
            result_df['opp_pts_per_game'] = df_advanced['DEF_RATING']
            
            # Optional stats
            if 'EFG_PCT' in df_advanced.columns:
                result_df['efg_pct'] = df_advanced['EFG_PCT']
            else:
                result_df['efg_pct'] = 0.5
                
            if 'TS_PCT' in df_advanced.columns:
                result_df['ts_pct'] = df_advanced['TS_PCT']
            else:
                result_df['ts_pct'] = 0.55
            
            # *** FILTER TO ONLY NBA TEAMS (30 teams) ***
            result_df = result_df[result_df['team_id'].isin(self.nba_team_ids)]
            
            print(f"✓ Retrieved stats for {len(result_df)} NBA teams")
            return result_df
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def run_full_scrape(self):
        """Execute complete NBA data collection"""
        print("="*60)
        print("NBA DATA SCRAPER - NBA TEAMS ONLY")
        print("="*60)
        
        team_stats = self.get_team_stats()
        
        if team_stats is None:
            print("❌ Scraping failed")
            return None
        
        # Create output directory
        output_dir = 'backend/data/raw/nba'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{output_dir}/nba_team_stats_{timestamp}.csv'
        team_stats.to_csv(filename, index=False)
        
        print(f"\n✓ Saved: {filename}")
        print(f"✓ Teams: {len(team_stats)}")
        
        # Also save as "latest" for easy access
        latest_file = f'{output_dir}/nba_team_stats_latest.csv'
        team_stats.to_csv(latest_file, index=False)
        print(f"✓ Saved: {latest_file}")
        
        return team_stats


if __name__ == "__main__":
    scraper = NBAScraper()
    data = scraper.run_full_scrape()
    
    if data is not None:
        print("\n📊 Top 5 teams by pace:")
        print(data.nlargest(5, 'pace')[['team_name', 'pace', 'off_rating', 'def_rating']])