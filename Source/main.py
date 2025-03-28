# Source\main.py
import pygame
import sys
import time
import argparse
import numpy as np
from maze import Maze
from search_algorithms import bfs, dfs, ucs,a_star

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
    def __init__(self, algorithm, start_pos=(0, 0)):
        # Set color based on algorithm
        if algorithm == "BFS":
            self.color = BLUE
        elif algorithm == "DFS":
            self.color = PINK
        elif algorithm == "UCS":
            self.color = ORANGE
        elif algorithm =="Astar":
            self.color = RED    
        self.algorithm = algorithm
        self.position = start_pos
        self.path = []
        self.total_expanded_nodes = 0
        self.total_search_time = 0
        self.total_memory_usage = 0  # KB
        self.search_count = 0
        self.move_counter = 0
        self.search_interval = 2
        self.move_delay = 0
        self.reached_target = False
        self.started = False
        
    def find_path(self, maze, pacman_pos, screen=None, font=None):
        if self.algorithm == "BFS":
            path, expanded_nodes, search_time, memory_usage = bfs(maze, self.position, pacman_pos)
        elif self.algorithm == "DFS":
            path, expanded_nodes, search_time, memory_usage = dfs(maze, self.position, pacman_pos)
        elif self.algorithm == "UCS":
            path, expanded_nodes, search_time, memory_usage = ucs(maze, self.position, pacman_pos)
        elif self.algorithm == "Astar":
            path, expanded_nodes, search_time, memory_usage = a_star(maze, self.position, pacman_pos)
        self.path = path
        self.total_expanded_nodes += expanded_nodes
        self.total_search_time += search_time
        self.total_memory_usage += memory_usage
        self.search_count += 1
        self.move_counter = 0
        
        # Check if reached target
        if self.position == pacman_pos and not self.reached_target:
            self.reached_target = True
            if screen and font:
                self.show_final_stats(screen, font)
        
    def move(self, maze, pacman_pos, screen=None, font=None):
        if not self.started:
            return
            
        self.move_delay += 1
        if self.move_delay < 3:  # Slow down movement
            return
        self.move_delay = 0
        
        # Recalculate path if needed
        # if not self.path or self.move_counter >= self.search_interval:
        if not self.path:
            self.find_path(maze, pacman_pos, screen, font)
        
        if self.path:
            next_pos = self.path[0]
            if not maze.is_wall(next_pos):
                self.position = next_pos
                self.path.pop(0)
                self.move_counter += 1
                
                # Check if reached target after move
                if self.position == pacman_pos and not self.reached_target:
                    self.reached_target = True
                    if screen and font:
                        self.show_final_stats(screen, font)
            else:
                # Recalculate path if wall encountered
                self.find_path(maze, pacman_pos, screen, font)
    
    def start(self):
        self.started = True
    
    def show_final_stats(self, screen, font):
        """Display final statistics when reaching target"""
        if self.search_count == 0:
            return
            
        avg_memory = self.total_memory_usage / self.search_count
        stats = [
            f"Algorithm: {self.algorithm}",
            f"Reached Target at: {self.position}",
            "",
            "=== Search Statistics ===",
            f"Total Search Time: {self.total_search_time:.4f} seconds",
            f"Total Expanded Nodes: {self.total_expanded_nodes}",
            f"Average Memory Usage: {avg_memory:.2f} KB",
            f"Number of Searches: {self.search_count}",
            "",
            "SPACE to reset"
        ]
        
        # Calculate popup size
        popup_width = 450
        line_height = 30
        popup_height = len(stats) * line_height + 20
        
        # Draw popup background
        popup_rect = pygame.Rect(
            (WIDTH - popup_width) // 2,
            (HEIGHT - popup_height) // 2,
            popup_width,
            popup_height
        )
        pygame.draw.rect(screen, (50, 50, 50), popup_rect)
        pygame.draw.rect(screen, WHITE, popup_rect, 2)
        
        # Draw text
        for i, stat in enumerate(stats):
            text_surface = font.render(stat, True, WHITE)
            screen.blit(text_surface, (
                popup_rect.x + 20,
                popup_rect.y + 10 + i * line_height
            ))
        
        pygame.display.flip()
        
        # Wait for space to reset
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Pac-Man Search Algorithms')
    parser.add_argument('--algorithm', type=str, nargs='+', choices=['BFS', 'DFS', 'UCS', 'Astar'], 
                       default='Astar', help='Search algorithm to use (BFS, DFS, UCS , or Astar)')

    return parser.parse_args()

