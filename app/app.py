from fastapi import FastAPI
from .aggregations import player_aggragation
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)
player_agg = player_aggragation.PlayerAggregation()

@app.get("/")
async def root():
    return {'message':'OK'}

@app.get("/api/1/wins")
async def compute_wins(username: str):
    return player_agg.calculate_wins(username)

@app.get("/api/1/openings")
async def compute_openings(username: str):
    return player_agg.calculate_opening_frequency(username)