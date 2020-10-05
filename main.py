from othello.piece import Piece
import pygame
from othello.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from othello.game import Game
FPS = 60


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Othello Game')

def get_row_col_mouse(pos):
    x, y = pos
    row = (y // SQUARE_SIZE) -1 
    col = (x // SQUARE_SIZE)
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_mouse(pos)
                game.play(row, col)
    game.update()
    pygame.quit()

main()