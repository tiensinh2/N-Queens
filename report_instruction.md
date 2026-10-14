# HƯỚNG DẪN VIẾT BÁO CÁO KHOA HỌC BÀI TẬP LỚN SỐ 1
## ĐỀ TÀI: GIẢI CHÍNH XÁC BÀI TOÁN N-QUEENS (SAT VS. CP VS. ILP)
### THEO CHUẨN ĐỊNH DẠNG ELSEVIER LATEX (`cas-sc`)

Tài liệu này hướng dẫn chi tiết cách viết báo cáo Bài tập lớn số 1 dưới dạng một bài báo khoa học chuẩn quốc tế, dựa trên cấu trúc mẫu đã được trích xuất từ tài liệu mẫu của Bộ môn (bài báo 2DBMP của Thầy Tô Văn Khánh và cộng sự).

---

## 1. THÔNG TIN CHUNG VỀ KHỞI TẠO LATEX
*   **Template sử dụng**: Định dạng một cột chuẩn của nhà xuất bản Elsevier (`cas-sc`). Bạn có thể tải mẫu này trên Overleaf bằng cách tìm kiếm cụm từ `"Elsevier's CAS Single Column Template"`.
*   **Khai báo đầu file `.tex`**:
    ```latex
    \documentclass[a4paper,fleqn]{cas-sc}
    \usepackage[numbers]{natbib}
    \usepackage{booktabs} % Hỗ trợ vẽ bảng chuẩn khoa học
    \usepackage{amsmath,amssymb,amsfonts} % Hỗ trợ gõ công thức toán học
    \usepackage{graphicx} % Hỗ trợ chèn biểu đồ dạng ảnh
    ```

---

## 2. CẤU TRÚC CHI TIẾT CỦA BÁO CÁO KHOA HỌC (SECTION-BY-SECTION)

### TITLE, AUTHORS & ABSTRACT
*   **Title (Tiêu đề)**: Nên đặt tiêu đề mang tính chất nghiên cứu, thực nghiệm và so sánh.
    *   *Gợi ý*: `An Empirical Performance Benchmark of SAT, Constraint Programming, and Integer Linear Programming on the N-Queens Problem`
*   **Author & Affiliations**: Ghi rõ thông tin cá nhân, mã số sinh viên, khoa, trường và email định dạng của nhà trường.
*   **Keywords (Từ khóa)**: `N-Queens problem`, `SAT solving`, `Constraint Programming`, `Integer Linear Programming`, `Benchmark`.
*   **Abstract (Tóm tắt)**: Viết một đoạn văn duy nhất từ 150 - 250 từ bao gồm:
    1.  *Context*: Tầm quan trọng của bài toán đặt hậu N-Queens trong lý thuyết tối ưu hóa tổ hợp.
    2.  *Objective*: Mục tiêu của nghiên cứu là đánh giá so sánh hiệu năng của 3 hướng tiếp cận giải quyết chính xác lớn: SAT, CP, và ILP.
    3.  *Methods*: Chúng tôi đã lập trình mô hình hóa N-Queens bằng các hệ thức logic (với 5 phương pháp mã hóa At-Most-One gồm Pairwise, Binary, Sequential Counter, Commander, Product), mô hình lập trình ràng buộc cấp cao (sử dụng OR-Tools, CPLEX CP), và mô hình quy hoạch tuyến tính nguyên tuyến tính (Gurobi, CPLEX MIP).
    4.  *Key Results*: Tóm tắt kết quả nổi bật nhất từ thực nghiệm (ví dụ: solver nào nhanh nhất, kích cỡ $N$ lớn nhất từng phương pháp giải quyết được, sự bùng nổ số lượng mệnh đề của mã hóa Pairwise).

---

