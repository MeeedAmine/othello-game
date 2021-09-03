import pygame, pygame_menu
from othello.constants import WIDTH, HEIGHT, SQUARE_SIZE
from othello.game import Game
FPS = 60

#Menu of the game
pygame.init()
surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu('Welcome to Othello', 600, 400, 
                       theme=pygame_menu.themes.THEME_DARK )

name = 'Meed Amine' 
difficulty_level = 1
player_mode = 1
def get_name(value):
    global name
    name = value
def set_player(player, value):
    global player_mode
    player_mode = value

def set_difficulty(value, difficulty):
    global difficulty_level
    difficulty_level = difficulty

def play():
    print(name, player_mode, difficulty_level)

menu.add.text_input('First Player :', default='Meed Amine', onchange=get_name)

menu.add.selector('Playing against :', [('Computer', 1), ('Another Player', 2)], 
                    onchange=set_player)
                   
menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], 
                            onchange=set_difficulty)

"""Here starts the code of the game"""
def get_row_col_mouse(pos):
        x, y = pos
        row = (y // SQUARE_SIZE) -1 
        col = (x // SQUARE_SIZE)
        return row, col


def main():
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Othello Game')

    
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW, difficulty_level, name, player_mode)

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


menu.add.button('Play', main)
menu.add.button('Quit', pygame_menu.events.EXIT)



menu.mainloop(surface)
#main()