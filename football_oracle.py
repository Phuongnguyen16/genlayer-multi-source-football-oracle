from genlayer import *

@gl.contract
class FootballOracle:
    """
    GenVM-compatible Football Prediction Oracle
    """
    
    def __init__(self, match_id: str, home_team: str, away_team: str):
        self.match_id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.is_resolved = False
        self.winning_team = ""
        self.final_score = ""

    @gl.public.view
    def get_match_info(self) -> dict:
        """Trả về thông tin trận đấu"""
        return {
            "match_id": self.match_id,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "is_resolved": self.is_resolved,
            "winning_team": self.winning_team,
            "final_score": self.final_score
        }

    @gl.public.write
    def resolve_match(self, result_url: str) -> dict:
        """
        Xác thực và phân định kết quả 1 lần duy nhất từ nguồn tin cậy
        """
        if self.is_resolved:
            raise Exception("Match has already been resolved")

        prompt = f"""
        Fetch official result from match-bound source: {result_url}
        Match ID: {self.match_id} ({self.home_team} vs {self.away_team})

        Respond ONLY in JSON format:
        {{
            "winner": "Team Name or Draw",
            "score": "X-Y"
        }}
        """

        ai_response = gl.exec_prompt(prompt)
        
        self.is_resolved = True
        self.winning_team = ai_response.get("winner", "")
        self.final_score = ai_response.get("score", "")

        return {
            "winner": self.winning_team,
            "score": self.final_score
        }
