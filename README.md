# Bài Tập Lớn 1: Giải Bài Toán N-Queens Bằng Các Phương Pháp Chính Xác (SAT, CP, ILP)
## Môn học: Các Vấn Đề Hiện Đại Khoa Học Máy Tính (HK I Năm học 2026 - 2027)

Dự án này triển khai và so sánh hiệu năng của ba hệ phương pháp luận giải quyết bài toán tối ưu tổ hợp kinh điển **N-Queens** trên quy mô lớn, sử dụng **100% các thư viện tự do, miễn phí và mã nguồn mở**.

---

## 1. Cấu Trúc Mã Nguồn Dự Án

Mã nguồn được thiết kế theo chuẩn hướng đối tượng khoa học và chuyên nghiệp:

```text
N-Queen-BTL1/
│
├── src/
│   ├── __init__.py
│   ├── benchmark.py       # Kịch bản chạy thực nghiệm đồng bộ
│   ├── plot_results.py    # Kịch bản vẽ biểu đồ trực quan hóa dữ liệu
│   │
│   └── solvers/           # Thư mục chứa các Solvers mô hình hóa N-Queens
│       ├── __init__.py
│       ├── sat_solver.py  # SAT Solver (Tự động chuyển đổi ALO & AMO sang CNF bằng PySAT)
│       ├── cp_solver.py   # Constraint Programming Solver (Dùng Google OR-Tools CP-SAT)
│       └── ilp_solver.py  # Integer Linear Programming Solver (Dùng OR-Tools CBC - 100% Free)
│
├── results/               # Folder lưu trữ dữ liệu CSV và biểu đồ kết quả
│   ├── benchmark_data.csv
│   ├── cross_solver_comparison.png
│   └── sat_clauses_comparison.png
│
├── requirements.txt       # Danh sách thư viện Python tự do cần cài đặt
├── Yeu_Cau_BTL1_NQueens.md # Bản mô tả yêu cầu thực hiện chi tiết đề tài
└── report_instruction.md   # Cẩm nang hướng dẫn viết báo cáo chuẩn Elsevier cas-sc
```

---

## 2. Các Công Cụ Giải (Solvers) Được Sử Dụng

Dự án này nói không với các phần mềm trả phí thương mại phức tạp (như Gurobi hay CPLEX thương mại), tập trung hoàn chỉnh vào giải pháp mã nguồn mở tự do:
1.  **SAT Solving**: Sử dụng thư viện `python-sat` (PySAT) với bộ giải hiệu năng cao `Glucose3` được tích hợp sẵn.
2.  **Constraint Programming (CP)**: Sử dụng **Google OR-Tools CP-SAT Solver** - một trong những bộ giải lập trình ràng buộc nhanh nhất thế giới hiện nay.
3.  **Integer Linear Programming (ILP)**: Sử dụng mô hình tuyến tính nguyên giải bởi động cơ **CBC** (Coin-or branch and cut) thông qua giao diện `pywraplp` của Google OR-Tools. 100% miễn phí, không yêu cầu license học thuật phức tạp.

---

## 3. Hướng Dẫn Cài Đặt Môi Trường

Mở terminal hoặc PowerShell tại thư mục dự án và chạy câu lệnh sau để tự động cài đặt tất cả các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

---

## 4. Hướng Dẫn Chạy Thực Nghiệm và Vẽ Biểu Đồ

Dự án đã được cấu hình sẵn các bước kiểm nghiệm tự động:

### Bước 1: Khởi chạy thực nghiệm tự động
Để chạy benchmark trên các kích thước bàn cờ, hãy truy cập vào thư mục `src` và chạy file `benchmark.py`:

```bash
cd src
python benchmark.py
```
*Lưu ý:*
- Mặc định, file đang để chế độ **Test nhanh** với các kích thước $N \in \{4, 8, 12, 16\}$ để xác nhận tính chính xác ngay lập tức.
- Khi muốn chạy thực nghiệm quy mô lớn để viết báo cáo khoa học, bạn hãy mở file [`src/benchmark.py`](src/benchmark.py) và khôi phục mảng `sizes` ở dòng 15 thành các giá trị lớn hơn:
  `sizes = [4, 8, 12, 16, 20, 24, 28, 32, 40, 50, 60, 80, 100]`

Kết quả đo lường thời gian chạy, số lượng biến và mệnh đề của từng phương pháp sẽ tự động được xuất ra tệp tin CSV tại [`src/results/benchmark_data.csv`](src/results/benchmark_data.csv).

### Bước 2: Vẽ biểu đồ trực quan hóa dữ liệu
Sau khi có tệp CSV kết quả thực nghiệm tại `results/benchmark_data.csv`, bạn có thể trực quan hóa dữ liệu bằng hai cách chuyên nghiệp sau:

#### Cách 1: Sử dụng công cụ trực quan hóa trực tuyến (Khuyến nghị)
Truy cập trực tiếp vào nền tảng vẽ biểu đồ tự động:
👉 **[CNS Plots Visualizer](https://cnsplots.farid.one/latest/)**

*Hướng dẫn*: Bạn chỉ cần kéo và thả (hoặc upload) tệp dữ liệu thực nghiệm **`results/benchmark_data.csv`** lên giao diện web. Hệ thống trực tuyến sẽ tự động phân tích cấu trúc cột, phân nhóm dữ liệu và tạo ra các đồ thị tương tác (ECharts/Matplotlib) sắc nét chuẩn khoa học cực kỳ nhanh chóng và chuyên nghiệp.

#### Cách 2: Sử dụng Script Python cục bộ (Offline)
Chạy script vẽ đồ thị trực tiếp từ thư mục `scripts` bằng môi trường ảo:
```bash
.venv\Scripts\python.exe scripts/plot_results.py
```
Hệ thống sẽ tự động phân tích tệp CSV cục bộ và xuất 4 tệp biểu đồ dạng ảnh chất lượng cao vào thư mục **`results/`**:
1.  **`results/cross_paradigm_time_comparison.png`**: So sánh thời gian giải quyết (Solving CPU Time) ở thang đo Logarithmic.
2.  **`results/peak_memory_comparison.png`**: So sánh lượng RAM tiêu thụ đỉnh điểm của các solver.
3.  **`results/sat_clauses_count_comparison.png`**: So sánh số lượng mệnh đề CNF của 6 SAT Encoders.
4.  **`results/sat_encodings_time_comparison.png`**: So sánh tốc độ thực tế của các SAT Encoders.

---

## 5. Hướng Dẫn Hoàn Thiện Báo Cáo Thuyết Minh
- Hãy đọc kỹ cẩm nang hướng dẫn đã được biên soạn riêng tại **[`report_instruction.md`](report_instruction.md)**.
- Tài liệu này hướng dẫn bạn cách viết báo cáo theo cấu trúc một bài báo khoa học chuẩn **Elsevier LaTeX (`cas-sc`)** dựa trên khung bài báo thực tế của Bộ môn, hướng dẫn viết công thức toán học và thiết kế các bảng biểu sạch sẽ đạt điểm số tối đa.

Chúc các bạn sinh viên thực hiện và bảo vệ bài tập lớn thành công rực rỡ!
