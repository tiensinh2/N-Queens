import time
from ortools.sat.python import cp_model

class CP_NQueensRunner:
    def __init__(self, n, solver_type="ortools", time_limit=300):
        self.n = n
        self.solver_type = solver_type.lower()
        self.time_limit = time_limit

    def solve(self):
        """
        Giải bài toán N-Queens bằng Constraint Programming.
        """
        if self.solver_type == "ortools":
            return self._solve_ortools()
        elif self.solver_type == "cplex_cp":
            return self._solve_cplex_cp()
        else:
            return False, None, 0.0, 0.0, f"Unknown solver type: {self.solver_type}"

    def _solve_ortools(self):
        start_model = time.perf_counter()
        model = cp_model.CpModel()
        
        Q = [model.NewIntVar(0, self.n - 1, f"Q_{i}") for i in range(self.n)]
        
        model.AddAllDifferent(Q)
        model.AddAllDifferent([Q[i] + i for i in range(self.n)])
        model.AddAllDifferent([Q[i] - i for i in range(self.n)])
        
        model_time = time.perf_counter() - start_model
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = float(self.time_limit)
        
        start_solve = time.perf_counter()
        status = solver.Solve(model)
        solve_time = time.perf_counter() - start_solve
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            board = [[0] * self.n for _ in range(self.n)]
            for r in range(self.n):
                col = solver.Value(Q[r])
                board[r][col] = 1
            return True, board, model_time, solve_time, "OPT"
        else:
            return False, None, model_time, solve_time, "TIMEOUT"

    def _solve_cplex_cp(self):
        start_model = time.perf_counter()
        try:
            from docplex.cp.model import CpoModel, integer_var_list, all_diff
        except ImportError:
            return False, None, 0.0, 0.0, "NOT_INSTALLED"
            
        try:
            import os
            cp_bin = r"D:\IBM_CP_SOLVER\cpoptimizer\bin\x64_win64"
            cplex_bin = r"D:\IBM_CP_SOLVER\cplex\bin\x64_win64"
            if os.path.exists(cp_bin) and cp_bin not in os.environ["PATH"]:
                os.environ["PATH"] = cp_bin + os.pathsep + cplex_bin + os.pathsep + os.environ["PATH"]

            mdl = CpoModel()
            Q = integer_var_list(self.n, 0, self.n - 1, "Q")
            
            mdl.add(all_diff(Q))
            mdl.add(all_diff([Q[i] + i for i in range(self.n)]))
            mdl.add(all_diff([Q[i] - i for i in range(self.n)]))
            
            model_time = time.perf_counter() - start_model
            
            start_solve = time.perf_counter()
            # Gọi trực tiếp qua file thực thi local được cài đặt tại D:\IBM_CP_SOLVER
            exec_path = "D:\\IBM_CP_SOLVER\\cpoptimizer\\bin\\x64_win64\\cpoptimizer.exe"
            msol = mdl.solve(execfile=exec_path, TimeLimit=self.time_limit)
            solve_time = time.perf_counter() - start_solve
            
            if msol:
                board = [[0] * self.n for _ in range(self.n)]
                for r in range(self.n):
                    col = msol[Q[r]]
                    board[r][col] = 1
                return True, board, model_time, solve_time, "OPT"
            else:
                return False, None, model_time, solve_time, "TIMEOUT"
                
        except Exception as e:
            if "license" in str(e).lower() or "expired" in str(e).lower():
                return False, None, 0.0, 0.0, "NO_LICENSE"
            return False, None, 0.0, 0.0, f"ERROR: {str(e)}"
