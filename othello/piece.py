import pygame
from .constants import SQUARE_SIZE, GREY, RADIUS


class Piece:
    OUTLINE = 1
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_position()
        self.last_played = False
        
    def calc_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2 + 75

    def draw_piece(self, window):
        pygame.draw.circle(window, GREY, (self.x, self.y), RADIUS + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), RADIUS)
    
    def __repr__(self):
        return str(self.color)