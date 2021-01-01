import pygame
import time
import copy
import random
from othello.board import Board
from .constants import DIRECTIONS, WHITE, BLACK, HINT_COLOR, SQUARE_SIZE, RADIUS, REWARD_SQUARES, RED
from .board import Board
from .status import Status
def coordinate_on_board(x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7


class Game:
    def __init__(self, window, difficulty_level, player_name, game_mode):
        self.window = window
        self.difficulty_level = difficulty_level
        self.game_mode = game_mode
        self.board = Board()
        self.board.draw(window)
        self.end_game = False
        self.player = BLACK
        self.possible_moves = self.get_possible_moves(self.board)
        self.black_pieces, self.white_pieces = self.board.count_pieces()
        self.status = Status(window, self.black_pieces, self.white_pieces, player_name)
        self.last_cord = [None, None]
        self.update()
    
    def get_end_game(self):
        return self.end_game
    
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.possible_moves)
        self.status.update(self.window, self.black_pieces, self.white_pieces)
        self.draw_click(self.last_cord)
        pygame.display.update()
    
    def change_turn(self):
        self.black_pieces, self.white_pieces = self.board.count_pieces()
        self.player = BLACK if self.player == WHITE else WHITE
        self.possible_moves = self.get_possible_moves(self.board)

    def stone_to_flip(self, board,  row, column):
        if board.game_field[row][column] == 0:
            board.add_piece(row, column, self.player)
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
                if coordinate_on_board(x, y) and board.game_field[x][y] != 0 and board.game_field[x][y].color == opponent_player:
                    x += xdirection
                    y += ydirection
                    if not coordinate_on_board(x, y):
                        continue
                    while board.game_field[x][y] != 0 and board.game_field[x][y].color is opponent_player:
                        x += xdirection
                        y += ydirection
                        if not coordinate_on_board(x, y):
                            break
                    if not coordinate_on_board(x, y):
                        continue
                    if board.game_field[x][y] != 0 and board.game_field[x][y].color == self.player:
                        while True:
                            x -= xdirection
                            y -= ydirection
                            if x == row and y == column:
                                break
                            pieces_to_flip.append([x, y])
            # set the stone to 0
            board.add_piece(row, column, 0)
            # If the list is empty return false
            if len(pieces_to_flip) == 0:
                return False
            else:
                return pieces_to_flip
        else:
            return False
    

    def get_possible_moves(self, board):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                stones = self.stone_to_flip(board, x, y)
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

    def draw_click(self, last_cord):
        x, y = last_cord
        if x is not None and y is not None:
            pos = ((y * SQUARE_SIZE + SQUARE_SIZE//2), (x * SQUARE_SIZE + SQUARE_SIZE//2) + 75)
            pygame.draw.circle(self.window, RED, pos, 5)
    
    def make_move(self, board, row, col):
        self.last_cord = [row, col]
        if self.valid_move(row, col) == True:
            stones = self.stone_to_flip(board, row, col)
            if stones != False:
                board.add_piece(row, col, self.player)
                for i in range(len(stones)):
                    coordinate = stones[i]
                    board.add_piece(coordinate[0], coordinate[1], self.player)
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
            #should be changed
            if self.game_mode == 1:
                if self.player == BLACK:
                    self.make_move(self.board, row, col)
                    self.skip()
                    time.sleep(1)
                if self.player == WHITE:
                    x, y = self.strategie(self.player, self.board)
                    self.make_move(self.board, x, y)
                    self.skip()
            else:
                self.make_move(self.board, row, col)
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

    """This section is for ai strategies"""
    
    def strategie(self, player, board):
        if self.difficulty_level == 1:
            return self.random_move()
        elif self.difficulty_level == 2:
            return self.best_weighted_move()
        elif self.difficulty_level == 3:
            score, move = self.minimax_alpha_beta(player, board, 4, -100000, 100000)
            return move
    #strategie 0
    def random_move(self):
        return random.choice(self.possible_moves)
    def best_weighted_move(self):
        coord_best_move = []
        best_move = -40
        for x, y in self.possible_moves:
            if REWARD_SQUARES[x][y] >= best_move:
                best_move = REWARD_SQUARES[x][y]
                coord_best_move = [x, y]
        return coord_best_move
    #strategie 1
    def simulate_move(self, board, player, row, col):
        if self.valid_move(row, col) == True:
            stones = self.stone_to_flip(board, row, col)
            if stones != False:
                board.add_piece(row, col, player)
                for i in range(len(stones)):
                    coordinate = stones[i]
                    board.add_piece(coordinate[0], coordinate[1], player)
    
    def evaluate(self, board, player):
        opponent = BLACK if player == WHITE else WHITE
        total  = 0
        #getting the cordinates of all pieces of a player on the board 
        players_pieces = board.get_pieces(player)
        opponents_pieces = board.get_pieces(opponent)

        for piece_cord in players_pieces:
            total += REWARD_SQUARES[piece_cord[0]][piece_cord[1]]
        
        for piece_cord in opponents_pieces:
            total -= REWARD_SQUARES[piece_cord[0]][piece_cord[1]]
        return total

    def minimax_search(self, player, board, depth):
        opponent = BLACK if player == WHITE else WHITE
        legal_moves = self.get_possible_moves(board)
        if not legal_moves:
            return (self.evaluate(board, player), None)
        if depth == 0:
            return (self.evaluate(board, player), None)
        best_score = -100000
        best_move = None
        for move in legal_moves:
            x, y = move
            new_board = copy.deepcopy(board)
            self.simulate_move(new_board, player, x, y)

            temp_eval = self.minimax_search(opponent, new_board, depth-1)
            temp_score = -temp_eval[0]
            if temp_score> best_score:
                best_score = temp_score
                best_move = move
        return best_score, best_move
    
    def minimax_alpha_beta(self, player, board, depth, alpha, beta):
        opponent = BLACK if player == WHITE else WHITE
        legal_moves = self.get_possible_moves(board)
        if not legal_moves:
            return (self.evaluate(board, player), None)
        if depth == 0:
            return (self.evaluate(board, player), None)
        best_score = alpha
        best_move = None
        for move in legal_moves:
            x, y = move
            new_board = copy.deepcopy(board)
            self.simulate_move(new_board, player, x, y)
            temp_eval = self.minimax_alpha_beta(opponent, new_board, depth-1, -beta, -best_score)
            temp_score = -temp_eval[0]
            if temp_score> best_score:
                best_score = temp_score
                best_move = move
            if best_score > beta:
                return best_score, best_move
        return best_score, best_move