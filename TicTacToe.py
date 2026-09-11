import random
import numpy as np

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

    def initialize_free_positions(self):
        '''initialize the free positions list'''
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.free_positions.append((i,j))

    def play(self):
        while True:
            turn = self.turn
            pick = self.pick_random_move()
            if not pick: # board empty
                self.winner = DRAW
                break # Draw
            self.make_a_move(pick)
            status = self.check_win(pick, turn)
            if status == AGENT:
                self.winner = AGENT
                break # agent won
            elif status == RIVAL:
                self.winner = RIVAL
                break # rival won
    
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
        return True

    def pick_random_move(self):
        if len(self.free_positions) == 0:
            return False # no more free positions - board full
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
        # Now the column
        for i in range(self.board_size):
            if self.board_size[i][column] != turn:
                won = False 
                break
        # and finally the diagonal
        for row in self.board:
            agent_won = True
            rival_won = True
            for item in row: # check if agent wins
                if item != 1: # we have an empty or taken by rival slot -> no win here
                    agent_won = False
                    break

            for item in row: # check if rival wins
                if item != -1: # we have an empty or taken by agent slot -> no win here
                    rival_won = False
                    break

            if rival_won: return -1
            elif agent_won: return 1
            else: continue

        # now we will check the columns
        for column in range(self.board_size):
            agent_won = True
            rival_won = True
            for row in range(self.board_size): # cheeck if agent wins
                if self.board[row][column] != 1:  # we have an empty or taken by rival slot -> no win here
                    agent_won = False
                    break
            for row in range(self.board_size): # check if rival wins
                if self.board[row][column] != -1:  # we have an empty or taken by rival slot -> no win here
                    rival_won = False
                    break

            if rival_won: return -1
            elif agent_won: return 1
            else: continue

        # finally the diagonals

        # diagonal 1
        agent_won = True
        rival_won = True
        for diag in range(self.board_size): # check if agent wins
            if self.board[diag][diag] != 1:
                agent_won = False 
                break

        for diag in range(self.board_size): # check if rival wins
            if self.board[diag][diag] != -1:
                rival_won = False 
                break

        if rival_won: return -1
        elif agent_won: return 1

        # diagonal 2
        agent_won = True
        rival_won = True
        for row in range(self.board_size):
            column = self.board_size - 1 - row
            if self.board[row][column] != 1:
                agent_won = False
                break

        for row in range(self.board_size):
            column = self.board_size - 1 - row
            if self.board[row][column] != -1:
                rival_won = False
                break

        if rival_won: return -1
        elif agent_won: return 1


        return 0

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
        


if __name__ == "__main__":
    game = Game(3)
    game.play()
    print(game.winner)