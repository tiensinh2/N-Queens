import os
import pandas as pd

def aggregate_and_summarize():
    csv_path = os.path.join("..", "results", "benchmark_data.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join("results", "benchmark_data.csv")
        if not os.path.exists(csv_path):
            print("Error: Could not find results/benchmark_data.csv. Run run_benchmark.py first.")
            return

    df = pd.read_csv(csv_path)
    
    print("=========================================================")
    print(" RESULTS AGGREGATION & SCIENTIFIC SUMMARY               ")
    print("=========================================================")
    
    # 1. So sánh chéo các Paradigms (Best SAT, CP-SAT, MIP CBC, MIP SCIP, MIP HiGHS)
    print("\n--- Paradigm Performance Summary (N vs. Solving Time) ---")
    
    # Lấy các hàng chạy thành công (Status == 'OPT')
    df_success = df[df["Status"].isin(["OPT", "FEAS"])].copy()
    
    # Chọn Sequential Counter làm đại diện cho SAT
    df_sat_seq = df_success[(df_success["Paradigm"] == "SAT") & (df_success["Encoding"] == "seqcounter")].copy()
    if not df_sat_seq.empty:
        df_sat_seq["Solver_Label"] = "SAT_SeqCounter"
        
    df_others = df_success[df_success["Paradigm"].isin(["CP-SAT", "CPLEX_CP", "MIP"])].copy()
    if not df_others.empty:
        df_others["Solver_Label"] = df_others["Solver_Name"]
        
    cross_df = pd.concat([df_sat_seq, df_others], ignore_index=True)
    
    if not cross_df.empty:
        pivot_df = cross_df.pivot_table(
            index="N",
            columns="Solver_Label",
            values="Solving_Time",
            aggfunc="mean"
        )
        print(pivot_df.to_string())
        
    # 2. So sánh số lượng Clause sinh ra giữa các SAT Encodings
    print("\n--- SAT Encodings Clause Sizes (CNF Complexity) ---")
    sat_df = df_success[df_success["Paradigm"] == "SAT"].copy()
    if not sat_df.empty:
        pivot_sat = sat_df.pivot_table(
            index="N",
            columns="Encoding",
            values="Clauses",
            aggfunc="first"
        )
        print(pivot_sat.to_string())
        
    print("\n=========================================================")
    print(" Aggregation completed. Data is ready for paper insertion.")
    print("=========================================================")

if __name__ == "__main__":
    aggregate_and_summarize()