### SECTION 1: INTRODUCTION (MỞ ĐẦU)
*   **Mục tiêu**: Dẫn dắt người đọc vào bài toán N-Queens và nêu rõ đóng góp của bạn.
*   **Nội dung cần viết**:
    *   *Đặt vấn đề*: Mô tả bài toán N-Queens (bàn cờ $N \times N$, đặt $N$ quân hậu không tấn công nhau). Giải thích tại sao bài toán này đại diện cho lớp các bài toán thỏa mãn ràng buộc (CSP) phi tuyến.
    *   *Lịch sử nghiên cứu*: Tóm tắt các phương pháp giải quyết cổ điển (thuật toán quay lui Backtracking, tìm kiếm cục bộ Heuristics như Hill Climbing, Min-Conflicts). Nêu ra nhược điểm của chúng (quay lui bị chậm khi $N$ tăng, heuristics không chứng minh được tính tối ưu/vô nghiệm).
    *   *Xu hướng hiện đại (Modern General-Purpose Solvers)*: Giới thiệu 3 xu hướng giải chính xác phổ biến là SAT Solving, Constraint Programming (CP), và Integer Linear Programming (ILP).
    *   *Mục tiêu & Đóng góp*: Nêu rõ các đóng góp chính của bài làm:
        - Triển khai và so sánh hiệu năng của 5 kỹ thuật mã hóa AMO (At-Most-One) cho SAT.
        - Triển khai mô hình toán học ILP và mô hình ràng buộc CP.
        - Benchmark toàn diện trên quy mô lớn từ $N=4$ đến $N=1000$ để tìm ra giới hạn mở rộng (scalability) của từng solver.
    *   *Bố cục bài báo*: *"The remainder of this paper is organized as follows. Section 2 reviews the mathematical models of ILP and CP. Section 3 details the SAT encoding formulations. Section 4 presents the experimental evaluation, and Section 5 concludes the paper."*

---

### SECTION 2: PARADIGM FORMULATIONS (MÔ HÌNH HÓA TOÁN HỌC)
Trình bày hai phương pháp mô hình hóa chính xác CP và ILP để người đọc nắm được cách thiết lập ràng buộc cấp cao.

#### 2.1. Integer Linear Programming (ILP) Formulation
*   **Biến quyết định**: Biến nhị phân $x_{i,j} \in \{0, 1\}$ ứng với mỗi ô bàn cờ ($0 \le i, j < N$).
*   **Hàm mục tiêu**: Bài toán là bài toán tìm nghiệm khả thi (feasibility), do đó hàm mục tiêu có thể đặt giả định là:
    $$\text{Minimize} \quad 0$$
*   **Hệ phương trình ràng buộc tuyến tính (Gõ bằng LaTeX math block)**:
    *   *Ràng buộc Hàng (Row Constraint)*: Mỗi hàng có đúng một quân hậu:
        $$\sum_{j=0}^{N-1} x_{i,j} = 1 \quad \forall i \in \{0, \dots, N-1\}$$
    *   *Ràng buộc Cột (Column Constraint)*: Mỗi cột có đúng một quân hậu:
        $$\sum_{i=0}^{N-1} x_{i,j} = 1 \quad \forall j \in \{0, \dots, N-1\}$$
    *   *Ràng buộc Đường chéo xuôi (Diagonal Constraint)*: Nhiều nhất một quân hậu trên mỗi đường chéo xuôi (xác định bởi hàng trừ cột bằng hằng số $k$):
        $$\sum_{i=0}^{N-1} x_{i, i-k} \le 1 \quad \forall k \in \{-(N-1), \dots, N-1\} \quad (\text{với } 0 \le i-k < N)$$
    *   *Ràng buộc Đường chéo ngược (Anti-Diagonal Constraint)*: Nhiều nhất một quân hậu trên mỗi đường chéo ngược (xác định bởi tổng hàng và cột bằng hằng số $k$):
        $$\sum_{i=0}^{N-1} x_{i, k-i} \le 1 \quad \forall k \in \{0, \dots, 2N-2\} \quad (\text{với } 0 \le k-i < N)$$

