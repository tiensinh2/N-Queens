import time
from pysat.solvers import Solver
from problem import NQueensProblem
from sat.encoders import ENCODERS

class SAT_NQueensRunner:
    def __init__(self, n, encoding_name="pairwise", solver_name="glucose3"):
        self.n = n
        self.encoding_name = encoding_name.lower().replace("_", "").replace("-", "")
        self.solver_name = solver_name.lower()
        self.problem = NQueensProblem(n)
        self.clauses = []
        self.num_vars = n * n

    def encode(self):
        """
        Thực hiện mã hóa N-Queens sang CNF dùng encoder tương ứng.
        """
        if self.encoding_name not in ENCODERS:
            raise ValueError(f"Unknown encoding: {self.encoding_name}")
            
        encoder = ENCODERS[self.encoding_name]
        self.clauses = []
        self.num_vars = self.n * self.n
        
        # 1. Ràng buộc Hàng (Exactly-One)
        for r in range(self.n):
            row_vars = [self.problem.get_var_id(r, c) for c in range(self.n)]
            cl, aux_used = encoder.encode_exactly_one(row_vars, self.num_vars)
            self.clauses.extend(cl)
            self.num_vars += aux_used
            
        # 2. Ràng buộc Cột (Exactly-One)
        for c in range(self.n):
            col_vars = [self.problem.get_var_id(r, c) for r in range(self.n)]
            cl, aux_used = encoder.encode_exactly_one(col_vars, self.num_vars)
            self.clauses.extend(cl)
            self.num_vars += aux_used
            
        # 3. Ràng buộc Đường chéo xuôi (At-Most-One)
        for k in range(-self.n + 1, self.n):
            diag_vars = []
            for r in range(self.n):
                c = r - k
                if 0 <= c < self.n:
                    diag_vars.append(self.problem.get_var_id(r, c))
            if len(diag_vars) > 1:
                cl, aux_used = encoder.encode_amo(diag_vars, self.num_vars)
                self.clauses.extend(cl)
                self.num_vars += aux_used
                
        # 4. Ràng buộc Đường chéo ngược (At-Most-One)
        for k in range(2 * self.n - 1):
            adiag_vars = []
            for r in range(self.n):
                c = k - r
                if 0 <= c < self.n:
                    adiag_vars.append(self.problem.get_var_id(r, c))
            if len(adiag_vars) > 1:
                cl, aux_used = encoder.encode_amo(adiag_vars, self.num_vars)
                self.clauses.extend(cl)
                self.num_vars += aux_used

    def solve(self):
        """
        Thực hiện mã hóa và giải SAT.
        """
        start_enc = time.perf_counter()
        self.encode()
        encoding_time = time.perf_counter() - start_enc
        
        start_solve = time.perf_counter()
        try:
            with Solver(name=self.solver_name, bootstrap_with=self.clauses) as solver:
                solved = solver.solve()
                solve_time = time.perf_counter() - start_solve
                
                if solved:
                    model = solver.get_model()
                    board = [[0] * self.n for _ in range(self.n)]
                    for r in range(self.n):
                        for c in range(self.n):
                            var_id = self.problem.get_var_id(r, c)
                            if model[var_id - 1] > 0:
                                board[r][c] = 1
                    return True, board, encoding_time, solve_time, self.num_vars, len(self.clauses), "OPT"
                else:
                    return False, None, encoding_time, solve_time, self.num_vars, len(self.clauses), "TIMEOUT"
        except Exception as e:
            return False, None, encoding_time, 0.0, self.num_vars, len(self.clauses), f"ERROR: {str(e)}"
