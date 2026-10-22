from agents import *

AGENT = 1
RIVAL = -1
DRAW = 0

class Game:
    def __init__(self, board_size, agent):
        self.board_size = board_size
        self.board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.free_positions = [(i,j) for i in range(self.board_size) for j in range (self.board_size)]
        self.winner = None
        self.turn = AGENT # Agent begins (hence has an advantage)
        self.game_history = []
        self.boards_log = []
        self.agent = agent

    def play(self) -> tuple:
        while True:
            turn = self.turn
            pick = self.make_a_move()

            if pick is None: 
                break 

            if self.check_win(pick, turn):
                self.winner = turn
                break

        return (self.winner, self.game_history, self.boards_log)
    
    def make_a_move(self) -> tuple:
        pick = self.agent.pick_move()
        if pick is None: # board full
            self.winner = DRAW
            return None
        
        row = pick[0]
        column = pick[1]
        if self.turn == AGENT: 
            self.board[row][column] = AGENT
            self.turn = RIVAL
        else: 
            self.board[row][column] = RIVAL
            self.turn = AGENT

        self.free_positions.remove(pick) 
        self.game_history.append(pick)
        current_board = tuple(tuple(row) for row in self.board) # convert to tuple to use as dict key
        self.boards_log.append(current_board)

        return pick

    def check_win(self, pick, turn) -> bool:
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
        self.board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.free_positions = [(i,j) for i in range(self.board_size) for j in range (self.board_size)]
        self.winner = None
        self.turn = AGENT
        self.game_history = []
        self.boards_log = []