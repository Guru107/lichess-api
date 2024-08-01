from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aggregations import player_aggragation
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
origins = [
    "http://localhost:3000",
    "localhost:3000"
]
app = FastAPI(debug=True)
app.add_middleware(CORSMiddleware,allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], allow_headers=["*"])
player_agg = player_aggragation.PlayerAggregation()

@app.get("/", tags=["root"])
async def root():
    return {'message':'OK'}

@app.get("/api/1/wins")
async def compute_wins(username: str):
    return player_agg.calculate_wins(username)

@app.get("/api/1/openings")
async def compute_openings(username: str):
    return player_agg.calculate_opening_frequency(username)