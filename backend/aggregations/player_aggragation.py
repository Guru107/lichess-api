import berserk
import pandas as pd
import duckdb
import numpy as np
import logging
from pydantic import BaseModel, PositiveInt
from dataclasses import dataclass
from pandas_to_pydantic import dataframe_to_pydantic
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WinsRecord(BaseModel):
    result: str
    count: PositiveInt

@dataclass
class OpeningRecord(BaseModel):
    opening: str
    count: PositiveInt

class PlayerAggregation:
    def __init__(self):
        LICHESS_API_TOKEN=os.getenv("API_TOKEN")
        self.session = berserk.TokenSession(token=LICHESS_API_TOKEN)
        self.client = berserk.Client(session=self.session,pgn_as_default=False)
    
    def _get_player_games(self, username: str):
        return self.client.games.export_by_player(username, opening=True, moves=False, finished=True,rated=True)
    
    def _get_games_df(self, username: str) -> pd.DataFrame:
        return pd.json_normalize(self._get_player_games(username),sep="_")

    def calculate_wins(self, username: str) -> pd.DataFrame:
        games_df = self._get_games_df(username)
        games_df['winner_user'] = np.where(games_df['winner'] == 'black', games_df['players_black_user_name'],games_df['players_white_user_name'])
        wins = dataframe_to_pydantic(duckdb.sql(f"select IF(winner_user !='{username}', 'loss', 'win') as result, count(1) as count from games_df group by result").to_df(), WinsRecord)
        return wins.model_dump()

    
    def calculate_opening_frequency(self, username: str) -> pd.DataFrame:
        games_df = self._get_games_df(username)
        games_df.rename(columns={'players_white_user_id':'player_white', 'opening_name':'opening_name'},inplace=True)
        openings = dataframe_to_pydantic(duckdb.sql("select opening_name as opening, count(opening_name) as count from games_df where player_white='guru107' group by opening order by count desc").to_df(), OpeningRecord)
        return openings.model_dump()
    


    

    