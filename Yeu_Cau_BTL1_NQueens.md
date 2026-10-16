# ĐỀ CƯƠNG CHI TIẾT & YÊU CẦU THỰC HIỆN BÀI TẬP LỚN SỐ 1
## MÔN CÁC VẤN ĐỀ HIỆN ĐẠI KHOA HỌC MÁY TÍNH (HK I NĂM HỌC 2026 – 2027)
### CHỦ ĐỀ: GIẢI BÀI TOÁN N-QUEENS BẰNG CÁC PHƯƠNG PHÁP CHÍNH XÁC (SAT, CP, ILP)

---

## 1. Thông Tin Chung & Bối Cảnh
*   **Môn học**: Các vấn đề hiện đại Khoa học máy tính (HK I Năm học 2026 – 2027).
*   **Hình thức thực hiện**: Cá nhân (Mỗi sinh viên chọn một trong hai chủ đề: Sudoku hoặc N-Queens. Tài liệu này đặc tả chi tiết theo hướng **N-Queens Solver**).
*   **Mục tiêu chính**: 
    1.  Nghiên cứu và triển khai mô hình hóa bài toán N-Queens sang định dạng **SAT (Boolean Satisfiability)** sử dụng các kỹ thuật mã hóa ràng buộc số lượng (Cardinality Encodings) tối ưu cho điều kiện At-Least-One (ALO) và At-Most-One (AMO).
    2.  Triển khai mô hình giải chính xác bằng **Lập trình tuyến tính nguyên (ILP/MIP)** và **Lập trình ràng buộc (CP)**.
    3.  Thực nghiệm so sánh hiệu năng quy mô lớn giữa các phương pháp giải và các solver thương mại/mã nguồn mở phổ biến.
    4.  Viết báo cáo khoa học chuẩn mực bằng LaTeX theo định dạng một cột của Nhà xuất bản Elsevier (`cas-sc`), dựa trên cấu trúc bài báo mẫu thực tế của Bộ môn.

---

## 2. Yêu Cầu Kỹ Thuật Chi Tiết

### 2.1. Hướng Tiếp Cận 1: SAT Encoding & Solving
Sinh viên tiến hành mã hóa bài toán N-Queens thành dạng hội chuẩn thức (CNF) và giải quyết thông qua thư viện `PySAT`.

#### A. Các Ràng Buộc Cơ Bản của N-Queens:
Đặt biến Boolean $x_{i, j}$ là `True` nếu đặt quân hậu ở ô hàng $i$, cột $j$ (với $0 \le i, j < N$).
1.  **Ràng buộc Hàng (Row Constraints)**:
    *   Mỗi hàng có ít nhất một quân hậu (ALO): $\bigwedge_{i=0}^{N-1} \left( \bigvee_{j=0}^{N-1} x_{i, j} \right)$.
    *   Mỗi hàng có nhiều nhất một quân hậu (AMO): $\bigwedge_{i=0}^{N-1} \text{AMO}(x_{i, 0}, x_{i, 1}, \dots, x_{i, N-1})$.
2.  **Ràng buộc Cột (Column Constraints)**:
    *   Mỗi cột có ít nhất một quân hậu (ALO): $\bigwedge_{j=0}^{N-1} \left( \bigvee_{i=0}^{N-1} x_{i, j} \right)$.
    *   Mỗi cột có nhiều nhất một quân hậu (AMO): $\bigwedge_{j=0}^{N-1} \text{AMO}(x_{0, j}, x_{1, j}, \dots, x_{N, j})$.
3.  **Ràng buộc Đường chéo xuôi (Diagonal Constraints)**:
    *   Mỗi đường chéo xuôi (hàng trừ cột bằng hằng số $k$) có nhiều nhất một quân hậu: $\text{AMO}(\{x_{i, j} \mid i - j = k\})$.
4.  **Ràng buộc Đường chéo ngược (Anti-diagonal Constraints)**:
    *   Mỗi đường chéo ngược (tổng hàng và cột bằng hằng số $k$) có nhiều nhất một quân hậu: $\text{AMO}(\{x_{i, j} \mid i + j = k\})$.

