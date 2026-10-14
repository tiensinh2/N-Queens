import tracemalloc

class PerformanceTracker:
    @staticmethod
    def start_memory_tracking():
        tracemalloc.start()

    @staticmethod
    def stop_memory_tracking():
        """
        Dừng đo bộ nhớ và trả về bộ nhớ tiêu thụ đỉnh thực tế (bytes).
        """
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak
