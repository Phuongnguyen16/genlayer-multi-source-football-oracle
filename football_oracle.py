import genlayer.gl as gl

class FootballOracle(gl.Contract):
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

    @gl.public.view
    def get_match_info(self) -> dict:
        """Trả về thông tin trạng thái trận đấu"""
        return {
            "match_id": self.match_id,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "is_resolved": self.is_resolved,
            "winning_team": self.winning_team,
            "final_score": self.final_score
        }

    @gl.public.write
    def resolve_match(self, result_url: str) -> None:
        """
        Lấy thông tin từ web (web-retrieval) và chạy qua cơ chế đồng thuận validator (consensus)
        """
        if self.is_resolved:
            raise Exception("Match has already been resolved")

        # Khối không định hạn: Tải dữ liệu từ trang web thực tế
        def fetch_and_evaluate():
            response = gl.nondet.web.get(result_url)
            web_content = response.body.decode("utf-8")
            
            prompt = f"""
            Analyze the following match report content:
            {web_content[:2000]}

            For match {self.home_team} vs {self.away_team} (ID: {self.match_id}):
            Extract the exact final winner team name and final score (e.g., 2-1).
            Return ONLY in format: WINNER|SCORE
            """
            return gl.nondet.exec_prompt(prompt)

        # Đạt đồng thuận giữa các Validator thông qua Equivalence Principle
        consensus_result = gl.eq_principle.prompt_comparative(
            fetch_and_evaluate,
            principle="The extracted winner and final score must match the match report."
        )

        parts = consensus_result.strip().split("|")
        
        self.winning_team = parts[0] if len(parts) > 0 else "Unknown"
        self.final_score = parts[1] if len(parts) > 1 else "0-0"
        self.is_resolved = True
