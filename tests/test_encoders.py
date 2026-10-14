import sys
import os

# Cho phép import từ thư mục src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from sat.encoders import ENCODERS
from problem import NQueensProblem

class TestNQueensEncoders(unittest.TestCase):
    def setUp(self):
        self.variables = [1, 2, 3, 4]
        self.top_id = 4

    def test_pairwise_logic(self):
        """Kiểm nghiệm tính đúng đắn logic của Pairwise encoder"""
        encoder = ENCODERS["pairwise"]
        
        # Test ALO
        alo_cl, _ = encoder.encode_alo(self.variables, self.top_id)
        self.assertEqual(len(alo_cl), 1)
        self.assertEqual(alo_cl[0], [1, 2, 3, 4])
        
        # Test AMO (pairwise AMO generates 6 clauses for 4 variables)
        amo_cl, _ = encoder.encode_amo(self.variables, self.top_id)
        self.assertEqual(len(amo_cl), 6)
        
        # Test EXACTLY-ONE (pairwise EXACTLY-ONE generates 7 clauses for 4 variables)
        eo_cl, _ = encoder.encode_exactly_one(self.variables, self.top_id)
        self.assertEqual(len(eo_cl), 7)

    def test_seqcounter_logic(self):
        """Kiểm nghiệm Sequential Counter encoder"""
        encoder = ENCODERS["seqcounter"]
        amo_cl, aux_used = encoder.encode_amo(self.variables, self.top_id)
        self.assertTrue(aux_used > 0)
        self.assertTrue(len(amo_cl) > 0)

    def test_ladder_logic(self):
        """Kiểm nghiệm Ladder encoder"""
        encoder = ENCODERS["ladder"]
        amo_cl, aux_used = encoder.encode_amo(self.variables, self.top_id)
        self.assertTrue(aux_used > 0)
        self.assertTrue(len(amo_cl) > 0)

    def test_all_encoders_validity_nqueens(self):
        """Đảm bảo tất cả 6 bộ mã hóa đều tìm ra lời giải hợp lệ cho N=4"""
        problem = NQueensProblem(4)
        for name, encoder in ENCODERS.items():
            from sat.runner import SAT_NQueensRunner
            runner = SAT_NQueensRunner(4, encoding_name=name, solver_name="glucose3")
            success, board, _, _, _, _, _ = runner.solve()
            
            self.assertTrue(success, f"Encoder {name} failed to find solution for N=4!")
            valid, reason = problem.verify_solution(board)
            self.assertTrue(valid, f"Encoder {name} returned invalid board: {reason}")

if __name__ == "__main__":
    unittest.main()
