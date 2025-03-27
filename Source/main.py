import pygame
import sys
import time
import argparse
import numpy as np
from maze import Maze
from search_algorithms import bfs, dfs, ucs

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PINK = (255, 182, 193)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

class Ghost:
    def __init__(self, color, algorithm, start_pos=(0, 0)):
        self.color = color
        self.algorithm = algorithm
        self.position = start_pos
        self.path = []
        self.expanded_nodes = 0
        self.search_time = 0
        self.move_counter = 0
        self.search_interval = 2  # Recalculate path every 5 moves
        self.move_delay = 0  # Thêm biến delay để giảm tốc độ
        
    def find_path(self, maze, pacman_pos):
        start_time = time.time()
        
        if self.algorithm == "BFS":
            self.path, self.expanded_nodes = bfs(maze, self.position, pacman_pos)
        elif self.algorithm == "DFS":
            self.path, self.expanded_nodes = dfs(maze, self.position, pacman_pos)
        elif self.algorithm == "UCS":
            self.path, self.expanded_nodes = ucs(maze, self.position, pacman_pos)
            
        self.search_time = time.time() - start_time
        self.move_counter = 0  # Reset move counter after recalculating path
        
    def move(self, maze, pacman_pos):
        # Giảm tốc độ di chuyển bằng cách chỉ di chuyển sau 3 lần gọi hàm
        self.move_delay += 1
        if self.move_delay < 3:
            return
            
        self.move_delay = 0
        
        if not self.path or self.move_counter >= self.search_interval:
            self.find_path(maze, pacman_pos)
        
        if self.path:
            next_pos = self.path[0]
            if not maze.is_wall(next_pos):
                self.position = next_pos
                self.path.pop(0)
                self.move_counter += 1
            else:
                # If next position is a wall (shouldn't happen), recalculate path
                self.find_path(maze, pacman_pos)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Pac-Man Search Algorithms')
    parser.add_argument('--algorithm', type=str, choices=['BFS', 'DFS', 'UCS'], 
                       default='BFS', help='Search algorithm to use (BFS, DFS, or UCS)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    selected_algorithm = args.algorithm
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Pac-Man Search Algorithms - {selected_algorithm}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 16)
    
    maze = Maze(GRID_SIZE, GRID_SIZE)
    pacman_pos = (GRID_SIZE//2, GRID_SIZE//2)  # Pac-Man starts at center
    
    # Create ghost with selected algorithm
    ghost = Ghost(BLUE, selected_algorithm, (0, 0))
    
    # Calculate initial path
    ghost.find_path(maze, pacman_pos)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Reset game nhưng vẫn giữ map cố định
                    maze = Maze(GRID_SIZE, GRID_SIZE)
                    pacman_pos = (GRID_SIZE//2, GRID_SIZE//2)
                    ghost.position = (0, 0)
                    ghost.path = []
                    ghost.find_path(maze, pacman_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if not maze.is_wall((grid_x, grid_y)):
                    pacman_pos = (grid_x, grid_y)
                    ghost.find_path(maze, pacman_pos)
        
        # Move ghost
        ghost.move(maze, pacman_pos)
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw maze
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if maze.is_wall((x, y)):
                    pygame.draw.rect(screen, GRAY, rect)
                else:
                    pygame.draw.rect(screen, BLACK, rect)
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)
        
        # Draw Pac-Man
        if pacman_pos:
            px, py = pacman_pos
            pygame.draw.circle(screen, YELLOW, 
                            (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2),
                            CELL_SIZE // 2 - 2)
        
        # Draw ghost
        gx, gy = ghost.position
        pygame.draw.circle(screen, ghost.color, 
                        (gx * CELL_SIZE + CELL_SIZE // 2, gy * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 2 - 2)
        
        # Display info
        info_y = HEIGHT - 40
        text = f"{ghost.color} Ghost ({ghost.algorithm}): Time={ghost.search_time:.4f}s, Nodes={ghost.expanded_nodes}"
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, info_y))
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()