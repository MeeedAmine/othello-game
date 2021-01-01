import pygame
from .constants import GREY, BLACK, WIDTH

pygame.init()

class Status:
    def __init__(self, window, first_player_score, second_player_score, fisrt_player_name):
        self.window = window
        self.first_player_score = first_player_score
        self.second_player_score = second_player_score
        self.first_player_name = fisrt_player_name
        self.update(window, self.first_player_score, self.second_player_score)
    
    def set_score(self, first_player_score, second_player_score):
        self.first_player_score = first_player_score
        self.second_player_score = second_player_score
    
    def update(self, window, first_player_score, second_player_score):
        self.set_score(first_player_score, second_player_score)
        self.draw_background(window)
        self.display_result(window)

    def draw_background(self, window):
        surface = pygame.Surface((598,73))
        surface.fill(GREY)
        window.blit(surface,(1,1))
    #Player Name
    def display_result(self, window):
        message = f'{self.first_player_name}: {self.first_player_score}'    
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(message, 1, (BLACK))
        text_pos = text.get_rect(center = (WIDTH // 6, 75/2))
        window.blit(text, text_pos)
        message = f'White: {self.second_player_score}'
        text = font.render(message, 1, (BLACK))
        text_pos = text.get_rect(center = ((WIDTH // 4) * 3, 75/2))
        window.blit(text, text_pos)
