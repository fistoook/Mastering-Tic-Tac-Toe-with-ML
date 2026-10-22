import random
import pickle # important note: pickel is not secure. only unpickle files you trust!
from Game import *
import numpy as np
from utils import utils

class randy:
    ''' Meet randy. randy is a dummy. he randomly picks his moves.'''
    def __init__(self):
        self.name = "Randy"

    def getName(self):
        return self.name # sorry I had to do it :)
    
    def train(self, count):
        pass # who need to train these days?

    def pick_move(self) -> tuple:
        if len(self.game.free_positions) == 0:
            return None # no more free positions - board full
        
        # pick random move 
        pick_index = random.randint(0, len(self.game.free_positions) - 1)
        pick = self.game.free_positions[pick_index]
        return pick



class carlos:
    ''' 
    Oho ho ho, carlo is slick! he uses a dictionary, to pick the best move.
    the dictionary was built using monte carlo reinforncment learning - running a ton of games,
    and rating them based on how often they lead carlo to win
    '''
    def __init__(self, board_size):
        self.game = Game(board_size, self)
        self.name = "Carlo"

        self.game_dict = {}
        self.hyper_param = 0.8
        self.max_moves = board_size ** 2

        self.results = []

    def getName(self):
        return self.name
    
    def train(self, count):
        for game_id in range(1, count+1):
            results = self.game.play() 
            winner = results[0]
            game_history = results[1]
            boards_log = results[2]
            self.update_score()
            self._log_game(game_id, winner, game_history)
            self._update_dict(winner, boards_log)
            self.game.reset_game()

        self._save_results("Games.csv", "dict")

    def pick_move(self):
        raise NotImplementedError(
            "Carlo is still learning how to choose moves!"
        )
    def _update_dict(self, winner, boards):
            boards = boards[::-1] # flip him
    
            if winner == AGENT: grade = 1
            elif winner == DRAW: grade = 0.2
            elif winner == RIVAL: grade = 0
            else: raise ValueError("Unknown winner")
    
            for board in boards:
                curr_value = self.game_dict.get(board)
                if curr_value is None:
                    self.game_dict[board] = [grade, 1]
                else:
                    curr_value[0] = (curr_value[0] * curr_value[1] + grade) / (curr_value[1] + 1)
                    curr_value[1] += 1
                grade *= self.hyper_param

    def _save_results(self, games_file_path, dict_file_path):
        headers = ["game_id"]

        for move_number in range(1, self.max_moves + 1):
            headers.append(f"move_{move_number}")

        headers.append("winner")

        results_array = np.asarray(self.results, dtype=str)

        np.savetxt(
            games_file_path,
            results_array,
            delimiter=",",
            fmt="%s",
            header=",".join(headers),
            comments="",
            encoding="utf-8"
        )

        dict_file = open(dict_file_path, 'wb')
        pickle.dump(self.game_dict, dict_file)
        dict_file.close()