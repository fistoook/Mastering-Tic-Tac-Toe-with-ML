import random

AGENT = 1
X = 1
RIVAL = -1
O = -1
DRAW = 0
class Game:
    def __init__(self, board_size):
        '''Class Constructor'''
        self.board_size = board_size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.free_positions = []
        self.initialize_free_positions()
        self.winner = None
        self.turn = AGENT
        self.game_history= []

    def initialize_free_positions(self):
        '''initialize the free positions list'''
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.free_positions.append((i,j))

    def play(self):
        while True:
            turn = self.turn
            pick = self.pick_random_move()
            if pick is None: # board full
                self.winner = DRAW
                break # Draw
            self.make_a_move(pick)
            won = self.check_win(pick, turn)
            if won:
                self.winner = turn
                break
    
    def make_a_move(self, pick):
        row = pick[0]
        column = pick[1]
        if self.turn == AGENT: 
            self.board[row][column] = X
            self.turn = RIVAL
        else: 
            self.board[row][column] = O
            self.turn = AGENT

        self.free_positions.remove(pick)
        self.game_history.append(pick)
        return True

    def pick_random_move(self):
        if len(self.free_positions) == 0:
            return None # no more free positions - board full
        # pick random move 
        pick_index = random.randint(0, len(self.free_positions) - 1)
        pick = self.free_positions[pick_index]
        return pick

    def check_win(self, pick, turn):
        # instead of checking all of the O(n^2) itmes, with rows -> column -> diagonal scan,
        # wee will scan only the row and column of the current move, in O(n) :)
        won = True
        row = pick[0]
        column = pick[1]
        # First we will check the row
        for item in self.board[row]:
            if item != turn:
                won = False
                break
        if won: return won
        won = True
        # Now the column
        for i in range(self.board_size):
            if self.board[i][column] != turn:
                won = False 
                break
        if won: return won
        # and finally the diagonals
        if row == column:
            won = True
            for diag in range(self.board_size): 
                if self.board[diag][diag] != turn:
                    won = False 
                    break
        if won: return won
        if row + column == self.board_size - 1:
             won = True
             for diag in range(self.board_size):
                column = self.board_size - 1 - diag
                if self.board[diag][column] != turn:
                    won = False
                    break

        return won

    def print_board(self):
        for row in self.board:
            print(*row)
        print()

    def reset_game(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.free_positions = []
        self.initialize_free_positions()
        self.winner = None
        self.turn = AGENT
        self.game_history= []