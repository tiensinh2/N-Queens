import os
import yaml
import pandas as pd
from sat import SAT_NQueensRunner, SAT_SolverRegistry
from cp import CP_NQueensRunner
from mip import MIP_NQueensRunner
from problem import NQueensProblem
from metrics import PerformanceTracker

def run_synchronized_benchmark():
    # 1. Đọc file cấu hình YAML
    config_path = os.path.join("..", "configs", "benchmark_config.yaml")
    if not os.path.exists(config_path):
        # Nếu chạy từ thư mục root
        config_path = os.path.join("configs", "benchmark_config.yaml")
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    sizes = config.get("sizes", [4, 8, 12, 16])
    repetitions = config.get("repetitions", 3)
    time_limit = config.get("time_limit_seconds", 300)
    
    print("=========================================================")
    print(" SYSTEM SYNCHRONIZED BENCHMARK HARNESS INITIATED         ")
    print("=========================================================")
    
    # 2. Quét các SAT Solvers khả dụng thực tế
    available_sat_solvers = SAT_SolverRegistry.get_available_solvers()
    print(f" -> Dynamically detected working SAT Solvers: {available_sat_solvers}")
    
    # Định nghĩa danh sách các Solvers cần thử nghiệm
    # (Hệ thức giải, Tên gọi cụ thể, Kiểu solver_type)
    other_solvers = [
        ("CP-SAT", "OR_Tools_CP_SAT", "ortools"),
        ("CPLEX_CP", "CPLEX_CP_Optimizer", "cplex_cp"),
        ("MIP", "OR_Tools_MIP_CBC", "ortools_cbc"),
        ("MIP", "OR_Tools_MIP_SCIP", "ortools_scip"),
        ("MIP", "SciPy_MILP_HiGHS", "scipy_highs"),
        ("MIP", "Gurobi_Optimizer", "gurobi"),
        ("MIP", "CPLEX_MIP_Solver", "cplex_mip"),
    ]
    
    # Định nghĩa 6 kỹ thuật mã hóa SAT thủ công
    sat_encodings = ["pairwise", "seqcounter", "ladder", "commander", "binary", "product"]
    
    records = []
    
    # Đảm bảo thư mục results tồn tại
    results_dir = os.path.join("..", "results")
    if not os.path.exists(results_dir):
        results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    for n in sizes:
        print(f"\n---> Benchmarking board size N = {n}...")
        problem = NQueensProblem(n)
        
        # -------------------------------------------------------------
        # THỬ NGHIỆM SAT SOLVING (Kết hợp Encodings x Solvers)
        # -------------------------------------------------------------
        for sat_solver in available_sat_solvers:
            for enc in sat_encodings:
                # Tránh bùng nổ bộ nhớ quá mức cho Pairwise ở kích thước cực lớn (N >= 128)
                if n >= 128 and enc == "pairwise":
                    print(f"  [SAT] Skipping {sat_solver.upper()} with {enc.upper()} for N >= 128 to prevent Out-Of-Memory...")
                    records.append({
                        "N": n,
                        "Paradigm": "SAT",
                        "Solver_Name": sat_solver,
                        "Encoding": enc,
                        "Success": False,
                        "Model_Construction_Time": 0.0,
                        "Solving_Time": 0.0,
                        "Variables": 0,
                        "Aux_Variables": 0,
                        "Clauses": 0,
                        "Peak_Memory_Bytes": 0.0,
                        "Status": "SKIPPED_OOM_PREVENTION",
                        "Solution_Validity": "N/A"
                    })
                    continue

                # Bỏ qua glucose solvers cho N >= 64 theo yêu cầu để tránh thời gian giải lâu và nguy cơ quá tải
                if n >= 64 and "glucose" in sat_solver.lower():
                    print(f"  [SAT] Skipping {sat_solver.upper()} with {enc.upper()} for N >= 64 to save execution time...")
                    records.append({
                        "N": n,
                        "Paradigm": "SAT",
                        "Solver_Name": sat_solver,
                        "Encoding": enc,
                        "Success": False,
                        "Model_Construction_Time": 0.0,
                        "Solving_Time": 0.0,
                        "Variables": 0,
                        "Aux_Variables": 0,
                        "Clauses": 0,
                        "Peak_Memory_Bytes": 0.0,
                        "Status": "SKIPPED_TIMEOUT_PREVENTION",
                        "Solution_Validity": "N/A"
                    })
                    continue

                # Tránh chạy quá nhiều loại SAT ở kích thước N >= 100 (chỉ giữ lại Sequential Counter tuyến tính)
                if n >= 100 and enc != "seqcounter":
                    print(f"  [SAT] Skipping {sat_solver.upper()} with {enc.upper()} for N >= 100 to save execution time...")
                    records.append({
                        "N": n,
                        "Paradigm": "SAT",
                        "Solver_Name": sat_solver,
                        "Encoding": enc,
                        "Success": False,
                        "Model_Construction_Time": 0.0,
                        "Solving_Time": 0.0,
                        "Variables": 0,
                        "Aux_Variables": 0,
                        "Clauses": 0,
                        "Peak_Memory_Bytes": 0.0,
                        "Status": "SKIPPED_TIMEOUT_PREVENTION",
                        "Solution_Validity": "N/A"
                    })
                    continue

                print(f"  [SAT] Solver: {sat_solver.upper()} | Encoding: {enc.upper()}...")
                
                # Thực hiện lặp lại để lấy trung bình thống kê
                enc_times = []
                solve_times = []
                solved = False
                board = None
                total_vars = 0
                total_clauses = 0
                peak_mems = []
                
                for rep in range(repetitions):
                    PerformanceTracker.start_memory_tracking()
                    runner = SAT_NQueensRunner(n, encoding_name=enc, solver_name=sat_solver)
                    run_solved, run_board, enc_t, sol_t, n_vars, n_clauses, _ = runner.solve()
                    peak_mem = PerformanceTracker.stop_memory_tracking()
                    
                    enc_times.append(enc_t)
                    solve_times.append(sol_t)
                    peak_mems.append(peak_mem)
                    if rep == 0:
                        solved = run_solved
                        board = run_board
                        total_vars = n_vars
                        total_clauses = n_clauses
                
                # Kiểm nghiệm nghiệm độc lập
                valid_str = "N/A"
                if solved:
                    is_valid, reason = problem.verify_solution(board)
                    valid_str = "VALID" if is_valid else f"INVALID: {reason}"
                    
                records.append({
                    "N": n,
                    "Paradigm": "SAT",
                    "Solver_Name": sat_solver,
                    "Encoding": enc,
                    "Success": solved,
                    "Model_Construction_Time": sum(enc_times) / repetitions,
                    "Solving_Time": sum(solve_times) / repetitions,
                    "Variables": total_vars,
                    "Aux_Variables": total_vars - (n * n),
                    "Clauses": total_clauses,
                    "Peak_Memory_Bytes": sum(peak_mems) / repetitions,
                    "Status": "OPT" if solved else "TIMEOUT",
                    "Solution_Validity": valid_str
                })

        # -------------------------------------------------------------
        # THỬ NGHIỆM CP & MIP SOLVERS
        # -------------------------------------------------------------
        for paradigm, name, s_type in other_solvers:
            # Bỏ qua MIP solvers cho N >= 256 để tránh bế tắc và tốn thời gian
            if n >= 256 and paradigm == "MIP":
                print(f"  [{paradigm}] Skipping {name} for N >= 256 to save execution time...")
                records.append({
                    "N": n,
                    "Paradigm": paradigm,
                    "Solver_Name": name,
                    "Encoding": "N/A",
                    "Success": False,
                    "Model_Construction_Time": 0.0,
                    "Solving_Time": 0.0,
                    "Variables": 0,
                    "Aux_Variables": 0,
                    "Clauses": None,
                    "Peak_Memory_Bytes": 0.0,
                    "Status": "SKIPPED_TIMEOUT_PREVENTION",
                    "Solution_Validity": "N/A"
                })
                continue

            # Bỏ qua CP solvers cho N >= 512 để tránh bế tắc ở các cỡ bàn cờ khổng lồ
            if n >= 512 and paradigm in ["CP-SAT", "CPLEX_CP"]:
                print(f"  [{paradigm}] Skipping {name} for N >= 512 to save execution time...")
                records.append({
                    "N": n,
                    "Paradigm": paradigm,
                    "Solver_Name": name,
                    "Encoding": "N/A",
                    "Success": False,
                    "Model_Construction_Time": 0.0,
                    "Solving_Time": 0.0,
                    "Variables": None,
                    "Aux_Variables": None,
                    "Clauses": None,
                    "Peak_Memory_Bytes": 0.0,
                    "Status": "SKIPPED_TIMEOUT_PREVENTION",
                    "Solution_Validity": "N/A"
                })
                continue

            print(f"  [{paradigm}] Solver: {name}...")
            
            model_times = []
            solve_times = []
            success = False
            board = None
            peak_mems = []
            status = "OPT"
            
            for rep in range(repetitions):
                PerformanceTracker.start_memory_tracking()
                if paradigm == "CP-SAT" or paradigm == "CPLEX_CP":
                    runner = CP_NQueensRunner(n, solver_type=s_type, time_limit=time_limit)
                else: # MIP
                    runner = MIP_NQueensRunner(n, solver_type=s_type, time_limit=time_limit)
                    
                run_success, run_board, m_time, s_time, run_status = runner.solve()
                peak_mem = PerformanceTracker.stop_memory_tracking()
                
                model_times.append(m_time)
                solve_times.append(s_time)
                peak_mems.append(peak_mem)
                if rep == 0:
                    success = run_success
                    board = run_board
                    status = run_status
            
            valid_str = "N/A"
            if success:
                is_valid, reason = problem.verify_solution(board)
                valid_str = "VALID" if is_valid else f"INVALID: {reason}"
                
            records.append({
                "N": n,
                "Paradigm": paradigm,
                "Solver_Name": name,
                "Encoding": "N/A",
                "Success": success,
                "Model_Construction_Time": sum(model_times) / repetitions,
                "Solving_Time": sum(solve_times) / repetitions,
                "Variables": n * n if paradigm == "MIP" else None,
                "Aux_Variables": 0 if paradigm == "MIP" else None,
                "Clauses": None,
                "Peak_Memory_Bytes": sum(peak_mems) / repetitions if status not in ["NOT_INSTALLED", "NO_LICENSE"] else 0,
                "Status": status,
                "Solution_Validity": valid_str
            })
            
    # Lưu file kết quả CSV
    csv_path = os.path.join(results_dir, "benchmark_data.csv")
    df = pd.DataFrame(records)
    df.to_csv(csv_path, index=False)
    
    print("\n=========================================================")
    print(f" ALL BENCHMARKS RUN COMPLETED! Exported raw data to:")
    print(f" -> {csv_path}")
    print("=========================================================")

if __name__ == "__main__":
    run_synchronized_benchmark()
