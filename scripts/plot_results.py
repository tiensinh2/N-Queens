import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots():
    csv_path = os.path.join("..", "results", "benchmark_data.csv")
    results_dir = os.path.join("..", "results")
    if not os.path.exists(csv_path):
        csv_path = os.path.join("results", "benchmark_data.csv")
        results_dir = "results"
        if not os.path.exists(csv_path):
            print(f"Error: Could not find benchmark data at '{csv_path}'. Please run run_benchmark.py first.")
            return
        
    print("=========================================================")
    print(" VISUALIZING EXPERIMENTAL RESULTS: PLOTTING CHARTS       ")
    print("=========================================================")
    
    df = pd.read_csv(csv_path)
    sns.set_theme(style="whitegrid")
    
    # Lọc các bản ghi chạy thành công (Status = 'OPT' hoặc 'FEAS')
    df_opt = df[df["Status"].isin(["OPT", "FEAS"])].copy()
    
    # 1. CHART 1: SAT Encodings Solving Time Comparison
    sat_df = df_opt[df_opt["Paradigm"] == "SAT"].copy()
    if not sat_df.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=sat_df,
            x="N",
            y="Solving_Time",
            hue="Encoding",
            style="Encoding",
            markers=True,
            dashes=False,
            linewidth=2.0
        )
        plt.yscale("log")
        plt.title("SAT Encodings Comparison: Solving Time vs. Board Size N (Glucose3)", fontsize=13, fontweight='bold', pad=12)
        plt.xlabel("Board Size (N x N)", fontsize=11)
        plt.ylabel("Solving Time (seconds) - Log Scale", fontsize=11)
        plt.legend(title="AMO Encoding", frameon=True)
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "sat_encodings_time_comparison.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f" -> Exported SAT Encodings Time Comparison plot to: {plot_path}")

    # 2. CHART 2: SAT Encodings Clause Sizes (Number of Clauses vs N)
    if not sat_df.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=sat_df,
            x="N",
            y="Clauses",
            hue="Encoding",
            style="Encoding",
            markers=True,
            dashes=False,
            linewidth=2.0
        )
        plt.yscale("log")
        plt.title("SAT Encodings Clause Counts vs. Board Size N", fontsize=13, fontweight='bold', pad=12)
        plt.xlabel("Board Size (N x N)", fontsize=11)
        plt.ylabel("Number of CNF Clauses - Log Scale", fontsize=11)
        plt.legend(title="AMO Encoding", frameon=True)
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "sat_clauses_count_comparison.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f" -> Exported SAT Clauses Count Comparison plot to: {plot_path}")

    # 3. CHART 3: Cross-Paradigm Solving Time (Best SAT vs CP-SAT vs ILP CBC)
    best_sat = df_opt[(df_opt["Paradigm"] == "SAT") & (df_opt["Encoding"] == "seqcounter")].copy()
    if not best_sat.empty:
        best_sat["Solver_Label"] = "SAT_SeqCounter"
    
    others = df_opt[df_opt["Paradigm"].isin(["CP-SAT", "CPLEX_CP", "MIP"])].copy()
    if not others.empty:
        others["Solver_Label"] = others["Solver_Name"]
        
    cross_df = pd.concat([best_sat, others], ignore_index=True)
    
    if not cross_df.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=cross_df,
            x="N",
            y="Solving_Time",
            hue="Solver_Label",
            style="Solver_Label",
            markers=True,
            dashes=False,
            linewidth=2.0
        )
        plt.yscale("log")
        plt.title("Cross-Paradigm Comparison: Solving Time vs. Board Size N", fontsize=13, fontweight='bold', pad=12)
        plt.xlabel("Board Size (N x N)", fontsize=11)
        plt.ylabel("Solving Time (seconds) - Log Scale", fontsize=11)
        plt.legend(title="Solver Configuration", frameon=True)
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "cross_paradigm_time_comparison.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f" -> Exported Cross-Paradigm Solving Time plot to: {plot_path}")

    # 4. CHART 4: Peak Memory Usage Comparison
    if not cross_df.empty:
        cross_df["Peak_Memory_MB"] = cross_df["Peak_Memory_Bytes"] / (1024 * 1024)
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=cross_df,
            x="N",
            y="Peak_Memory_MB",
            hue="Solver_Label",
            style="Solver_Label",
            markers=True,
            dashes=False,
            linewidth=2.0
        )
        plt.title("Peak Memory Consumption vs. Board Size N", fontsize=13, fontweight='bold', pad=12)
        plt.xlabel("Board Size (N x N)", fontsize=11)
        plt.ylabel("Peak Traced Memory (MB)", fontsize=11)
        plt.legend(title="Solver Configuration", frameon=True)
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "peak_memory_comparison.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f" -> Exported Peak Memory Comparison plot to: {plot_path}")

    print("=========================================================")
    print(" PLOTTING COMPLETED! All charts have been saved successfully.")
    print("=========================================================")

if __name__ == "__main__":
    generate_plots()
