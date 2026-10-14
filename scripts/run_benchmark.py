import sys
import os

# Cho phép import từ thư mục src (chèn vào đầu để tránh bị đè bởi package 'mip' ngoài)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from benchmark import run_synchronized_benchmark

if __name__ == "__main__":
    print("=========================================================")
    print(" EXECUTING SCIENTIFIC RUNNING CONTEXT VIA CLI            ")
    print("=========================================================")
    run_synchronized_benchmark()
