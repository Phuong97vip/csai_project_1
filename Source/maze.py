# Source\maze.py
import numpy as np

class Maze:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        
        # Tạo các bức tường cố định
        # Tường ngang
        for x in range(5, 15):
            self.grid[5][x] = 1
            self.grid[15][x] = 1
        
        # Tường dọc
        for y in range(5, 16):
            self.grid[y][5] = 1
            self.grid[y][15] = 1
        
        # Mở lỗ đi
        self.grid[10][5] = 0
        self.grid[10][15] = 0
        
        # Thêm các chướng ngại vật phức tạp
        for x in range(4, 16):
            if x != 8:
                self.grid[4][x] = 1

        for y in range(4, 17):
            if y != 10:
                self.grid[y][12] = 1

        for x in range(2, 19):
            if x != 10:
                self.grid[8][x] = 1

        for y in range(8, 18):
            if y != 12:
                self.grid[y][7] = 1

    def is_wall(self, position):
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == 1
        return True  # Xem các ô ngoài biên là tường
        
    def get_neighbors(self, position):
        """Trả về các ô lân cận có thể di chuyển đến (lên, xuống, trái, phải)"""
        x, y = position
        neighbors = []
        # Thứ tự: phải, xuống, trái, lên (để DFS ưu tiên hướng ngược lại)
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.is_wall((nx, ny)):
                    neighbors.append((nx, ny))
        return neighbors