import pygame
import sys
from shapes import Tetromino

pygame.init()


ROWS, COLS = 15, 20
BLOCK_SIZE = 30
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Plays Tetris")

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def valid_position(tetromino, board, cols, rows, dx=0, dy=0, rotation=None):
    rot = tetromino.rotation if rotation is None else rotation
    for (ox, oy) in tetromino.rotations[rot]:
        cx = tetromino.x + ox + dx
        cy = tetromino.y + oy + dy
        
        if cx < 0 or cx >= cols or cy < 0 or cy >= rows:
            return False

        if board[cy][cx] != 0:
            return False

    return True


def draw_board(screen, board, block_size):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell != 0:
                color = cell
                pygame.draw.rect(
                    screen,
                    color,
                    (x * block_size, y * block_size, block_size, block_size)
                )
            else:
                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    (x * block_size, y * block_size, block_size, block_size)
                )
                pygame.draw.rect(
                    screen,
                    (50, 50, 50),
                    (x * block_size, y * block_size, block_size, block_size),
                    1
                )

x,y = COLS // 2, 0

clock = pygame.time.Clock()
running = True

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000)

block = Tetromino('I', x, y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            if (valid_position(block, board, COLS, ROWS, 0, 1)):
                block.y += 1
            else:
                for (cx, cy) in block.cells:
                    board[cy][cx] = block.color
                block = Tetromino('T', 9, 0)

    keys = pygame.key.get_pressed()
    
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if (valid_position(block, board, COLS, ROWS, -1, 0)):
            block.x -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if (valid_position(block, board, COLS, ROWS, 1, 0)):
            block.x += 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if (valid_position(block, board, COLS, ROWS, 0, 1)):
            block.y += 1
    
    block.x = max(0, min(COLS - 3, block.x))
    block.y = max(0, min(ROWS - 2, block.y))

    draw_board(screen, board, BLOCK_SIZE)
    for (x, y) in block.cells:
        pygame.draw.rect(
            screen,
            block.color,
            (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        )

    pygame.display.flip()

    clock.tick(20)

pygame.quit()
sys.exit()

