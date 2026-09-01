import unittest
from unittest.mock import patch, MagicMock
from football_oracle import FootballOracle

class TestFootballOracle(unittest.TestCase):

    @patch("genlayer.gl.nondet.web.get")
    @patch("genlayer.gl.eq_principle.prompt_comparative")
    def test_resolution_path_end_to_end(self, mock_consensus, mock_web_get):
        # 1. Khởi tạo hợp đồng
        oracle = FootballOracle(
            match_id="MATCH_001",
            home_team="Arsenal",
            away_team="Chelsea"
        )
        
        # Kiểm tra trạng thái ban đầu
        info = oracle.get_match_info()
        self.assertFalse(info["is_resolved"])

        # 2. Giả lập kết quả lấy từ nguồn tin cậy & đạt đồng thuận
        mock_response = MagicMock()
        mock_response.body.decode.return_value = "Arsenal defeated Chelsea 2-1 in MATCH_001."
        mock_web_get.return_value = mock_response
        
        mock_consensus.return_value = "Arsenal|2-1"

        # 3. Thực thi giải quyết trận đấu (Resolve)
        oracle.resolve_match("https://trusted-sports-source.com/match/MATCH_001")

        # Xác minh kết quả đã được ghi nhận đúng
        updated_info = oracle.get_match_info()
        self.assertTrue(updated_info["is_resolved"])
        self.assertEqual(updated_info["winning_team"], "Arsenal")
        self.assertEqual(updated_info["final_score"], "2-1")

        # 4. Kiểm tra ràng buộc giải quyết 1 lần (One-time resolution constraint)
        with self.assertRaises(Exception):
            oracle.resolve_match("https://trusted-sports-source.com/match/MATCH_001")

if __name__ == '__main__':
    unittest.main()
