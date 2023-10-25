import pygame
import random

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

MOVEMENT_SPEED = 200

class Dungeon:
    def __init__(self):
        self.level = 1
        self.generate_maze()
        self.player_x, self.player_y = 1, 1
        self.regenerate_maze = False

        self.last_move_time = 0
        self.move_delay = MOVEMENT_SPEED

    def generate_maze(self):
        self.map = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        stack = [(1, 1)]

        while stack:
            x, y = stack[-1]
            self.map[y][x] = True

            unvisited_neighbors = []

            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < GRID_WIDTH - 1 and 0 < ny < GRID_HEIGHT - 1 and not self.map[ny][nx]:
                    unvisited_neighbors.append((nx, ny))

            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)
                wall_x, wall_y = (next_x + x) // 2, (next_y + y) // 2
                self.map[wall_y][wall_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

        self.player_x, self.player_y = 1, 1

        self.goal_x, self.goal_y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)

    def draw(self, screen):
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                color = WHITE if cell else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (self.goal_x * CELL_SIZE, self.goal_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (0, 0, 255), (self.player_x * CELL_SIZE, self.player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(text, (WIDTH - 150, 20))

    def move(self, dx, dy):
        if self.regenerate_maze:
            self.level += 1
            self.generate_maze()
            self.regenerate_maze = False

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_delay:
            new_x, new_y = self.player_x + dx, self.player_y + dy
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if new_x == self.goal_x and new_y == self.goal_y:
                    self.regenerate_maze = True
                elif self.map[new_y][new_x]:
                    self.player_x, self.player_y = new_x, new_y
                self.last_move_time = current_time

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Maze Game")

dungeon = Dungeon()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get player input
    keys = pygame.key.get_pressed()
    move = (keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])

    # Process player input
    dungeon.move(*move)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the dungeon and player
    dungeon.draw(screen)

    pygame.display.flip()

pygame.quit()