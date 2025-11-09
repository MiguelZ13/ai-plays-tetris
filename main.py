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

# rotate_with_srs.py
def rotate(block, board, cols, rows, direction=1):
    """
    Rotate block using SRS wall-kicks.
    direction: +1 clockwise, -1 counterclockwise
    Returns True if rotation succeeded (possibly with a kick), False otherwise.
    Assumes block.rotation in [0..3], block.rotations exists, block.shape_name is 'I','O','T','S','Z','J','L'
    """
    from_rot = block.rotation
    to_rot = (block.rotation + direction) % len(block.rotations)

    JLTSZ_KICKS = {
        (0, 1): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
        (1, 0): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
        (1, 2): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
        (2, 1): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
        (2, 3): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
        (3, 2): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
        (3, 0): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
        (0, 3): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
    }

    I_KICKS = {
        (0, 1): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
        (1, 0): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
        (1, 2): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
        (2, 1): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
        (2, 3): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
        (3, 2): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
        (3, 0): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
        (0, 3): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
    }

    if block.name == 'O':
        block.rotation = to_rot
        return True

    if block.name == 'I':
        kicks = I_KICKS.get((from_rot, to_rot))
    else:
        kicks = JLTSZ_KICKS.get((from_rot, to_rot))

    if kicks is None:
        kicks = [(0,0), (-1,0), (1,0), (0,-1)]

    for dx, dy in kicks:
        if valid_position(block, board, cols, rows, dx=dx, dy=dy, rotation=to_rot):
            block.x += dx
            block.y += dy
            block.rotation = to_rot
            return True

    return False



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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                rotate(block, board, COLS, ROWS, -1)
            if event.key == pygame.K_d:
                rotate(block, board, COLS, ROWS, 1)
                

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

