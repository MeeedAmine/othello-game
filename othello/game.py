import pygame
from othello.board import Board
from .constants import BLUE, DIRECTIONS, WHITE, BLACK, BLUE, HINT_COLOR, SQUARE_SIZE, RADIUS
from .board import Board
from .status import Status
def coordinate_on_board(x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7


class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.board.draw(window)
        self.end_game = False
        self.player = BLACK
        self.possible_moves = self.get_possible_moves()
        self.black_pieces, self.white_pieces = self.board.count_pieces()
        self.status = Status(window, self.black_pieces, self.white_pieces)
        self.update()
    
    def get_end_game(self):
        return self.end_game
    
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.possible_moves)
        self.status.update(self.window, self.black_pieces, self.white_pieces)
        pygame.display.update()
    
    def change_turn(self):
        self.black_pieces, self.white_pieces = self.board.count_pieces()
        self.player = BLACK if self.player == WHITE else WHITE
        self.possible_moves = self.get_possible_moves()

    def stone_to_flip(self, row, column):
        if self.board.game_field[row][column] == 0:
            self.board.add_piece(row, column, self.player)
            pieces_to_flip = []  # list of pieces cords that will be fliped
            if self.player is WHITE:
                opponent_player = BLACK
            else:
                opponent_player = WHITE
            for xdirection, ydirection in DIRECTIONS:
                x = row
                y = column
                x += xdirection
                y += ydirection
                # check if we still on board and if there's a stone of the opponent player
                if coordinate_on_board(x, y) and self.board.game_field[x][y] != 0 and self.board.game_field[x][y].color == opponent_player:
                    x += xdirection
                    y += ydirection
                    if not coordinate_on_board(x, y):
                        continue
                    while self.board.game_field[x][y] != 0 and self.board.game_field[x][y].color is opponent_player:
                        x += xdirection
                        y += ydirection
                        if not coordinate_on_board(x, y):
                            break
                    if not coordinate_on_board(x, y):
                        continue
                    if self.board.game_field[x][y] != 0 and self.board.game_field[x][y].color == self.player:
                        while True:
                            x -= xdirection
                            y -= ydirection
                            if x == row and y == column:
                                break
                            pieces_to_flip.append([x, y])
            # set the stone to 0
            self.board.add_piece(row, column, 0)
            # If the list is empty return false
            if len(pieces_to_flip) == 0:
                return False
            else:
                return pieces_to_flip
        else:
            return False
    

    def get_possible_moves(self):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                stones = self.stone_to_flip(x, y)
                if stones is not False:
                    if len(stones) is not 0:
                        valid_moves.append([x, y])
        return valid_moves
    
    def valid_move(self, row, col):
        move = [row, col]
        if move in self.possible_moves:
            return True
        else:
            return False
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pos = ((col * SQUARE_SIZE + SQUARE_SIZE//2), (row * SQUARE_SIZE + SQUARE_SIZE//2) + 75)
            pygame.draw.circle(self.window, HINT_COLOR, pos, RADIUS, 1)

    def make_move(self, row, col):
        if self.valid_move(row, col) == True:
            stones = self.stone_to_flip(row, col)
            if stones != False:
                self.board.add_piece(row, col, self.player)
                for i in range(len(stones)):
                    coordinate = stones[i]
                    self.board.add_piece(coordinate[0], coordinate[1], self.player)
                self.change_turn()
                self.update()
    
    def skip(self):
        if not self.possible_moves:
            self.change_turn()
            self.update()
            if not self.possible_moves:
                self.end_game = True
                self.winner()
                return 0
            print(f'{self.player} plays again!')
    
    def play(self, row, col):
        if self.end_game == False:
            self.make_move(row, col)
            self.skip()
        else:
            self.winner()

    def winner(self):
        if self.black_pieces > self.white_pieces:
            print(f'Black wins and the result is: White: {self.white_pieces}, Black: {self.black_pieces}')
        elif self.black_pieces < self.white_pieces:
            print(f'White wins and the result is: White: {self.white_pieces}, Black: {self.black_pieces}')
        else:
            print(f'Draw! And the result is: White: {self.white_pieces}, Black: {self.black_pieces}')
