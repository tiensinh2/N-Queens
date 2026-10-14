from pysat.solvers import Solver

class SAT_SolverRegistry:
    @staticmethod
    def get_available_solvers():
        """
        Kiểm tra động và trả về danh sách các SAT solver thực sự khả dụng trên máy hiện tại.
        """
        all_solvers = [
            "glucose3", 
            "glucose4", 
            "cadical", 
            "minisat", 
            "lingeling", 
            "maplesat"
        ]
        
        available = []
        for name in all_solvers:
            try:
                # Thử khởi tạo solver trong 1 giây để kiểm tra tính khả dụng
                with Solver(name=name) as s:
                    available.append(name)
            except Exception:
                pass
        return available
