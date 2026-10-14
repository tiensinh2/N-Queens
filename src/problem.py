class NQueensProblem:
    def __init__(self, n):
        """
        Khởi tạo thực thể bài toán N-Queens kích thước N x N.
        """
        self.n = n

    def get_var_id(self, r, c):
        """
        Ánh xạ tọa độ 2D (hàng r, cột c) sang chỉ số biến Boolean 1D (1-based index).
        Hàng r: 0 -> N-1
        Cột c: 0 -> N-1
        Kết quả: 1 -> N^2
        """
        return r * self.n + c + 1

    def verify_solution(self, board):
        """
        Kiểm tra độc lập một lời giải nhị phân 2D bàn cờ N x N.
        
        Parameters:
        - board (list 2D): Ma trận nhị phân N x N (1: quân hậu, 0: trống)
        
        Returns:
        - valid (bool): True nếu lời giải đúng quy tắc đặt hậu, False nếu vi phạm.
        - reason (str): Lý do vi phạm, hoặc 'OK' nếu hợp lệ.
        """
        if board is None:
            return False, "Board is None"
            
        n = len(board)
        if n != self.n:
            return False, f"Invalid board size: found {n}x{n}, expected {self.n}x{self.n}"
            
        # 1. Đếm số quân hậu trên bàn cờ
        total_queens = sum(sum(row) for row in board)
        if total_queens != self.n:
            return False, f"Incorrect number of queens: found {total_queens}, expected {self.n}"
            
        queens = []
        for r in range(self.n):
            for c in range(self.n):
                if board[r][c] == 1:
                    queens.append((r, c))
                    
        # 2. Kiểm tra xung đột cặp quân hậu
        for i in range(len(queens)):
            r1, c1 = queens[i]
            for j in range(i + 1, len(queens)):
                r2, c2 = queens[j]
                
                # Trùng hàng
                if r1 == r2:
                    return False, f"Row conflict: Queens at ({r1},{c1}) and ({r2},{c2})"
                # Trùng cột
                if c1 == c2:
                    return False, f"Column conflict: Queens at ({r1},{c1}) and ({r2},{c2})"
                # Trùng đường chéo xuôi hoặc ngược
                if abs(r1 - r2) == abs(c1 - c2):
                    return False, f"Diagonal conflict: Queens at ({r1},{c1}) and ({r2},{c2})"
                    
        return True, "OK"
