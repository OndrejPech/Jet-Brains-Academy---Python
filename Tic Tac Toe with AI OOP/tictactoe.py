# Program created due to objectives from Jet Brains Academy. It passed all the
# test, but they have been created only for 3x3 grid. This program can be easily
# modify to bigger grid, change symbols or even change number of points needed
# to win. But for higher grids the "smarter" difficulties are not working so
# smart. Minimax algorithm with alpha-beta cost to much execution time for
# bigger grids. I keep this file in case I want to improve it in the future.



import random
from typing import Tuple


class Board:
    height = 3
    width = 3
    symbol1 = 'X'
    symbol2 = 'O'
    empty_cell_sign = ' '

    def __init__(self):
        self.grid = [[self.empty_cell_sign for _ in range(self.width)]
                     for _ in range(self.height)]
        self.empty_cells = set((x, y) for x in range(1, self.width + 1)
                               for y in range(1, self.height + 1))

    def print_board(self):
        print('-' * 3 * self.width)
        for row in self.grid:
            print('| ', end='')
            print(*row, end='')
            print(' |')
        print('-' * 3 * self.width)

    def user_layout(self):
        """fill up grid with symbols and change empty_cells attribute"""
        self.grid = []
        empty_cells = []
        while True:
            symbols = input('Enter the cells:')
            if not self.input_layout_ok(symbols):
                continue
            all_symbols = list(symbols)
            for row_num in range(self.height):
                row = []
                for col_num in range(self.width):
                    symbol = all_symbols.pop(0)
                    if symbol == '_':
                        symbol = self.empty_cell_sign
                        empty_cells.append((to_human(row_num), to_human(col_num)))

                    row.append(symbol)
                self.grid.append(row)
            self.empty_cells = set(empty_cells)
            break

    def input_layout_ok(self, user_input):
        """
        check if user entered only valid symbols and correct amount of symbols
        """
        allowed_symbols = {self.symbol1, self.symbol2,
                           '_'}  # CAPITAL letters only
        if len(user_input) != self.height * self.width:
            print('Wrong number of symbols')
            return False

        if not set(user_input).issubset(allowed_symbols):
            print('Wrong symbols in input')
            return False

        return True

    @property
    def is_full(self):
        if sum(cell.count(self.empty_cell_sign) for cell in self.grid) == 0:
            return True
        return False


def to_human(num):
    """add 1 to num,so counting starts at 1"""
    return num + 1


def to_it(num):
    """decrease num by 1,so counting starts at 0"""
    return num - 1


def user_command():
    options = {'user': User, 'easy': Easy, 'medium': Medium, 'hard': Hard}
    while True:
        user_input = input('Input command:')
        if user_input == 'exit':
            quit()
        elif user_input.startswith('start'):
            try:
                words = user_input.split()
                if words[1] in options and words[2] in options:
                    return options[words[1]], options[words[2]]
            except IndexError:
                print('Bad parameters!')
                continue
            else:
                print('Bad parameters!')
                continue
        else:
            print('Bad parameters!')


class Game:
    needed_points = 3
    player1_turn = True

    def __init__(self, board):

        # choose which symbols is turn, useful when we dont start with empty board
        symbol1_count = sum(
            symbol.count(board.symbol1) for symbol in board.grid)
        symbol2_count = sum(
            symbol.count(board.symbol2) for symbol in board.grid)
        if symbol1_count > symbol2_count:
            self.symbol_turn = board.symbol2
            self.symbol_not_turn = board.symbol1
        else:
            self.symbol_turn = board.symbol1
            self.symbol_not_turn = board.symbol2

        # create both players based on input
        option1, option2 = user_command()
        self.player1 = option1(self.symbol_turn, self.symbol_not_turn, self)
        self.player2 = option2(self.symbol_not_turn, self.symbol_turn, self)

    def change_player(self):
        self.player1_turn = not self.player1_turn
        self.symbol_turn, self.symbol_not_turn = self.symbol_not_turn, self.symbol_turn

    def move(self, board):
        """update board with new move"""
        if self.player1_turn is True:
            coordinates = self.player1.player_choice(board)
        else:
            coordinates = self.player2.player_choice(board)

        board.empty_cells.remove(coordinates)
        row, col = coordinates
        board.grid[to_it(row)][to_it(col)] = self.symbol_turn

    def check_winner(self, board, symbol):
        """check all possibilities and return True if winner is made"""
        if self.check_horizontal(board.grid, symbol):
            return True
        if self.check_vertical(board.grid, symbol):
            return True
        if self.check_diagonal(board, symbol):
            return True
        if self.check_diagonal(board, symbol, reverse=True):
            return True
        return False

    def check_horizontal(self, grid, symbol):
        for row in grid:
            max_in_row = 0
            for cell in row:
                if cell == symbol:
                    max_in_row += 1
                    if max_in_row == self.needed_points:
                        return True
                else:
                    max_in_row = 0
        else:
            return False

    def check_vertical(self, grid, symbol):
        grid = [[grid[i][j] for i in range(len(grid))] for j in
                range(len(grid[0]))]
        return self.check_horizontal(grid, symbol)

    def check_diagonal(self, bord, symbol, reverse=False):

        grid = bord.grid
        if reverse is True:  # want to check anti-diagonal
            grid = [row[::-1] for row in grid]  # swap columns
        needed = self.needed_points

        # check all diagonals which start at column 0
        for row_num in range(bord.height):
            max_in_row = 0
            for col_num in range(bord.width):

                remaining_cells = min(bord.height - row_num, bord.width - col_num)
                if not max_in_row + remaining_cells >= needed:  # not possible to make
                    break

                if grid[row_num][col_num] == symbol:
                    max_in_row += 1
                    if max_in_row == needed:  # here comes check
                        return True
                else:
                    max_in_row = 0

                row_num += 1  # increase row
                if row_num >= bord.height:  # avoid index error
                    break

        #  check diagonal starting at row 0
        for j in range(bord.width):
            row_num = 0
            max_in_row = 0
            for col_num in range(1+j, bord.width):
                remaining_cells = min(bord.height - row_num, bord.width - col_num)
                if not max_in_row + remaining_cells >= needed:  # not possible to make
                    break

                if grid[row_num][col_num] == symbol:
                    max_in_row += 1
                    if max_in_row == needed:  # check
                        return True
                else:
                    max_in_row = 0

                row_num += 1

        else:
            return False


