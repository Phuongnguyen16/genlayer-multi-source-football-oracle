
import json
from genlayer import *

class FootballPredictionMarket(gl.Contract):
    match_id: str
    home_team: str
    away_team: str
    is_resolved: bool
    winning_team: str
    final_score: str

    def __init__(self, match_id: str, home_team: str, away_team: str):
        self.match_id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.is_resolved = False
        self.winning_team = ""
        self.final_score = ""

    @gl.public.write
    def resolve_match(self, match_url: str) -> None:
        # Fetch web page using GenLayer nondeterministic web access
        web_data = gl.get_web_page(match_url)
        
        # Define prompt for validator AI execution
        prompt = f"""
        Extract the football match result for {self.home_team} vs {self.away_team} from this web content:
        {web_data}
        
        Return ONLY a JSON object with keys:
        - "winner": string ("home", "away", or "draw")
        - "score": string (e.g. "2-1")
        """
        
        # Equivalence Principle verification callback
        def equivalence_principle(result_str: str) -> bool:
            data = json.loads(result_str)
            return "winner" in data and "score" in data

        ai_response = gl.exec_prompt(prompt, eq_principle=equivalence_principle)
        parsed_result = json.loads(ai_response)

        # Update contract states
        self.winning_team = parsed_result["winner"]
        self.final_score = parsed_result["score"]
        self.is_resolved = True

    @gl.public.read
    def get_match_status(self) -> dict:
        return {
            "match_id": self.match_id,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "is_resolved": self.is_resolved,
            "winning_team": self.winning_team,
            "final_score": self.final_score
        }
