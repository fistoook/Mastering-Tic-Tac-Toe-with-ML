from randomMoves import randomMoves

AGENT = 1
RIVAL = -1
DRAW = 0

class Game:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.free_positions = [(i,j) for i in range(self.board_size) for j in range (self.board_size)]
        self.winner = None
        self.turn = AGENT # Agent begins (hence has an advantage)
        self.game_history= [] # for CSV logging in class Torunament later
        self.random = randomMoves(self)

    def play(self):
        while True:
            turn = self.turn
            pick = self.random.pick_random_move()
            if pick is None: # board full
                self.winner = DRAW
                break

            self.make_a_move(pick)
            won = self.check_win(pick, turn)
            if won:
                self.winner = turn
                break
    
    def make_a_move(self, pick) -> bool:
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
        return True

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
        self.board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.free_positions = [(i,j) for i in range(self.board_size) for j in range (self.board_size)]
        self.winner = None
        self.turn = AGENT
        self.game_history= []