class Player:
    def __init__(self, symbol, symbol2, current_game):
        self.symbol = symbol
        self.opponent_symbol = symbol2
        self.game = current_game


class User(Player):
    @staticmethod
    def player_choice(board) -> Tuple[int, int]:
        """check user input and return coordinates of user choice"""
        while True:
            coordinates = input('Enter the coordinates:')
            try:
                row, col = coordinates.split()
                row = int(row)
                col = int(col)
            except ValueError:
                print('You should enter numbers!')
                continue

            if row not in list(range(1, board.height + 1)):
                print(f'Coordinates should be from 1 to {board.height}!')
                continue
            if col not in list(range(1, board.width + 1)):
                print(f'Coordinates should be from 1 to {board.width}!')
                continue

            if board.grid[to_it(row)][to_it(col)] != board.empty_cell_sign:
                print('This cell is occupied! Choose another one!')
                continue

            return row, col


class Easy(Player):
    @staticmethod
    def player_choice(board):
        print('Making move level "easy"')
        return random.choice(list(board.empty_cells))


class Medium(Player):
    def player_choice(self, board):
        print('Making move level "medium')

        # assign coordinates to make win with next move
        coordinates = self.winning_possible(board, self.symbol)

        # assign coordinates needed to block opponent against his win in next move
        if coordinates is None:
            coordinates = self.winning_possible(board, self.opponent_symbol)

        # assign random coordinates from empty_cells list
        if coordinates is None:
            coordinates = random.choice(list(board.empty_cells))

        return coordinates

    def winning_possible(self, board, symbol):
        for coordinates in board.empty_cells:
            c1 = coordinates[0]
            c2 = coordinates[1]
            board.grid[to_it(c1)][to_it(c2)] = symbol  # try move
            if self.game.check_winner(board, symbol):
                board.grid[to_it(c1)][to_it(c2)] = board.empty_cell_sign  # undo
                return coordinates

            # undo try move, so the board is unchanged, I dont need deepcopy
            board.grid[to_it(c1)][to_it(c2)] = board.empty_cell_sign


class Hard(Player):
    minimax_run = 0

    def player_choice(self, board):
        print('Making move level "hard')

        # if board is empty make random move:
        if len(board.empty_cells) == board.height * board.width:
            return random.choice(list(board.empty_cells))

        # else choose the best option from possible moves using minimax
        possible_moves = list(board.empty_cells)
        score, coordinates = self.minimax(board, self.symbol, possible_moves, depth=0, alpha=-999, beta=999)
        # print(f'minimax runs :{self.minimax_run}')
        self.minimax_run = 0
        return coordinates

    def minimax(self, board, current_symbol, possible_moves, depth, alpha, beta):
        self.minimax_run += 1

        # base case, check for final state:
        # if depth >= 5:  # we dont want to go deeper, it cost to much counting
        #     # here should be other algorithm smarter, than random choice
        #     return 0, None

        if self.game.check_winner(board, self.opponent_symbol):  # lose
            return -10, None
        if self.game.check_winner(board, self.symbol):  # win
            return 10, None
        if board.is_full:  # draw
            return 0, None

        best_score = None
        best_coordinates = None

        for coordinates in possible_moves:
            c1 = coordinates[0]
            c2 = coordinates[1]

            # try move, add symbol
            board.grid[to_it(c1)][to_it(c2)] = current_symbol
            # remove current coordinates from possible moves
            reduced_moves = possible_moves[:]
            reduced_moves.remove(coordinates)

            if current_symbol == self.symbol:  # AI Hard
                score = self.minimax(board, self.opponent_symbol, reduced_moves, depth + 1, alpha, beta)[0]

                if best_score is None or score > best_score:
                    best_score = score
                    best_coordinates = coordinates

                alpha = max(alpha, score)
                if beta <= alpha:
                    break

            else:  # opponent
                score = self.minimax(board, self.symbol, reduced_moves, depth + 1, alpha, beta)[0]

                if best_score is None or score < best_score:
                    best_score = score
                    best_coordinates = coordinates

                beta = max(beta, score)
                if beta <= alpha:
                    break

            # undo move, remove symbol
            board.grid[to_it(c1)][to_it(c2)] = board.empty_cell_sign

        return best_score, best_coordinates


if __name__ == '__main__':
    while True:  # __NEW GAME__
        basic_board = Board()
        # basic_board.user_layout()  # if we dont want to start with empty board
        game = Game(basic_board)
        basic_board.print_board()
        while True:  # game rounds loop:
            playing_symbol = game.symbol_turn
            game.move(basic_board)
            basic_board.print_board()
            if game.check_winner(basic_board, playing_symbol):
                print(f'{playing_symbol} wins')
                break
            if basic_board.is_full:
                print('Draw')
                break

            game.change_player()
