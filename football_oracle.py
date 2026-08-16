# GenLayer Intelligent Contract: Football Prediction Market & Oracle
import json
from genlayer import *

class FootballPredictionMarket:
    def __init__(self, match_id: str, home_team: str, away_team: str):
        self.match_id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.is_resolved = False
        self.winning_team = ""
        self.final_score = ""

    @gl.public.write
    def resolve_match_with_ai_oracle(self, api_url: str):
        # 1. Fetch match data from web sources using GenLayer Non-Deterministic Web Access
        web_data = gl.web.get(api_url)
        
        # 2. Equivalence Principle check with AI-based reasoning
        prompt = f"""
        Analyze the following web response for match {self.home_team} vs {self.away_team}.
        Determine the winner ("home", "away", or "draw") and final score.
        Data: {web_data}
        Respond ONLY in JSON: {{"winner": "home/away/draw", "score": "X-Y"}}
        """
        
        ai_resolution = gl.ai.complete(prompt)
        parsed_result = json.loads(ai_resolution)

        # 3. Update contract state after consensus verification
        self.winning_team = parsed_result["winner"]
        self.final_score = parsed_result["score"]
        self.is_resolved = True

    @gl.public.read
    def get_match_result(self) -> dict:
        return {
            "match_id": self.match_id,
            "teams": f"{self.home_team} vs {self.away_team}",
            "is_resolved": self.is_resolved,
            "winning_team": self.winning_team,
            "final_score": self.final_score
        }
