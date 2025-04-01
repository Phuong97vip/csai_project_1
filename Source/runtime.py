import pygame
from maze import Maze
from ghost import Ghost
from constants import *

class PygameRuntime:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 200, GRID_SIZE * CELL_SIZE))
        pygame.display.set_caption("Pacman Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 16)
        self.running = True
        self.game_started = False
        self.maze = Maze(GRID_SIZE, GRID_SIZE)
        self.pacman_pos = (1, 1)
        self.ghosts = []
        self.selected_algorithms = []
        self.screen_color = BLACK
        self.wall_color = GRAY
        self.path_color = BLACK
        self.pacman_color = YELLOW
        self.buttons = [
            {"label": "Add BFS Ghost (b)", "action": "BFS"},
            {"label": "Add DFS Ghost (d)", "action": "DFS"},
            {"label": "Add UCS Ghost (u)", "action": "UCS"},
            {"label": "Add A* Ghost (a)", "action": "Astar"},
            {"label": "Start Game (SPACE)", "action": "START"}
        ]

    def move_pacman(self, direction):
        x, y = self.pacman_pos
        new_pos = self.pacman_pos
        match direction:
            case "UP":
                new_pos = (x, y - 1)
            case "DOWN":
                new_pos = (x, y + 1)
            case "LEFT":
                new_pos = (x - 1, y)
            case "RIGHT":
                new_pos = (x + 1, y)
        
        if not (self.maze.is_wall(new_pos) or new_pos is None):
            self.pacman_pos = new_pos

    def start_game(self):
        for ghost in self.ghosts:
            ghost.start()
        self.game_started = True

    def pause_game(self):
        for ghost in self.ghosts:
            ghost.stop()
        self.game_started = False

    def handle_game_input(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.running = False
                        case pygame.K_SPACE:    
                            self.pause_game()
                        case pygame.K_UP:
                            self.move_pacman("UP")
                        case pygame.K_DOWN:
                            self.move_pacman("DOWN")
                        case pygame.K_LEFT:
                            self.move_pacman("LEFT")
                        case pygame.K_RIGHT:
                            self.move_pacman("RIGHT")

    def add_ghost(self, algorithm):
        if algorithm not in self.selected_algorithms:
            self.selected_algorithms.append(algorithm)
        generated_pos = self.maze.find_random_empty()
        while generated_pos in [ghost.position for ghost in self.ghosts]:
            generated_pos = self.maze.find_random_empty()
        new_ghost = Ghost(algorithm, generated_pos)
        self.ghosts.append(new_ghost)

    def handle_settings_input(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.running = False
                        case pygame.K_b:
                            self.add_ghost("BFS")
                        case pygame.K_d:
                            self.add_ghost("DFS")
                        case pygame.K_u:
                            self.add_ghost("UCS")
                        case pygame.K_a:
                            self.add_ghost("Astar")
                        case pygame.K_SPACE:
                            self.start_game()
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button in enumerate(self.buttons):
                        x = GRID_SIZE * CELL_SIZE + 20
                        y = 20 + i * (40 + 10)
                        rect = pygame.Rect(x, y, 150, 40)
                        if rect.collidepoint(mouse_pos):
                            if button["action"] == "START":
                                self.start_game()
                            else:
                                self.add_ghost(button["action"])
                    for j in range(self.maze.width):
                        x = j * CELL_SIZE
                        for k in range(self.maze.height):
                            y = k * CELL_SIZE
                            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                            if rect.collidepoint(mouse_pos):
                                if not (self.maze.is_wall((j, k)) or self.pacman_pos in [ghost.position for ghost in self.ghosts]):
                                    self.pacman_pos = (j, k)


    def draw_maze(self):
        # Draw background and maze
        self.screen.fill(self.screen_color)
        # Draw maze
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.maze.is_wall((x, y)):
                    pygame.draw.rect(self.screen, self.wall_color, rect)
                else:
                    pygame.draw.rect(self.screen, self.path_color, rect)
                    pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)

    def draw_pacman(self):
        if self.pacman_pos is None:
            return

        x, y = self.pacman_pos
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.circle(self.screen, self.pacman_color, rect.center, CELL_SIZE // 2 - 2)

    def draw_ghosts(self):
        for ghost in self.ghosts:
            x, y = ghost.position
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.circle(self.screen, ghost.color, rect.center, CELL_SIZE // 2 - 2)

            if ghost.path:
                path = [(x, y)] + ghost.path
                for i in range(len(path) - 1):
                    start_pos = (path[i][0] * CELL_SIZE + CELL_SIZE // 2, path[i][1] * CELL_SIZE + CELL_SIZE // 2)
                    end_pos = (path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2, path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.line(self.screen, ghost.color, start_pos, end_pos, 2)

    def game_runtime(self):
        if self.ghosts == []:
            self.game_started = False
            return

        for ghost in self.ghosts:
            if ghost.position == self.pacman_pos:
                self.ghosts.remove(ghost)
            ghost.move(self.maze, self.pacman_pos, self.screen, self.font, [g.position for g in self.ghosts if g != ghost])
            

        self.handle_game_input()


    def draw_ui(self):
        x = GRID_SIZE * CELL_SIZE + 20
        for i, button in enumerate(self.buttons):
            y = 20 + i * (40 + 10)
            rect = pygame.Rect(x, y, 150, 40)
            pygame.draw.rect(self.screen, GRAY, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)

            text_surface = self.font.render(button["label"], True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    
    def run(self):
        while self.running:
            self.draw_maze()

            if not self.game_started:
                self.handle_settings_input()
                self.draw_ui()
            else:
                self.game_runtime()

            self.draw_pacman()
            self.draw_ghosts()

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
                        

        


