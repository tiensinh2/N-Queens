import time
import numpy as np
from ortools.linear_solver import pywraplp

class MIP_NQueensRunner:
    def __init__(self, n, solver_type="ortools_cbc", time_limit=300):
        self.n = n
        self.solver_type = solver_type.lower()
        self.time_limit = time_limit

    def solve(self):
        """
        Giải bài toán N-Queens bằng quy hoạch tuyến tính nguyên (MIP/ILP).
        """
        if self.solver_type == "ortools_cbc":
            return self._solve_ortools("CBC")
        elif self.solver_type == "ortools_scip":
            return self._solve_ortools("SCIP")
        elif self.solver_type == "scipy_highs":
            return self._solve_scipy_highs()
        elif self.solver_type == "gurobi":
            return self._solve_gurobi()
        elif self.solver_type == "cplex_mip":
            return self._solve_cplex_mip()
        else:
            return False, None, 0.0, 0.0, f"Unknown solver type: {self.solver_type}"

    def _solve_ortools(self, backend):
        start_model = time.perf_counter()
        solver = pywraplp.Solver.CreateSolver(backend)
        if not solver:
            return False, None, 0.0, 0.0, "NOT_INSTALLED"
 
        solver.set_time_limit(int(self.time_limit) * 1000)

        x = {}
        for i in range(self.n):
            for j in range(self.n):
                x[i, j] = solver.BoolVar(f"x_{i}_{j}")

        # Hàng
        for i in range(self.n):
            solver.Add(solver.Sum([x[i, j] for j in range(self.n)]) == 1)

        # Cột
        for j in range(self.n):
            solver.Add(solver.Sum([x[i, j] for i in range(self.n)]) == 1)

        # Đường chéo xuôi
        for k in range(-self.n + 1, self.n):
            diag_vars = [x[i, i - k] for i in range(self.n) if 0 <= i - k < self.n]
            if len(diag_vars) > 1:
                solver.Add(solver.Sum(diag_vars) <= 1)

        # Đường chéo ngược
        for k in range(2 * self.n - 1):
            adiag_vars = [x[i, k - i] for i in range(self.n) if 0 <= k - i < self.n]
            if len(adiag_vars) > 1:
                solver.Add(solver.Sum(adiag_vars) <= 1)

        model_time = time.perf_counter() - start_model

        start_solve = time.perf_counter()
        status = solver.Solve()
        solve_time = time.perf_counter() - start_solve

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            board = [[0] * self.n for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    if x[i, j].solution_value() > 0.5:
                        board[i][j] = 1
            return True, board, model_time, solve_time, "OPT"
        else:
            return False, None, model_time, solve_time, "TIMEOUT"

    def _solve_scipy_highs(self):
        start_model = time.perf_counter()
        try:
            from scipy.optimize import milp, LinearConstraint, Bounds
        except ImportError:
            return False, None, 0.0, 0.0, "NOT_INSTALLED"

        num_vars = self.n * self.n
        c = np.zeros(num_vars)
        integrality = np.ones(num_vars)
        bounds = Bounds(0, 1)

        A_rows = []
        lb_rows = []
        ub_rows = []

        # Ràng buộc hàng: Tổng = 1
        for i in range(self.n):
            row = np.zeros(num_vars)
            for j in range(self.n):
                row[i * self.n + j] = 1
            A_rows.append(row)
            lb_rows.append(1)
            ub_rows.append(1)

        # Ràng buộc cột: Tổng = 1
        for j in range(self.n):
            row = np.zeros(num_vars)
            for i in range(self.n):
                row[i * self.n + j] = 1
            A_rows.append(row)
            lb_rows.append(1)
            ub_rows.append(1)

        # Đường chéo xuôi: Tổng <= 1
        for k in range(-self.n + 1, self.n):
            row = np.zeros(num_vars)
            count = 0
            for i in range(self.n):
                j = i - k
                if 0 <= j < self.n:
                    row[i * self.n + j] = 1
                    count += 1
            if count > 1:
                A_rows.append(row)
                lb_rows.append(-np.inf)
                ub_rows.append(1)

        # Đường chéo ngược: Tổng <= 1
        for k in range(2 * self.n - 1):
            row = np.zeros(num_vars)
            count = 0
            for i in range(self.n):
                j = k - i
                if 0 <= j < self.n:
                    row[i * self.n + j] = 1
                    count += 1
            if count > 1:
                A_rows.append(row)
                lb_rows.append(-np.inf)
                ub_rows.append(1)

        A = np.array(A_rows)
        constraints = LinearConstraint(A, lb_rows, ub_rows)
        model_time = time.perf_counter() - start_model

        start_solve = time.perf_counter()
        res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds, options={"time_limit": self.time_limit})
        solve_time = time.perf_counter() - start_solve

        if res.success:
            board = [[0] * self.n for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    if res.x[i * self.n + j] > 0.5:
                        board[i][j] = 1
            return True, board, model_time, solve_time, "OPT"
        else:
            return False, None, model_time, solve_time, "TIMEOUT"

    def _solve_gurobi(self):
        start_model = time.perf_counter()
        try:
            import gurobipy as gp
            from gurobipy import GRB
        except ImportError:
            return False, None, 0.0, 0.0, "NOT_INSTALLED"

        try:
            env = gp.Env(empty=True)
            env.setParam("OutputFlag", 0)
            env.start()
            
            model = gp.Model("N-Queens_Gurobi", env=env)
            model.setParam("TimeLimit", self.time_limit)
            
            x = model.addVars(self.n, self.n, vtype=GRB.BINARY, name="x")
            
            model.addConstrs((x.sum(i, '*') == 1 for i in range(self.n)), name="row")
            model.addConstrs((x.sum('*', j) == 1 for j in range(self.n)), name="col")
            
            for k in range(-self.n + 1, self.n):
                model.addConstr(gp.quicksum(x[i, i - k] for i in range(self.n) if 0 <= i - k < self.n) <= 1)
                
            for k in range(2 * self.n - 1):
                model.addConstr(gp.quicksum(x[i, k - i] for i in range(self.n) if 0 <= k - i < self.n) <= 1)
                
            model_time = time.perf_counter() - start_model
            
            start_solve = time.perf_counter()
            model.optimize()
            solve_time = time.perf_counter() - start_solve
            
            if model.status == GRB.OPTIMAL or model.status == GRB.FEASIBLE:
                board = [[0] * self.n for _ in range(self.n)]
                for i in range(self.n):
                    for j in range(self.n):
                        if x[i, j].X > 0.5:
                            board[i][j] = 1
                return True, board, model_time, solve_time, "OPT"
            else:
                return False, None, model_time, solve_time, "TIMEOUT"
                
        except Exception as e:
            if "license" in str(e).lower() or "expired" in str(e).lower() or "qcl" in str(e).lower():
                return False, None, 0.0, 0.0, "NO_LICENSE"
            return False, None, 0.0, 0.0, f"ERROR: {str(e)}"

    def _solve_cplex_mip(self):
        start_model = time.perf_counter()
        try:
            from docplex.mp.model import Model as CPLEXModel
        except ImportError:
            return False, None, 0.0, 0.0, "NOT_INSTALLED"

        try:
            mdl = CPLEXModel(name="N-Queens_CPLEX_MIP")
            mdl.parameters.timelimit = self.time_limit
            
            x = mdl.binary_var_matrix(self.n, self.n, name="x")
            
            for i in range(self.n):
                mdl.add_constraint(mdl.sum(x[i, j] for j in range(self.n)) == 1)
            for j in range(self.n):
                mdl.add_constraint(mdl.sum(x[i, j] for i in range(self.n)) == 1)
                
            for k in range(-self.n + 1, self.n):
                mdl.add_constraint(mdl.sum(x[i, i - k] for i in range(self.n) if 0 <= i - k < self.n) <= 1)
                
            for k in range(2 * self.n - 1):
                mdl.add_constraint(mdl.sum(x[i, k - i] for i in range(self.n) if 0 <= k - i < self.n) <= 1)
                
            model_time = time.perf_counter() - start_model
            
            start_solve = time.perf_counter()
            solution = mdl.solve()
            solve_time = time.perf_counter() - start_solve
            
            if solution:
                board = [[0] * self.n for _ in range(self.n)]
                for i in range(self.n):
                    for j in range(self.n):
                        if solution[x[i, j]] > 0.5:
                            board[i][j] = 1
                return True, board, model_time, solve_time, "OPT"
            else:
                return False, None, model_time, solve_time, "TIMEOUT"
                
        except Exception as e:
            if "license" in str(e).lower() or "expired" in str(e).lower():
                return False, None, 0.0, 0.0, "NO_LICENSE"
            return False, None, 0.0, 0.0, f"ERROR: {str(e)}"
