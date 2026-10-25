import random
import pickle # important note: pickel is not secure. only unpickle files you trust!
import numpy as np
from utils import utils
import math
from Game import AGENT, RIVAL, DRAW

# Base Class agent, all other agents inheirt it.
class agent:
    def __init__(self, name, ready=False):
        self.name = name
        self.ready = ready

    def getName(self):
        return self.name

    def isReady(self):
        return self.ready
    
    # define functions signatures for compatability
    # some function are required to be implmented
    # others can be inherted empty
    def pick_move(self, game):
        raise NotImplementedError(
            "Each agent must implement pick_move()."
        )

    def learn(self, winner, boards_log):
        pass # ah... ignorant forever... sorry randy :(

    def save_knowledge(self):
        pass
class randy(agent):
    ''' Meet randy. randy is a dummy. he randomly picks his moves.'''
    def __init__(self):
        super().__init__("Randy", ready=True)

    def pick_move(self, game) -> tuple:
        # pick random move 
        pick_index = random.randint(0, len(game.free_positions) - 1)
        pick = game.free_positions[pick_index]
        return pick

class carlos(agent):
    ''' 
    Oho ho ho, carlo is slick! he uses a dictionary, to pick the best move.
    the dictionary is built using monte carlo reinforncment learning - running a ton of games,
    and rating them based on how often they lead carlo to win
    '''
    def __init__(self):
        super().__init__("Carlos", ready=True)
        self.game_dict = {}
        self.dict_filepath = "dict"
        self.csv_filepath = "games.csv"
        self.hyper_param = 0.8

    def pick_move(self, game) -> tuple:
        if not self.ready:
            raise RuntimeError(f"Agent {self.getName} was not yet trained.")

        if not self.game_dict: # (non empty dictionaries evaluate to True in python)
            try:
                dict_file = open(self.dict_filepath, 'rb')
                self.game_dict = load(self.game_dict, dict_file)
            except:
                raise FileNotFoundError("dictionary file not found. provide it under this directory in 'dict' - or just train again")
        
        best_rating = -math.inf
        best_pick = None
        temp_board = game.board[:]
        for pick in game.free_positions:
            row = pick[0]
            column = pick[1]
            temp_board[row][column] = game.turn
            current_board = tuple(tuple(row) for row in temp_board)
            try:
                rating = self.game_dict[current_board][0]
                if rating > best_rating:
                    best_rating = rating
                    best_pick = pick
            except KeyError:
                raise KeyError(f"Board not found in dictionary, train {self.getName()} on a bigger set.")
            temp_board[row][column] = 0 # bring back the initial state 
            
        return best_pick

    def learn(self, winner, boards_log):
        # the boards come in normal order: first to last. for ease of use, we filp it.
        boards_log = boards_log[::-1] 

        # multiplication factor based on winner
        if winner == AGENT: grade = 1
        elif winner == DRAW: grade = 0.2
        elif winner == RIVAL: grade = 0
        else: raise ValueError("Unknown winner")

        # give each board a rating. 
        for board in boards_log:
            # safely get the current board rating for this board
            curr_rating = self.game_dict.get(board) 

            if curr_rating is None:
                # no records of this board. add the first one:
                self.game_dict[board] = [grade, 1]
            else:
                # update the score to be the average, average formula
                curr_rating[0] = (curr_rating[0] * curr_rating[1] + grade) / (curr_rating[1] + 1)
                curr_rating[1] += 1

            # the further the board away from winner board, the less rating it will get
            grade *= self.hyper_param

    def save_knowledge(self):
        with open(self.dict_filepath, 'wb') as dict_file:
            pickle.dump(self.game_dict, dict_file)
            dict_file.close()