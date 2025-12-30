import pygame
import sys
from shapes import Tetromino
from random import randint

pygame.init()


ROWS, COLS = 15, 20
BLOCK_SIZE = 30
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
SIDE_PANEL_WIDTH = 5 * BLOCK_SIZE
PANEL_X = WIDTH + 10
screen = pygame.display.set_mode((WIDTH + SIDE_PANEL_WIDTH, HEIGHT))
pygame.display.set_caption("AI Plays Tetris")

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

score = 0
font = pygame.font.SysFont("arial", 24)

LINE_SCORES = {
    1: 100,
    2: 300,
    3: 500,
    4: 800
}

held_piece = None
can_hold = True

game_over = False

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


def rotate(block, board, cols, rows, direction=1):
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

def clear_lines(board):
    global score

    new_board = []
    cleared = 0

    for row in board:
        if all(cell != 0 for cell in row):
            cleared += 1
        else:
            new_board.append(row)

    for _ in range(cleared):
        new_board.insert(0, [0 for _ in range(COLS)])

    if cleared > 0:
        score += LINE_SCORES.get(cleared, 0)

    return new_board

def draw_mini_tetromino(screen, shape, x, y):
    temp = Tetromino(shape, x, y)
    for ox, oy in temp.rotations[0]:
        pygame.draw.rect(
            screen,
            temp.color,
            (
                x + ox * BLOCK_SIZE,
                y + oy * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE
            )
        )

def draw_side_panel(screen, shapeQueue, held_piece):
    next_text = font.render("NEXT", True, (255, 255, 255))
    held_text = font.render("HELD", True, (255, 255, 255))
    
    screen.blit(next_text, (PANEL_X, 20))
    screen.blit(held_text, (PANEL_X, 310))
    
    for i, shape in enumerate(shapeQueue):
        draw_mini_tetromino(
            screen, 
            shape, 
            PANEL_X, 
            60 + i * 90
        )
    
    if held_piece:
        draw_mini_tetromino(
            screen,
            held_piece,
            PANEL_X,
            350
        )
    

shapes = ('T', 'I', 'O', 'S', 'Z', 'L', 'J')
def generate_shape():
    return shapes[randint(0, len(shapes) - 1)]

x,y = COLS // 2, 0

clock = pygame.time.Clock()
running = True

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1000)

block = Tetromino(generate_shape(), x, y)

shapeQueue = [generate_shape() for _ in range(3)]

while running:
    if game_over:
        pygame.time.delay(2000)
        running = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            if (valid_position(block, board, COLS, ROWS, 0, 1)):
                block.y += 1
            else:
                for (cx, cy) in block.cells:
                    if cy < 0:
                        game_over = True
                    else:    
                        board[cy][cx] = block.color
                
                if game_over:
                    break

                board = clear_lines(board)

                block = Tetromino(shapeQueue[0], 9, 0)
                shapeQueue.pop(0)
                shapeQueue.append(generate_shape())
                
                can_hold = True

                if not valid_position(block, board, COLS, ROWS):
                    game_over = True
        
        if game_over:
            over_text = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(
                over_text,
                (
                    WIDTH // 2 - over_text.get_width() // 2,
                    HEIGHT // 2 - over_text.get_height() // 2
                )
            )

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                rotate(block, board, COLS, ROWS, -1)
            if event.key == pygame.K_d:
                rotate(block, board, COLS, ROWS, 1)
            if event.key == pygame.K_c and can_hold:
                if held_piece is None:
                    held_piece = block.name
                    block = Tetromino(shapeQueue[0], COLS // 2, 0)
                    shapeQueue.pop(0)
                    shapeQueue.append(generate_shape())
                else:
                    held_piece, block.name = block.name, held_piece
                    block = Tetromino(block.name, COLS // 2, 0)
                can_hold = False
                

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
    
    screen.fill((0, 0, 0))
    
    draw_board(screen, board, BLOCK_SIZE)
    for (x, y) in block.cells:
        pygame.draw.rect(
            screen,
            block.color,
            (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        )

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    draw_side_panel(screen, shapeQueue, held_piece)

    pygame.display.flip()

    clock.tick(20)

pygame.quit()
sys.exit()