#### 2.2. Constraint Programming (CP) Formulation
*   **Biến quyết định**: Sử dụng $N$ biến nguyên đại diện cho vị trí cột của quân hậu ở mỗi hàng: $Q_i \in [0, N-1]$ với $i \in \{0, \dots, N-1\}$.
*   **Hệ ràng buộc toàn cục (Global Constraints)**:
    *   *Không trùng hàng & cột*: Nhờ định nghĩa $Q_i$ nên các hàng đã tự động phân biệt. Để đảm bảo không có hai quân hậu nằm trên cùng một cột, ta áp dụng ràng buộc `AllDifferent`:
        $$\text{AllDifferent}(Q_0, Q_1, \dots, Q_{N-1})$$
    *   *Không trùng chéo xuôi*: Khoảng cách cột không được bằng khoảng cách hàng: $Q_i - Q_j \ne i - j \implies Q_i - i \ne Q_j - j$. Biểu diễn dạng ràng buộc:
        $$\text{AllDifferent}(Q_0 - 0, Q_1 - 1, \dots, Q_{N-1} - (N-1))$$
    *   *Không trùng chéo ngược*: $Q_i + i \ne Q_j + j$. Biểu diễn dạng ràng buộc:
        $$\text{AllDifferent}(Q_0 + 0, Q_1 + 1, \dots, Q_{N-1} + (N-1))$$

---

### SECTION 3: PROPOSED SAT-BASED APPROACH (MÔ HÌNH HÓA SAT)
Đây là phần trọng tâm khoa học của bài nghiên cứu, giải thích cách biến đổi các ràng buộc sang logic Boolean.

#### 3.1. Variable Mapping (Ánh xạ biến)
Mô tả cách ánh xạ biến Boolean 2D $x_{i,j}$ thành chỉ số 1D trong SAT:
$$\text{id}(i, j) = i \times N + j + 1 \quad \in \{1, \dots, N^2\}$$

#### 3.2. ALO & AMO Decomposition (Phân rã ALO và AMO)
Giải thích rằng các ràng buộc hàng và cột (phải có đúng 1 quân hậu) được phân rã thành hai phần logic độc lập:
$$\text{Exactly-One} \equiv \text{At-Least-One (ALO)} \land \text{At-Most-One (AMO)}$$
*   **ALO**: Biểu diễn bằng mệnh đề tuyển đơn giản:
    $$(x_{i,0} \lor x_{i,1} \lor \dots \lor x_{i,N-1})$$
*   **AMO**: Nhiều nhất một biến được nhận giá trị True.

#### 3.3. AMO Encoding Formulations (Các kỹ thuật mã hóa AMO)
Trình bày chi tiết lý thuyết toán học của các kỹ thuật mã hóa mà bạn đã lập trình:
1.  **Pairwise Encoding (Naive)**: 
    *   Công thức: $\bigwedge_{0 \le a < b < M} (\neg y_a \lor \neg y_b)$
    *   *Nhận xét*: Số lượng mệnh đề sinh ra tăng theo hàm bậc hai $O(M^2) = \frac{M(M-1)}{2}$. Không sử dụng biến phụ.
2.  **Binary Encoding (Bitwise)**:
    *   Sử dụng $k = \lceil \log_2 M \rceil$ biến phụ $b_0, \dots, b_{k-1}$ đại diện cho mã nhị phân của chỉ số biến nhận giá trị True.
    *   *Nhận xét*: Số lượng mệnh đề sinh ra là $O(M \log M)$. Sử dụng ít biến phụ.
3.  **Sequential Counter Encoding**:
    *   Sử dụng $M-1$ biến phụ $s_0, \dots, s_{M-2}$ làm thanh ghi trạng thái tích lũy số lượng quân hậu đã phát hiện.
    *   *Nhận xét*: Số lượng mệnh đề sinh ra là tuyến tính $O(M)$. Giúp giảm tải đáng kể cho solver khi kích thước bàn cờ lớn.
