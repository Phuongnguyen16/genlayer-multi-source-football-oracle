import unittest
from football_oracle import FootballOracle

class TestFootballOracle(unittest.TestCase):

    def test_one_time_match_resolution(self):
        # 1. Khởi tạo hợp đồng cho trận đấu cụ thể
        oracle = FootballOracle(
            match_id="MATCH123",
            home_team="Arsenal",
            away_team="Chelsea"
        )
        
        # Kiểm tra trạng thái ban đầu
        info = oracle.get_match_info()
        self.assertFalse(info["is_resolved"])

        # 2. Giả lập xác thực kết quả từ nguồn tin cậy
        trusted_source_url = "https://api.football-data.org/v4/matches/MATCH123"
        
        oracle.is_resolved = True
        oracle.winning_team = "Arsenal"
        oracle.final_score = "2-1"

        # Kiểm tra người thắng và tỷ số thực tế
        updated_info = oracle.get_match_info()
        self.assertTrue(updated_info["is_resolved"])
        self.assertEqual(updated_info["winning_team"], "Arsenal")
        self.assertEqual(updated_info["final_score"], "2-1")

        # 3. Chặn không cho giải quyết lại (Ràng buộc 1 lần duy nhất)
        with self.assertRaises(Exception):
            oracle.resolve_match(trusted_source_url)

if __name__ == '__main__':
    unittest.main()
