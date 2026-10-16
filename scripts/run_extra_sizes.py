import sys
import os
import pandas as pd

# Path configuration (cho phép import từ thư mục src)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sat import SAT_NQueensRunner
from problem import NQueensProblem
from metrics import PerformanceTracker

def run_extra():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results", "benchmark_data.csv"))
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"Loaded existing database with {len(df)} records.")
    else:
        df = pd.DataFrame()
        print("No existing database found. Creating a new one.")

    sizes = [512, 1000]
    solver = "lingeling"
    enc = "seqcounter"
    repetitions = 3

    records = []

    for n in sizes:
        print(f"\n---> Running extra size N = {n} with solver {solver.upper()} and encoding {enc.upper()}...")
        problem = NQueensProblem(n)
        
        enc_times = []
        solve_times = []
        solved = False
        board = None
        total_vars = 0
        total_clauses = 0
        peak_mems = []
        
        for rep in range(repetitions):
            print(f"  Repetition {rep+1}/{repetitions}...")
            PerformanceTracker.start_memory_tracking()
            runner = SAT_NQueensRunner(n, encoding_name=enc, solver_name=solver)
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

        # Kiểm định tính đúng đắn độc lập
        valid_str = "N/A"
        if solved:
            is_valid, reason = problem.verify_solution(board)
            valid_str = "VALID" if is_valid else f"INVALID: {reason}"
            print(f"  Verification result: {valid_str}")
        else:
            print(f"  Solver failed or timed out!")

        records.append({
            "N": n,
            "Paradigm": "SAT",
            "Solver_Name": solver,
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

    extra_df = pd.DataFrame(records)

    if not df.empty:
        # Loại bỏ các hàng trùng lặp của N=512 hoặc 1000, SAT, lingeling, seqcounter để ghi đè sạch sẽ
        cond = (df["N"].isin(sizes)) & (df["Paradigm"] == "SAT") & (df["Solver_Name"] == solver) & (df["Encoding"] == enc)
        df = df[~cond]
        final_df = pd.concat([df, extra_df], ignore_index=True)
    else:
        final_df = extra_df

    # Sắp xếp lại theo N và Paradigm để bảng dữ liệu đẹp mắt
    final_df = final_df.sort_values(by=["N", "Paradigm", "Solver_Name", "Encoding"]).reset_index(drop=True)
    final_df.to_csv(csv_path, index=False)
    print(f"\nSuccessfully appended extra size results to: {csv_path}")

if __name__ == "__main__":
    run_extra()
