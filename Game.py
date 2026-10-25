AGENT = 1
RIVAL = -1
DRAW = 0

class Game:
    def __init__(self, board_size, agent, rival):
        self.board_size = board_size
        self.board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.free_positions = [(i,j) for i in range(self.board_size) for j in range (self.board_size)]
        self.winner = None
        self.turn = AGENT # Agent begins (hence has an advantage)
        self.game_history = []
        self.boards_log = []
        self.agent = agent
        self.rival = rival

    def play(self) -> tuple:
        while True:
            pick = self.pick_move() # pick move
            game_over = self.apply_move(pick) # apply it
            if game_over: break

        return (self.winner, self.game_history, self.boards_log)
    
    def pick_move(self) -> tuple:
        if self.turn == AGENT:
            pick = self.agent.pick_move(self)
            if pick is None: 
                raise RuntimeError(f"Agent {self.agent if self.turn ==  AGENT else self.rival} spit out garbage.")
        elif self.turn == RIVAL:
            pick = self.rival.pick_move(self)
            if pick is None: 
                raise RuntimeError(f"Agent {self.agent if self.turn ==  AGENT else self.rival} spit out garbage.")
        return pick

    def apply_move(self, pick):
        # validate move
        if pick not in self.free_positions: 
            raise RuntimeError(f"Agent {self.agent if self.turn ==  AGENT else self.rival} spit out garbage.")

        # mark it on the board
        row = pick[0]
        column = pick[1]
        self.board[row][column] = self.turn

        # record the move
        self.free_positions.remove(pick) 
        self.game_history.append(pick)
        current_board = tuple(tuple(row) for row in self.board) # convert to tuple to use as dict key later
        self.boards_log.append(current_board)

        # check for winner
        if self.check_win(pick, self.turn):
            self.winner = self.turn
            return True # signal game over

        # check if the board is full
        if len(self.free_positions) == 0:
            self.winner = DRAW
            return True # no more free positions - board full

        # switch player
        self.turn = self.turn = RIVAL if self.turn == AGENT else AGENT
        return False # signal game not over


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