def main():
    args = parse_arguments()
    selected_algorithms = args.algorithm
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Pac-Man Search Algorithms - {', '.join(selected_algorithms)}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 16)
    
    maze = Maze(GRID_SIZE, GRID_SIZE)
    pacman_pos = None
    ghosts = [None for _ in range(len(selected_algorithms))]
    ghost_positions = []
    for i, algorithm in enumerate(selected_algorithms):
        generated_pos = maze.find_random_empty()
        while generated_pos in ghost_positions:
            generated_pos = maze.find_random_empty()
        ghosts[i] = Ghost(algorithm, generated_pos)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if pacman_pos is not None:
                        for i, ghost in enumerate(ghosts):
                            ghost.find_path(maze, pacman_pos, screen, font)
                            ghost.start()
                        # if ghost is None:
                        #     ghost = Ghost(selected_algorithm, (1, 1))
                        #     ghost.find_path(maze, pacman_pos, screen, font)
                        # ghost.start()
                    else:
                        print("Please set Pac-Man position first by clicking on the maze")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if not maze.is_wall((grid_x, grid_y)):
                    pacman_pos = (grid_x, grid_y)
                    # if ghost is not None:
                    #     ghost = Ghost(selected_algorithm, (1, 1))
                    #     ghost.find_path(maze, pacman_pos, screen, font)
        
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
        
        # Draw Pac-Man if position is set
        if pacman_pos:
            px, py = pacman_pos
            pygame.draw.circle(screen, YELLOW, 
                            (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2),
                            CELL_SIZE // 2 - 2)
        
        # Draw ghost if it exists
        for ghost in ghosts:
            if ghost:
                ghost.move(maze, pacman_pos, screen, font)
                gx, gy = ghost.position
                pygame.draw.circle(screen, ghost.color, 
                                (gx * CELL_SIZE + CELL_SIZE // 2, gy * CELL_SIZE + CELL_SIZE // 2),
                                CELL_SIZE // 2 - 2)
                if ghost.path:
                    path = [(gx, gy)] + ghost.path
                    for i in range(len(path) - 1):
                        start_pos = (path[i][0] * CELL_SIZE + CELL_SIZE // 2, path[i][1] * CELL_SIZE + CELL_SIZE // 2)
                        end_pos = (path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2, path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2)
                        pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)
        # if ghost:
        #     ghost.move(maze, pacman_pos, screen, font)
        #     gx, gy = ghost.position
        #     pygame.draw.circle(screen, ghost.color, 
        #                     (gx * CELL_SIZE + CELL_SIZE // 2, gy * CELL_SIZE + CELL_SIZE // 2),
        #                     CELL_SIZE // 2 - 2)
        #     if ghost.path:
        #         path = [(gx, gy)] + ghost.path
        #         for i in range(len(path) - 1):
        #             start_pos = (path[i][0] * CELL_SIZE + CELL_SIZE // 2, path[i][1] * CELL_SIZE + CELL_SIZE // 2)
        #             end_pos = (path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2, path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2)
        #             pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)
        
        # Display information
        info_text = [
            f"Algorithm: {', '.join(selected_algorithms)}",
            f"Pac-Man Position: {pacman_pos if pacman_pos else 'Not set'}",
            "",
            "Instructions:",
            "1. Click to set Pac-Man position",
            "2. Press SPACE to start ghost",
            "3. Press SPACE to reset after ghost reaches target",
            "4. ESC to quit"
        ]

        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (10, 10 + i * 20))
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()