# Source\maze.py
import numpy as np
import random

class Maze:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.tagged = np.zeros((height, width), dtype=int)
        
        # Tạo các bức tường cố định
        self.border()
        self.generate()

        # # Tường ngang
        # for x in range(5, 15):
        #     self.grid[5][x] = 1
        #     self.grid[15][x] = 1
        
        # # Tường dọc
        # for y in range(5, 16):
        #     self.grid[y][5] = 1
        #     self.grid[y][15] = 1
        
        # Mở lỗ đi
        # self.grid[10][5] = 0
        # self.grid[10][15] = 0
        
        # Thêm các chướng ngại vật phức tạp
        # for x in range(4, 16):
        #     if x != 8:
        #         self.grid[4][x] = 1

        # for y in range(4, 17):
        #     if y != 10:
        #         self.grid[y][12] = 1

        # for x in range(2, 19):
        #     if x != 10:
        #         self.grid[8][x] = 1

        # for y in range(8, 18):
        #     if y != 12:
        #         self.grid[y][7] = 1

    def border(self):
        """Tạo các tường bao quanh"""
        for x in range(self.width):
            self.tag((x, 0), outer=True)
            self.tag((x, self.height - 1), outer=True)
        for y in range(self.height):
            self.tag((0, y), outer=True)
            self.tag((self.width - 1, y), outer=True)

        # "Mở lỗ đi"
        # mid = self.height // 2
        # self.grid[mid][0] = 0
        # self.grid[mid][self.width - 1] = 0



    def generate(self):
        """Tạo một mê cung ngẫu nhiên"""
 
        sizes = [(5,3), (3,5), (2,2), (3,4), (4,3), (1,3), (3,1), (1,4), (4,1), (1,5), (5,1), (1,2), (2,1), (2,3), (3,2)] 
        for i in range( 2, self.width - 2):
            for j in range(2, self.height - 2):
                if self.tagged[j][i] == 0:
                    size = random.choice(sizes)
                    if (size[0] >= 3 and size[1] >= 3):
                        self.generate_cage_cluster(i, j, size)
                    else:
                        self.generate_loop_cluster(i, j, size)
                    # self.generate_loop_cluster(i, j, size)


    def generate_loop_cluster(self, x, y, size):
        """Tạo một cụm ngẫu nhiên"""
        width, height = size

        print(f"Generating cluster at ({x}, {y}) with size {size}")
        # print(self.grid)
        # print(self.tagged)

        # Tạo tường ở giữa
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.tag((i, j))

        # Đánh dấu xung quanh
        self.tag_outer_walls((x, y), size)

    def generate_cage_cluster(self, x, y, size):
        """Tạo một chuồng ngẫu nhiên"""
        width, height = size

        print(f"Generating cage at ({x}, {y}) with size {size}")
        # Tạo tường ở biên
        for i in range(x, x + width):
            self.tag((i, y), outer=True)
            self.tag((i, y + height - 1), outer=True)

        for j in range(y, y + height):
            self.tag((x, j), outer=True)
            self.tag((x + width - 1, j), outer=True)

        holes_count = random.randint(1, 4)
        for _ in range(holes_count):
            hole_x = random.randint(x, x + width - 1)
            if (hole_x == x or hole_x == x + width - 1):
                hole_y = random.randint(y + 1, y + height - 2)
                self.tag((hole_x, hole_y), value=0)    
            else:
                hole_y = random.choice([y, y + height - 1])
                self.tag((hole_x, hole_y), value=0)    

        for i in range(x + 1, x + width - 1):
            for j in range(y + 1, y + height - 1):
                self.tag_no_change((i, j))

        # Đánh dấu xung quanh
        self.tag_outer_walls((x, y), size)

    def tag_outer_walls(self, position, size):
        width, height = size
        x, y = position
        for i in range(x - 1, x + width + 1):
            self.tag_no_change((i, y - 1), outer=True)
            self.tag_no_change((i, y + height), outer=True)

        for j in range(y - 1, y + height + 1):
            self.tag_no_change((x - 1, j), outer=True)
            self.tag_no_change((x + width, j), outer=True)

    def tag_no_change(self, position, outer=False):
        x, y = position
        offset = outer*2
        if (1 - offset < x < self.width - 2 + offset) and (1 - offset < y < self.height - 2 + offset):
            self.tagged[y][x] = 1

    def tag(self, position, value=1, outer=False):
        x, y = position
        offset = outer*2
        if (1 - offset < x < self.width - 2 + offset) and (1 - offset < y < self.height - 2 + offset):
            self.grid[y][x] = value
            self.tagged[y][x] = 1

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