
WIDTH, HEIGHT = 600, 675
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# For checking in all direction around the stone
DIRECTIONS = ([-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1])
#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 144, 103) #background color
RED = (255, 0, 0)
HINT_COLOR = (136,124,230)
BLUE = (0, 0, 255)

PADDING = 6 #padding between the piece and the square
RADIUS = SQUARE_SIZE//2 - PADDING

REWARD_SQUARES = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120]
]