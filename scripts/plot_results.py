import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cnsplots as cns

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
    print(" VISUALIZING EXPERIMENTAL RESULTS VIA CNSPLOTS (BRIGHT)  ")
    print("=========================================================")
    
    df = pd.read_csv(csv_path)
    
    # Ép buộc cấu hình phông nền sáng, đồng bộ màu trắng tinh khiết (không transparent) cho mọi đồ thị
    # Điều này giúp ảnh luôn sáng rõ và đồng bộ trên mọi giao diện (kể cả khi xem ở Dark Mode của VS Code/GitHub)
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['savefig.transparent'] = False
    
    # Lọc các bản ghi chạy thành công (Status = 'OPT' hoặc 'FEAS')
    df_opt = df[df["Status"].isin(["OPT", "FEAS"])].copy()
    
    # 1. CHART 1: SAT Encodings Solving Time Comparison
    sat_df = df_opt[df_opt["Paradigm"] == "SAT"].copy()
    if not sat_df.empty:
        # Sử dụng cnsplots canvas với bảng màu sáng ECharts cực kỳ nổi bật
        cns.figure(300, 200, color_cycle='ECharts')
        ax = plt.gca()
        sns.lineplot(
            ax=ax,
            data=sat_df,
            x="N",
            y="Solving_Time",
            hue="Encoding",
            style="Encoding",
            markers=True,
            dashes=False,
            linewidth=2.5,
            markersize=7
        )
        ax.set_yscale("log")
        ax.set_title("SAT Encodings Comparison: Solving Time vs. Board Size N", fontsize=11, fontweight='bold', pad=10)
        ax.set_xlabel("Board Size (N x N)", fontsize=9, fontweight='bold')
        ax.set_ylabel("Solving Time (seconds) - Log Scale", fontsize=9, fontweight='bold')
        ax.legend(title="AMO Encoding", frameon=True, facecolor='white', edgecolor='#dddddd', loc="best")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#e0e0e0')
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "sat_encodings_time_comparison.png")
        cns.save(plot_path)
        plt.close()
        print(f" -> Exported [CNSPlots] SAT Encodings Time Comparison to: {plot_path}")

    # 2. CHART 2: SAT Encodings Clause Sizes (Number of Clauses vs N)
    if not sat_df.empty:
        cns.figure(300, 200, color_cycle='ECharts')
        ax = plt.gca()
        sns.lineplot(
            ax=ax,
            data=sat_df,
            x="N",
            y="Clauses",
            hue="Encoding",
            style="Encoding",
            markers=True,
            dashes=False,
            linewidth=2.5,
            markersize=7
        )
        ax.set_yscale("log")
        ax.set_title("SAT Encodings Clause Counts vs. Board Size N", fontsize=11, fontweight='bold', pad=10)
        ax.set_xlabel("Board Size (N x N)", fontsize=9, fontweight='bold')
        ax.set_ylabel("Number of CNF Clauses - Log Scale", fontsize=9, fontweight='bold')
        ax.legend(title="AMO Encoding", frameon=True, facecolor='white', edgecolor='#dddddd', loc="best")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#e0e0e0')
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "sat_clauses_count_comparison.png")
        cns.save(plot_path)
        plt.close()
        print(f" -> Exported [CNSPlots] SAT Clauses Count Comparison to: {plot_path}")

    # 3. CHART 3: Cross-Paradigm Solving Time (Best SAT vs CP-SAT vs ILP CBC)
    best_sat = df_opt[(df_opt["Paradigm"] == "SAT") & (df_opt["Encoding"] == "seqcounter")].copy()
    if not best_sat.empty:
        best_sat["Solver_Label"] = "SAT_SeqCounter"
    
    others = df_opt[df_opt["Paradigm"].isin(["CP-SAT", "CPLEX_CP", "MIP"])].copy()
    if not others.empty:
        others["Solver_Label"] = others["Solver_Name"]
        
    cross_df = pd.concat([best_sat, others], ignore_index=True)
    
    if not cross_df.empty:
        cns.figure(300, 200, color_cycle='ECharts')
        ax = plt.gca()
        sns.lineplot(
            ax=ax,
            data=cross_df,
            x="N",
            y="Solving_Time",
            hue="Solver_Label",
            style="Solver_Label",
            markers=True,
            dashes=False,
            linewidth=2.5,
            markersize=7
        )
        ax.set_yscale("log")
        ax.set_title("Cross-Paradigm Comparison: Solving Time vs. Board Size N", fontsize=11, fontweight='bold', pad=10)
        ax.set_xlabel("Board Size (N x N)", fontsize=9, fontweight='bold')
        ax.set_ylabel("Solving Time (seconds) - Log Scale", fontsize=9, fontweight='bold')
        ax.legend(title="Solver Configuration", frameon=True, facecolor='white', edgecolor='#dddddd', loc="best")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#e0e0e0')
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "cross_paradigm_time_comparison.png")
        cns.save(plot_path)
        plt.close()
        print(f" -> Exported [CNSPlots] Cross-Paradigm Solving Time to: {plot_path}")

    # 4. CHART 4: Peak Memory Usage Comparison
    if not cross_df.empty:
        cross_df["Peak_Memory_MB"] = cross_df["Peak_Memory_Bytes"] / (1024 * 1024)
        
        cns.figure(300, 200, color_cycle='ECharts')
        ax = plt.gca()
        sns.lineplot(
            ax=ax,
            data=cross_df,
            x="N",
            y="Peak_Memory_MB",
            hue="Solver_Label",
            style="Solver_Label",
            markers=True,
            dashes=False,
            linewidth=2.5,
            markersize=7
        )
        ax.set_title("Peak Memory Consumption vs. Board Size N", fontsize=11, fontweight='bold', pad=10)
        ax.set_xlabel("Board Size (N x N)", fontsize=9, fontweight='bold')
        ax.set_ylabel("Peak Traced Memory (MB)", fontsize=9, fontweight='bold')
        ax.legend(title="Solver Configuration", frameon=True, facecolor='white', edgecolor='#dddddd', loc="best")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#e0e0e0')
        plt.tight_layout()
        
        plot_path = os.path.join(results_dir, "peak_memory_comparison.png")
        cns.save(plot_path)
        plt.close()
        print(f" -> Exported [CNSPlots] Peak Memory Comparison to: {plot_path}")

    print("=========================================================")
    print(" PLOTTING COMPLETED! CNSPlots updated all graphics.")
    print("=========================================================")

if __name__ == "__main__":
    generate_plots()
