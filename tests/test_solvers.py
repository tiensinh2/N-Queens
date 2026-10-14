import sys
import os

# Cho phép import từ thư mục src (chèn vào đầu để tránh bị đè bởi package 'mip' ngoài)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from cp import CP_NQueensRunner
from mip import MIP_NQueensRunner
from problem import NQueensProblem

class TestNQueensSolvers(unittest.TestCase):
    def test_cp_ortools_solver(self):
        """Kiểm nghiệm CP solver (OR-Tools)"""
        problem = NQueensProblem(4)
        runner = CP_NQueensRunner(4, solver_type="ortools")
        success, board, _, _, status = runner.solve()
        
        self.assertTrue(success)
        self.assertEqual(status, "OPT")
        
        # Xác minh nghiệm độc lập
        valid, reason = problem.verify_solution(board)
        self.assertTrue(valid, f"CP solution is invalid: {reason}")

    def test_cp_cplex_solver(self):
        """Kiểm nghiệm CP solver (IBM CPLEX CP Optimizer)"""
        problem = NQueensProblem(4)
        runner = CP_NQueensRunner(4, solver_type="cplex_cp")
        success, board, _, _, status = runner.solve()
        
        self.assertTrue(success)
        self.assertEqual(status, "OPT")
        
        # Xác minh nghiệm độc lập
        valid, reason = problem.verify_solution(board)
        self.assertTrue(valid, f"CPLEX CP solution is invalid: {reason}")

    def test_mip_cbc_solver(self):
        """Kiểm nghiệm MIP solver (CBC via OR-Tools)"""
        problem = NQueensProblem(4)
        runner = MIP_NQueensRunner(4, solver_type="ortools_cbc")
        success, board, _, _, status = runner.solve()
        
        self.assertTrue(success)
        self.assertEqual(status, "OPT")
        
        # Xác minh nghiệm độc lập
        valid, reason = problem.verify_solution(board)
        self.assertTrue(valid, f"MIP CBC solution is invalid: {reason}")

    def test_uninstalled_solver_graceful_handling(self):
        """Đảm bảo các solver chưa cài đặt hoặc thiếu license được xử lý êm đẹp"""
        # Thử gọi Gurobi (giả sử chưa có license / chưa cài đặt trên máy này)
        runner = MIP_NQueensRunner(4, solver_type="gurobi")
        success, board, _, _, status = runner.solve()
        
        # Không được crash, phải trả về success=False và status thích hợp
        self.assertFalse(success)
        self.assertIn(status, ["NOT_INSTALLED", "NO_LICENSE"])

if __name__ == "__main__":
    sys.exit(unittest.main())