#### B. Các Kỹ Thuật Mã Hóa Ràng Buộc Cardinality (AMO/ALO):
Khuyến khích sinh viên sử dụng trực tiếp các thuật toán mã hóa C++ tối ưu thông qua lớp `pysat.card.CardEnc` của PySAT để sinh các clause logic, bao gồm 6 cấu hình:
1.  **Pairwise Encoding (Naive)**: Mã hóa từng cặp, sinh ra $O(M^2)$ clauses cho tập $M$ biến, không biến phụ. Gây bùng nổ số lượng clause khi $N$ lớn.
2.  **Binary Encoding (Bitwise)**: Sử dụng $\lceil \log_2 M \rceil$ biến phụ để biểu diễn chỉ số nhị phân của biến nhận giá trị True. Sinh ra $O(M \log M)$ clauses.
3.  **Sequential Counter Encoding**: Sử dụng thanh ghi dịch tích lũy số lượng quân hậu, sinh ra $O(M)$ clauses và biến phụ tuyến tính.
4.  **Commander Encoding**: Chia nhỏ các biến thành nhóm (commander) trung gian. Trong PySAT, phương pháp này được cấu hình ánh xạ tối ưu về thuật toán Tree-based `totalizer` (`EncType.totalizer`).
5.  **Product Encoding (Mã hóa tích)**: Sắp xếp các biến thành lưới 2D trung gian để mã hóa. Trong PySAT, phương pháp này được ánh xạ tối ưu về `mtotalizer` (`EncType.mtotalizer`).
6.  **Ladder Encoding**: Mã hóa dạng bậc thang nối tiếp (`EncType.ladder`).

#### C. Các SAT Solvers Trải Nghiệm:
Sinh viên cấu hình và so sánh kết quả trên các SAT solver tích hợp sẵn trong PySAT:
*   **CaDiCaL** (phiên bản khuyến nghị: `cadical195`)
*   **Glucose** (các bản `glucose3`, `glucose4`)
*   **Kissat** / **CryptoMiniSAT** / **Maplesat** (nếu hệ thống hỗ trợ)

---

### 2.2. Hướng Tiếp Cận 2: Constraint Programming (CP)
Sử dụng mô hình lập trình ràng buộc cấp cao giúp phát biểu bài toán tự nhiên thông qua các ràng buộc toàn cục (Global Constraints):
*   **Mô hình hóa**: Định nghĩa $N$ biến nguyên $Q_i \in [0, N-1]$ tương ứng với vị trí cột của quân hậu ở hàng $i$.
*   **Ràng buộc**:
    *   Không trùng cột: $\text{AllDifferent}(Q_0, Q_1, \dots, Q_{N-1})$.
    *   Không trùng chéo xuôi: $\text{AllDifferent}(Q_0 - 0, Q_1 - 1, \dots, Q_{N-1} - (N-1))$.
    *   Không trùng chéo ngược: $\text{AllDifferent}(Q_0 + 0, Q_1 + 1, \dots, Q_{N-1} + (N-1))$.
*   **Thư viện tích hợp**:
    1.  **Google OR-Tools (CP-SAT Solver)**: Sử dụng `ortools.sat.python.cp_model`.
    2.  **IBM ILOG CPLEX CP Optimizer**: Sử dụng `docplex.cp` (yêu cầu cài đặt CPLEX local hoặc kết nối êm dịu).

---

### 2.3. Hướng Tiếp Cận 3: Lập Trình Tuyến Tính Nguyên (ILP/MIP)
Quy bài toán về dạng tối ưu hóa tuyến tính với các biến quyết định nhị phân $x_{i, j} \in \{0, 1\}$.
*   **Hàm mục tiêu**: Tìm nghiệm khả thi tuyến tính (Feasibility):
    $$\text{Minimize} \quad 0$$
*   **Các ràng buộc tuyến tính dạng ma trận**:
    *   $\sum_{j=0}^{N-1} x_{i, j} = 1 \quad \forall i \in \{0, \dots, N-1\}$ (Hàng)
    *   $\sum_{i=0}^{N-1} x_{i, j} = 1 \quad \forall j \in \{0, \dots, N-1\}$ (Cột)
    *   $\sum_{i - j = k} x_{i, j} \le 1 \quad \forall k \in \{-(N-1), \dots, N-1\}$ (Đường chéo xuôi)
    *   $\sum_{i + j = k} x_{i, j} \le 1 \quad \forall k \in \{0, \dots, 2N-2\}$ (Đường chéo ngược)