4.  **Commander / Product Encoding**:
    *   Giải thích nguyên lý hoạt động (chia nhóm các biến, sử dụng biến trung gian) giúp tối ưu hóa số lượng mệnh đề.

---

### SECTION 4: COMPUTATIONAL EXPERIMENTS (THỰC NGHIỆM)

#### 4.1. Experimental Setup
Nêu rõ cấu hình môi trường để đảm bảo tính tái lập (Reproducibility):
*   **Phần cứng**: CPU (ví dụ: Intel Core i7-12700KF), RAM (ví dụ: 16GB), OS (ví dụ: Windows 11).
*   **Phần mềm**: Python 3.10+, thư viện `python-sat` (với SAT solver backend là `Glucose3`/`Glucose4`), Google OR-Tools (CP-SAT), CPLEX Optimizer (CPLEX CP và CPLEX MIP), Gurobi Optimizer (`gurobipy`).
*   **Tham số**: Time-out limit cho mỗi lượt chạy là **300 giây**.

#### 4.2. SAT Encodings Performance (So sánh các kỹ thuật mã hóa SAT)
*   **Bảng kết quả**: Lập bảng so sánh Số lượng biến (Variables), Số lượng mệnh đề (Clauses) và Thời gian giải (Solving Time) giữa các loại mã hóa: Pairwise, Binary, Sequential Counter khi tăng dần kích thước $N \in \{4, 8, 16, 20, 25, 30, 40, 50, 100\}$.
*   **Phân tích & Thảo luận**: 
    - Giải thích tại sao khi $N \ge 32$, mã hóa Pairwise bắt đầu gặp khó khăn về bộ nhớ hoặc thời gian sinh mệnh đề (do sự bùng nổ $O(N^3)$ tổng số clause cho tất cả các hướng).
    - Chỉ ra Sequential Counter là cứu cánh như thế nào khi giữ số lượng clause ở mức tuyến tính $O(N^2)$ đối với bàn cờ, giúp solver giải được các kích thước lớn hơn một cách dễ dàng.

#### 4.3. Cross-Paradigm Benchmark (So sánh liên phương pháp)
*   **Bảng kết quả tổng hợp**: Lập bảng so sánh thời gian chạy thực tế giữa:
    - SAT Solver (dùng `SeqCounter` + `Glucose3`)
    - CP-SAT (Google OR-Tools)
    - IBM CPLEX CP
    - Gurobi Optimizer (ILP)
    - IBM CPLEX MIP (ILP)
*   **Vẽ Biểu Đồ (Trực quan hóa)**: Đưa các biểu đồ đường (Line Chart) so sánh thời gian giải quyết theo kích thước $N$ (thang đo trục Y nên đặt ở dạng Logarithmic scale để thấy rõ sự khác biệt của các thuật toán tiệm cận).
*   **Thảo luận chuyên sâu (Trọng tâm đạt điểm A+)**:
    - *Tại sao CP-SAT giải nhanh nhất?*: Giải thích cơ chế lọc miền trị và lan truyền ràng buộc cực mạnh của thuật toán `AllDifferent` giúp loại bỏ toàn bộ các nhánh rẽ vô nghiệm ngay lập tức mà không phải mò mẫm thử sai.
    - *Hành vi của Gurobi / ILP*: Giải thích Gurobi giải quyết các bài toán tối ưu tuyến tính có hàm mục tiêu rất tốt, nhưng đối với bài toán tìm nghiệm khả thi thuần logic như N-Queens, cấu trúc ma trận số thực của ILP có phần nặng nề và kém linh hoạt hơn so với thuật toán lan truyền ràng buộc của CP.

---

### SECTION 5: CONCLUSION (KẾT LUẬN)
*   Khẳng định lại kết quả nghiên cứu. Nêu rõ rằng Lập trình ràng buộc (CP) là phương pháp tối ưu nhất cho bài toán N-Queens, trong khi SAT Solving với mã hóa Sequential Counter là giải pháp logic Boolean có khả năng mở rộng tốt nhất.

