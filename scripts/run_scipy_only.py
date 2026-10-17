import os
import sys
import yaml
import pandas as pd
import numpy as np

# Adjust sys.path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from mip import MIP_NQueensRunner
from problem import NQueensProblem
from metrics import PerformanceTracker

def run_scipy_only():
    csv_path = os.path.join("results", "benchmark_data.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join("..", "results", "benchmark_data.csv")
        if not os.path.exists(csv_path):
            print("Error: benchmark_data.csv not found!")
            return

    # Load configuration
    config_path = os.path.join("configs", "benchmark_config.yaml")
    if not os.path.exists(config_path):
        config_path = os.path.join("..", "configs", "benchmark_config.yaml")
        
    repetitions = 3
    time_limit = 60
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            repetitions = config.get("repetitions", 3)
            time_limit = config.get("time_limit_seconds", 60)

    print("=========================================================")
    # Load old benchmark data
    df = pd.read_csv(csv_path)
    print(f"Loaded existing results from {csv_path} ({len(df)} rows)")

    # Identify all unique sizes of N that need SciPy_MILP_HiGHS run
    # According to CSV, N ranges from 4 to 256
    sizes = sorted(df[df["Solver_Name"] == "SciPy_MILP_HiGHS"]["N"].unique())
    print(f"Sizes to run for SciPy_MILP_HiGHS: {sizes}")
    print(f"Parameters: repetitions={repetitions}, time_limit={time_limit}s")
    print("=========================================================")

    for n in sizes:
        print(f"\n---> Benchmarking SciPy_MILP_HiGHS for N = {n}...")
        problem = NQueensProblem(n)
        
        # We will bypass sizes >= 128 if they are known to take a lot of memory/time or let's run them and expect timeouts
        # SciPy's MILP HiGHS solver respects time_limit but for larger sizes (like 256), the constraint matrix itself
        # can be massive. Let's check size first.
        if n >= 256:
            # Let's skip N=256 for SciPy MILP because constructing a 65536 x 65536 dense/sparse array can raise OOM or take forever
            print(f"  Skipping N={n} for SciPy_MILP_HiGHS to prevent memory explosion/hang during model construction.")
            status = "SKIPPED_TIMEOUT_PREVENTION"
            success = False
            model_time_avg = 0.0
            solve_time_avg = 0.0
            peak_mem_avg = 0.0
            valid_str = "N/A"
        else:
            model_times = []
            solve_times = []
            success = False
            board = None
            peak_mems = []
            status = "OPT"
            
            try:
                for rep in range(repetitions):
                    PerformanceTracker.start_memory_tracking()
                    runner = MIP_NQueensRunner(n, solver_type="scipy_highs", time_limit=time_limit)
                    run_success, run_board, m_time, s_time, run_status = runner.solve()
                    peak_mem = PerformanceTracker.stop_memory_tracking()
                    
                    model_times.append(m_time)
                    solve_times.append(s_time)
                    peak_mems.append(peak_mem)
                    if rep == 0:
                        success = run_success
                        board = run_board
                        status = run_status
                
                model_time_avg = sum(model_times) / repetitions
                solve_time_avg = sum(solve_times) / repetitions
                peak_mem_avg = sum(peak_mems) / repetitions
                
                valid_str = "N/A"
                if success and board is not None:
                    is_valid, reason = problem.verify_solution(board)
                    valid_str = "VALID" if is_valid else f"INVALID: {reason}"
                    
            except Exception as e:
                print(f"  Error running SciPy_MILP_HiGHS for N={n}: {e}")
                status = f"ERROR: {str(e)}"
                success = False
                model_time_avg = 0.0
                solve_time_avg = 0.0
                peak_mem_avg = 0.0
                valid_str = "N/A"

        # Update the CSV rows for this size N and SciPy_MILP_HiGHS
        mask = (df["N"] == n) & (df["Solver_Name"] == "SciPy_MILP_HiGHS")
        if mask.any():
            idx = df[mask].index[0]
            df.at[idx, "Success"] = success
            df.at[idx, "Model_Construction_Time"] = model_time_avg
            df.at[idx, "Solving_Time"] = solve_time_avg
            df.at[idx, "Peak_Memory_Bytes"] = peak_mem_avg
            df.at[idx, "Status"] = status
            df.at[idx, "Solution_Validity"] = valid_str
            print(f"  Updated row in DataFrame: Success={success}, Status={status}, Construction={model_time_avg:.4f}s, Solving={solve_time_avg:.4f}s, Memory={peak_mem_avg/(1024*1024):.2f}MB, Validity={valid_str}")
        else:
            # If not exists, append a new row
            new_row = {
                "N": n,
                "Paradigm": "MIP",
                "Solver_Name": "SciPy_MILP_HiGHS",
                "Encoding": "N/A",
                "Success": success,
                "Model_Construction_Time": model_time_avg,
                "Solving_Time": solve_time_avg,
                "Variables": n * n,
                "Aux_Variables": 0,
                "Clauses": None,
                "Peak_Memory_Bytes": peak_mem_avg,
                "Status": status,
                "Solution_Validity": valid_str
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            print(f"  Added new row to DataFrame for N={n}")

    # Write back to CSV
    df.to_csv(csv_path, index=False)
    print(f"\nSaved updated results back to {csv_path}")
    print("=========================================================")

if __name__ == "__main__":
    run_scipy_only()