*   **Bộ giải (Solvers) tích hợp**:
    *   **Commercial Solvers**: Gurobi Optimizer (`gurobipy`), IBM ILOG CPLEX MIP (`docplex.mp`).
    *   **Open-source Solvers**: HiGHS (`highspy`), SCIP (`pyscipopt`), CBC (`ortools_cbc` hoặc `mip`).
    *   *Yêu cầu*: Các solver thương mại chưa được cài đặt hoặc thiếu license phải được bắt ngoại lệ (`try-except`) một cách êm đẹp và ghi nhận trạng thái (`NOT_INSTALLED`, `NO_LICENSE`) thay vì gây sập chương trình.

---

## 3. Quy Trình Thực Nghiệm & Đo Lường
Để đảm bảo tính khách quan và khoa học, hệ thống benchmark tự động cần được thiết lập:

### 3.1. Cấu Hình Benchmark (`configs/benchmark_config.yaml`)
Cho phép điều chỉnh các tham số thực nghiệm một cách linh hoạt:
*   **Board Sizes ($N$)**: Thử nghiệm từ quy mô nhỏ ($N=4, 8, 16$) đến quy mô trung bình và lớn ($N=25, 50, 100, 200, 500, 1000$).
*   **Repetitions (Số lần lặp)**: Chạy mỗi cấu hình nhiều lần (ví dụ: 3-5 lần) để lấy trung bình, loại bỏ sai số do hệ điều hành.
*   **Timeout (Thời gian giới hạn)**: Giới hạn tối đa cho mỗi lượt giải (ví dụ: 300 giây theo chuẩn hoặc 3600 giây tùy cấu hình phần cứng).
*   **Memory Limit**: Giới hạn bộ nhớ tiêu thụ để tránh tràn RAM hệ thống.

### 3.2. Chỉ Số Đo Lường (Metrics)
*   **Thời gian khởi tạo (Model Construction Time)**: Thời gian thiết lập mô hình và sinh các mệnh đề/ràng buộc.
*   **Thời gian giải (Solving CPU/Wall Time)**: Chỉ tính riêng thời gian xử lý của solver core.
*   **Bộ nhớ đỉnh (Peak Memory Usage)**: Sử dụng thư viện hệ thống (như `tracemalloc` trong Python) để đo chính xác lượng RAM đỉnh điểm trong suốt quá trình chạy.
*   **Độ phức tạp logic (Logic Complexity)**: 
    *   Đối với SAT: Số lượng biến và số lượng clause sinh ra.
    *   Đối với MIP/CP: Số lượng biến nguyên/nhị phân và số lượng ràng buộc (constraints).
*   **Trạng thái kết quả (Status)**: Ghi nhận chính xác `OPT` (đã chứng minh tối ưu/tìm thấy nghiệm), `TIMEOUT` (hết giờ), `NOT_INSTALLED` / `NO_LICENSE`.

