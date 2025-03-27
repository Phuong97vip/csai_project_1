import numpy as np

class Maze:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        # Create the maze grid
        self.grid = np.zeros((height, width), dtype=int)
        
        # Original fixed walls
        # Horizontal walls
        for x in range(5, 15):
            self.grid[5][x] = 1
            self.grid[15][x] = 1
        
        # Vertical walls
        for y in range(5, 16):
            self.grid[y][5] = 1
            self.grid[y][15] = 1
        
        # Openings in the original walls
        self.grid[10][5] = 0
        self.grid[10][15] = 0
        
        # Additional complexity:
        # Extra horizontal wall on row 4 from columns 4 to 15, with a gap at column 8.
        for x in range(4, 16):
            if x != 8:  # Leave gap for connectivity.
                self.grid[4][x] = 1

        # Extra vertical wall on column 12 from rows 4 to 16, with a gap at row 10.
        for y in range(4, 17):
            if y != 10:  # Leave gap at row 10.
                self.grid[y][12] = 1

        # New additional obstacles for further complexity:
        # Extra horizontal wall on row 8 from columns 2 to 18, with a gap at column 10.
        for x in range(2, 19):
            if x != 10:
                self.grid[8][x] = 1

        # Extra vertical wall on column 7 from rows 8 to 17, with a gap at row 12.
        for y in range(8, 18):
            if y != 12:
                self.grid[y][7] = 1

    def is_wall(self, position):
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == 1
        return True  # Treat out-of-bounds as walls
        
    def get_neighbors(self, position):
        """Get valid neighboring positions (up, down, left, right)."""
        x, y = position
        neighbors = []
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if not self.is_wall((nx, ny)):
                neighbors.append((nx, ny))
                
        return neighbors
        
    def clear_ghosts(self):
        """Remove ghost markers from the maze (2=blue, 3=pink, 4=orange)."""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] in [2, 3, 4]:
                    self.grid[y][x] = 0