import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 500
TILE_SIZE = 100
GRID_SIZE = 4
FONT = pygame.font.SysFont('Arial', 30)
SCORE_FONT = pygame.font.SysFont('Arial', 40)
BACKGROUND_COLOR = (187, 173, 160)
GAME_OVER_COLOR = (255, 69, 0)


TILE_COLORS = [
    (204, 192, 179),
    (255, 255, 255),
    (255, 246, 229),
    (255, 223, 186),
    (255, 192, 103),
    (255, 159, 28),
    (255, 129, 0),
    (255, 108, 0),
    (255, 87, 34),
    (255, 71, 27),
    (255, 55, 0),
    (255, 35, 0),
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

def add_new_tile(grid):
    empty_tiles = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                empty_tiles.append((r, c))
    if empty_tiles:
        random_tile = random.choice(empty_tiles)  
        row, col = random_tile
        grid[row][col] = random.choices([2, 4], [0.9, 0.1])[0]

def compress(grid):
    new_grid = []
    for q in range(GRID_SIZE):
        row = [0] * GRID_SIZE
        new_grid.append(row)
    for r in range(GRID_SIZE):
        position = 0
        for c in range(GRID_SIZE):
            if grid[r][c] != 0:
                new_grid[r][position] = grid[r][c]
                position += 1
    return new_grid

def merge(grid, score):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c + 1] and grid[r][c] != 0:
                grid[r][c] *= 2
                grid[r][c + 1] = 0
                score += grid[r][c]
    return grid, score

def move_left(grid, score):
    new_grid = compress(grid)
    new_grid, score = merge(new_grid, score)
    new_grid = compress(new_grid)
    return new_grid, score

def rotate_90_clockwise(grid):
    return list(map(list, zip(*grid[::-1])))

def move_right(grid, score):
    new_grid = rotate_90_clockwise(rotate_90_clockwise(grid))
    new_grid, score = move_left(new_grid, score)
    return rotate_90_clockwise(rotate_90_clockwise(new_grid)), score

def move_up(grid, score):
    new_grid = rotate_90_clockwise(grid)
    new_grid, score = move_left(new_grid, score)
    return rotate_90_clockwise(rotate_90_clockwise(rotate_90_clockwise(new_grid))), score

def move_down(grid, score):
    new_grid = rotate_90_clockwise(rotate_90_clockwise(rotate_90_clockwise(grid)))
    new_grid, score = move_left(new_grid, score)
    return rotate_90_clockwise(new_grid), score

def is_game_over(grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                return False
            if r < GRID_SIZE - 1 and grid[r][c] == grid[r + 1][c]:
                return False
            if c < GRID_SIZE - 1 and grid[r][c] == grid[r][c + 1]:
                return False
    return True

def restart_game():
    grid = []
    for n in range(GRID_SIZE):
        row = [0] * GRID_SIZE
        grid.append(row)
    add_new_tile(grid)
    add_new_tile(grid)
    return grid, 0

grid, score = restart_game()

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    grid, score = restart_game()
                    game_over = False
            else:
                if event.key == pygame.K_LEFT:
                    new_grid, new_score = move_left(grid, score)
                    if new_grid != grid:
                        grid, score = new_grid, new_score
                        add_new_tile(grid)
                elif event.key == pygame.K_RIGHT:
                    new_grid, new_score = move_right(grid, score)
                    if new_grid != grid:
                        grid, score = new_grid, new_score
                        add_new_tile(grid)
                elif event.key == pygame.K_DOWN:
                    new_grid, new_score = move_up(grid, score)
                    if new_grid != grid:
                        grid, score = new_grid, new_score
                        add_new_tile(grid)
                elif event.key == pygame.K_UP:
                    new_grid, new_score = move_down(grid, score)
                    if new_grid != grid:
                        grid, score = new_grid, new_score
                        add_new_tile(grid)

    if is_game_over(grid):
        game_over = True
        screen.fill(GAME_OVER_COLOR)
        game_over_surface = SCORE_FONT.render("Konec hry !", True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        screen.blit(game_over_surface, game_over_rect)

        score_surface = SCORE_FONT.render(f" Tvoje Skóre: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(score_surface, score_rect)

        restart_surface = FONT.render("Zmáčkni R pro restart", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        screen.blit(restart_surface, restart_rect)
    else:
        screen.fill(BACKGROUND_COLOR)
        
        score_surface = SCORE_FONT.render(f"Skóre: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH / 2, 50))
        screen.blit(score_surface, score_rect)
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = grid[row][col]
                
                if value == 0:
                    color = TILE_COLORS[0]
                elif value == 2:
                    color = TILE_COLORS[1]
                elif value == 4:
                    color = TILE_COLORS[2]
                elif value == 8:
                    color = TILE_COLORS[3]
                elif value == 16:
                    color = TILE_COLORS[4]
                elif value == 32:
                    color = TILE_COLORS[5]
                elif value == 64:
                    color = TILE_COLORS[6]
                elif value == 128:
                    color = TILE_COLORS[7]
                elif value == 256:
                    color = TILE_COLORS[8]
                elif value == 512:
                    color = TILE_COLORS[9]
                elif value == 1024:
                    color = TILE_COLORS[10]
                elif value == 2048:
                    color = TILE_COLORS[11]
                else:
                    color = (255, 255, 255)
                    
                pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (col * TILE_SIZE, row * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE), 2)
                if value != 0:
                    text_surface = FONT.render(str(value), True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(col * TILE_SIZE + TILE_SIZE / 2, row * TILE_SIZE + TILE_SIZE / 2 + 100))
                    screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()








