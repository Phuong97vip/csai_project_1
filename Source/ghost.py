from constants import *
from search_algorithms import bfs, dfs, ucs, a_star
import pygame

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
        self.stored_pacman_pos = None
        
    def find_path(self, maze, pacman_pos, screen=None, font=None):
        # update pacman position
        if pacman_pos != self.stored_pacman_pos:
            self.stored_pacman_pos = pacman_pos

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
        
    def move(self, maze, pacman_pos, screen=None, font=None, other_ghost_positions=[]):
        if not self.started:
            return
            
        self.move_delay += 1
        if self.move_delay < 3:  # Slow down movement
            return
        self.move_delay = 0
        
        # Recalculate path if needed
        # if not self.path or self.move_counter >= self.search_interval:
        if not self.path or self.stored_pacman_pos != pacman_pos:
            self.find_path(maze, pacman_pos, screen, font)
        
        if self.path:
            next_pos = self.path[0]
            if next_pos in other_ghost_positions:
                modded_maze = maze.copy()
                for ghost_pos in other_ghost_positions:
                    modded_maze.tag(ghost_pos)
                self.find_path(modded_maze, pacman_pos, screen, font)
                return
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
    
    def stop(self):
        self.started = False
        

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
