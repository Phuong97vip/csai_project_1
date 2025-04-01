# Source\main.py
import sys
import argparse
from constants import *
from runtime import PygameRuntime

# Initialize pygame
# pygame.init()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Pac-Man Search Algorithms')
    parser.add_argument('--algorithm', type=str, nargs='+', choices=['BFS', 'DFS', 'UCS', 'Astar'], 
                       default='Astar', help='Search algorithm to use (BFS, DFS, UCS , or Astar)')

    return parser.parse_args()

def main():
    game = PygameRuntime()
    game.run()
    # args = parse_arguments()
    # selected_algorithms = []
    
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption(f"Pac-Man Search Algorithms - {', '.join(selected_algorithms)}")
    # clock = pygame.time.Clock()
    # font = pygame.font.SysFont('Arial', 16)
    
    # maze = Maze(GRID_SIZE, GRID_SIZE)
    # pacman_pos = None
    # ghosts = []

    # game_started = False
    # running = True
    # while running:
    #     draw_maze(screen, GRID_SIZE, CELL_SIZE, maze, BLACK, GRAY, BLACK)

    #     if game_started:
    #         runtime(screen, clock, ghosts, pacman_pos, maze, BLACK, GRAY, BLACK, font)
    #     else:
    #         game_started = draw_ui(screen, font, selected_algorithms, pacman_pos, maze, ghosts)

    #     pygame.display.flip()
    #     clock.tick(10)
    
    # pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()