---

## 3. QUY CHUẨN THIẾT KẾ BIỂU BẢNG TRONG LATEX (ELSEVIER STYLE)

### Quy tắc vẽ bảng khoa học (Booktabs):
*   **Không** sử dụng các đường kẻ dọc (`|`).
*   Sử dụng nét kẻ ngang đậm ở đầu và cuối bảng (`\toprule`, `\bottomrule`).
*   Sử dụng nét kẻ ngang mảnh phân chia tiêu đề (`\midrule`).
*   Sử dụng nét kẻ ngang mảnh cho các nhóm cột (`\cmidrule`).

#### Code mẫu bảng so sánh các phương pháp (sẵn sàng chép vào LaTeX):
```latex
\begin{table}[width=1.0\linewidth,cols=6,pos=h]
\caption{Solving execution CPU time (seconds) and status comparison on N-Queens.}
\label{tbl:queens_cross_benchmark}
\begin{tabular*}{\tblwidth}{@{} LLLLLL @{}}
\toprule
$N$ & SAT (SeqCounter) & OR-Tools CP-SAT & CPLEX CP & Gurobi MIP & CPLEX MIP \\
\midrule
4   & 0.0003 (OPT) & 0.0012 (OPT) & 0.0021 (OPT) & 0.0011 (OPT) & 0.0020 (OPT) \\
8   & 0.0008 (OPT) & 0.0020 (OPT) & 0.0031 (OPT) & 0.0025 (OPT) & 0.0035 (OPT) \\
16  & 0.0051 (OPT) & 0.0055 (OPT) & 0.0080 (OPT) & 0.0120 (OPT) & 0.0152 (OPT) \\
50  & 0.4215 (OPT) & 0.0210 (OPT) & 0.0451 (OPT) & 2.1542 (OPT) & 5.6410 (OPT) \\
100 & 4.5120 (OPT) & 0.0841 (OPT) & 0.1205 (OPT) & 45.120 (OPT) & 120.42 (OPT) \\
200 & 84.152 (OPT) & 0.2514 (OPT) & 0.4502 (OPT) & -- (TO)      & -- (TO)      \\
500 & -- (TO)      & 1.4501 (OPT) & 2.8105 (OPT) & -- (TO)      & -- (TO)      \\
1000& -- (TO)      & 6.5412 (OPT) & 12.301 (OPT) & -- (TO)      & -- (TO)      \\
\bottomrule
\end{tabular*}
\end{table}
```

---

## 4. DANH MỤC TÀI LIỆU THAM KHẢO TIÊU BIỂU (BIBTEX)
Để phần References của bài báo chuẩn chỉ, hãy tạo một file `references.bib` và chèn các trích dẫn sau:

```bibtex
@article{ignatiev2018pysat,
  title={{PySAT}: A Python toolkit for prototyping with {SAT} oracles},
  author={Ignatiev, Alexey and Janota, Mikol{\'a}{\v{s}} and Marques-Silva, Joao},
  journal={SAT Association},
  year={2018}
}

@inproceedings{sinz2005towards,
  title={Towards an optimal {SAT} encoding of cardinality constraints},
  author={Sinz, Carsten},
  booktitle={Principles and Practice of Constraint Programming},
  pages={827--831},
  year={2005},
  organization={Springer}
}

@article{biere2021cadical,
  title={CaDiCaL, Kissat, Paracooba, Plingeling and Treengeling entering the SAT Competition 2020},
  author={Biere, Armin and Fazekas, Katalin and Fleury, Mathias and Heisinger, Maximillian},
  journal={Proceedings of SAT Competition},
  pages={51--53},
  year={2021}
}
```

Hãy tuân thủ nghiêm ngặt cẩm nang này để bài viết của bạn đạt phong cách học thuật chuẩn Elsevier và ghi điểm tuyệt đối trong môn học!