### 3.3. Tổng Hợp & Trực Quan Hóa (Aggregation & Visualizations)
*   Tự động xuất kết quả thô ra file CSV (`results/benchmark_data.csv`).
*   Script post-processing tự động đọc file CSV, tính toán trung bình, xuất bảng so sánh Markdown/LaTeX.
*   **Trực quan hóa đồ thị**: Sinh viên được khuyến khích sử dụng công cụ trực quan hóa nghiên cứu tự động:
    👉 Nền tảng trực tuyến: **[CNS Plots Visualizer](https://cnsplots.farid.one/latest/)** (Kéo thả file CSV kết quả `benchmark_data.csv` để sinh các biểu đồ khoa học tương tác ECharts/Matplotlib tức thì).
*   Sử dụng script cục bộ hoặc công cụ trực tuyến để vẽ và xuất 4 biểu đồ khoa học chất lượng cao phục vụ chèn báo cáo LaTeX:
    1.  Biểu đồ đường (Line plot) so sánh thời gian giải (Solving Time) theo thang đo Logarit trục Y ứng với kích thước $N$ (trục X).
    2.  Biểu đồ đường (Line plot) so sánh bộ nhớ đỉnh (Peak Memory) theo kích thước $N$.
    3.  Biểu đồ cột (Bar plot) so sánh số lượng clause sinh ra giữa các kỹ thuật SAT Encoders khi $N$ tăng dần (làm rõ sự bùng nổ của Pairwise).
    4.  Biểu đồ cột (Bar plot) so sánh số lượng biến phụ sinh ra giữa các SAT Encoders.

---

## 4. Hướng Dẫn Viết Báo Cáo Khoa Học (LaTeX Elsevier `cas-sc`)
Báo cáo của sinh viên phải được trình bày như một bài báo nghiên cứu khoa học chuẩn Elsevier quốc tế. Sinh viên có thể tham khảo trực tiếp cấu trúc mô hình hóa toán học và thực nghiệm từ bài báo nghiên cứu **2DBMP (Two-Dimensional Bandwidth Minimization Problem)** của PGS. TS. Tô Văn Khánh và cộng sự (chi tiết cấu trúc lưu tại `template_extracted.txt`).

### 4.1. Khởi Tạo LaTeX
Sử dụng template chính thức của Elsevier Single-Column (`cas-sc`):
```latex
\documentclass[a4paper,fleqn]{cas-sc}
\usepackage[numbers]{natbib}
\usepackage{booktabs} % Hỗ trợ vẽ bảng chuẩn khoa học (không kẻ dọc)
\usepackage{amsmath,amssymb,amsfonts} % Công thức toán học chuyên sâu
\usepackage{graphicx} % Chèn biểu đồ ảnh PNG
```

### 4.2. Cấu Trúc Đề Xuất Cho Báo Cáo:
1.  **Title (Tiêu đề)**: Mang tính học thuật, nhấn mạnh vào thực nghiệm so sánh. 
    *   *Ví dụ*: `A Rigorous Empirical Benchmark of SAT, Constraint Programming, and Integer Linear Programming on the N-Queens Problem`.
2.  **Abstract (Tóm tắt)**: 150-250 từ, cô đọng đầy đủ bối cảnh, mục tiêu, phương pháp (5+ SAT Encoders, CP, ILP), kết quả thực nghiệm then chốt (solver nào thống trị, giới hạn mở rộng của từng phương pháp).
3.  **Introduction (Mở đầu)**: Giới thiệu bài toán N-Queens dưới góc độ bài toán thỏa mãn ràng buộc phi tuyến (CSP). Giới thiệu sự dịch chuyển từ các thuật toán quay lui cổ điển sang các solver đa dụng hiện đại (SAT, CP, ILP). Nêu rõ đóng góp chính của đề tài.
4.  **Paradigm Formulations (Mô hình hóa)**: Trình bày chi tiết công thức toán học của mô hình ILP và CP (sử dụng các khối phương trình LaTeX toán học đẹp mắt).
5.  **Proposed SAT-Based Approach (Mã hóa SAT)**: Trình bày cơ chế ánh xạ biến sang chỉ số 1D: $\text{id}(i, j) = i \times N + j + 1 \in [1, N^2]$. Phân tích toán học các giải thuật mã hóa ALO/AMO (Pairwise, Binary, Sequential Counter, Commander, Product, Ladder).
6.  **Computational Experiments (Thực nghiệm & Phân tích)**:
    *   Mô tả môi trường phần cứng, phiên bản phần mềm (CaDiCaL, OR-Tools, Gurobi, CPLEX).
    *   *Bảng 1*: So sánh chi tiết hiệu năng giữa các SAT Encoders (Variables, Clauses, Solving Time). Phân tích tại sao Pairwise bị bùng nổ mệnh đề bậc ba $O(N^3)$ trên toàn bàn cờ khi $N \ge 32$.
    *   *Bảng 2*: So sánh liên phương pháp (SAT vs. OR-Tools CP-SAT vs. CPLEX CP vs. Gurobi MIP vs. CPLEX MIP).
    *   *Phân tích chuyên sâu*: Thảo luận cơ chế lọc miền trị và lan truyền ràng buộc cực mạnh của thuật toán `AllDifferent` trong CP giúp CP-SAT vượt trội so với sự nặng nề của nới lỏng thực (LP relaxation) trong MIP trên bài toán thuần logic này.
7.  **Conclusion & Future Work (Kết luận)**: Đúc kết phát hiện và hướng mở rộng.
8.  **Data Availability (Tính khả dụng của dữ liệu)**: Cung cấp link Github công khai chứa toàn bộ mã nguồn và dữ liệu thực nghiệm thô để đảm bảo tính tái lặp khoa học (reproducibility).
9.  **References (Tài liệu tham khảo)**: Trích dẫn chuẩn BibTeX (PySAT, các bài báo của Sinz về Sequential Counter, các solver Cadical/Glucose).

---

## 5. Danh Mục Sản Phẩm Bàn Giao (Deliverables)
Sản phẩm của bài tập lớn phải được tổ chức khoa học trong một thư mục nén chứa các thành phần sau:

```
N-Queen/
├── configs/
│   └── benchmark_config.yaml         # File cấu hình board kích thước, số lần lặp, timeout
├── src/
│   ├── __init__.py
│   ├── problem.py                    # Đại diện bài toán, logic map biến và kiểm tra nghiệm chéo
│   ├── metrics.py                    # Trình đo đạc thời gian và peak memory (tracemalloc)
│   ├── benchmark.py                  # Điều phối chạy benchmark tự động
│   ├── sat/
│   │   ├── __init__.py
│   │   ├── runner.py                 # Wrapper quản lý gọi SAT solver và giải mã nghiệm
│   │   ├── solver_registry.py        # Quét các SAT solver khả dụng trong PySAT
│   │   └── encoders/
│   │       ├── __init__.py           # Đăng ký 6 loại mã hóa Cardinality qua CardEnc
│   │       ├── pairwise.py
│   │       ├── binary.py
│   │       ├── seq_counter.py
│   │       ├── commander.py
│   │       ├── product.py
│   │       └── ladder.py
│   ├── mip/
│   │   ├── __init__.py
│   │   └── runner.py                 # Mô hình hóa ILP hỗ trợ CBC, SCIP, HiGHS, Gurobi, CPLEX
│   └── cp/
│       ├── __init__.py
│       └── runner.py                 # Mô hình hóa CP hỗ trợ Google CP-SAT và CPLEX CP
├── tests/
│   ├── test_encoders.py              # Unit tests kiểm nghiệm tính đúng đắn logic của các bộ mã hóa
│   └── test_solvers.py               # Unit tests kiểm nghiệm lời giải của các solver
├── scripts/
│   ├── run_benchmark.py              # CLI script chạy thực nghiệm tự động từ file config
│   ├── aggregate_results.py          # CLI script tổng hợp kết quả CSV ra bảng báo cáo khoa học
│   └── plot_results.py               # CLI script đọc kết quả CSV vẽ 4 biểu đồ khoa học
├── results/
│   ├── benchmark_data.csv            # File dữ liệu thô thu được từ thực nghiệm
│   ├── solving_time_comparison.png   # Biểu đồ so sánh thời gian giải giữa các solver
│   ├── peak_memory_comparison.png    # Biểu đồ so sánh bộ nhớ đỉnh
│   ├── sat_clauses_comparison.png    # Biểu đồ so sánh số lượng clause sinh ra của các encoders
│   └── sat_variables_comparison.png  # Biểu đồ so sánh số lượng biến phụ sinh ra
├── report/
│   ├── references.bib                # Danh mục tài liệu tham khảo BibTeX
│   ├── report.tex                    # Mã nguồn báo cáo khoa học bằng LaTeX
│   └── report.pdf                    # Báo cáo khoa học hoàn chỉnh đã biên dịch
├── requirements.txt                  # Danh sách thư viện Python cần cài đặt
├── README.md                         # Hướng dẫn chi tiết cách thiết lập môi trường và chạy tái lập kết quả
└── Yeu_Cau_BTL1_NQueens.md           # File yêu cầu và đặc tả này
```

---
*Tài liệu này được biên soạn dựa trên các yêu cầu chính thức từ bài tập lớn số 1 môn Các vấn đề hiện đại KHMT, tích hợp mẫu bài báo khoa học chuẩn Elsevier của Bộ môn.*
