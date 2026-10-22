import random

class randomMoves():
    def __init__(self, game):
        self.game = game

    def pick_random_move(self) -> tuple:
        if len(self.game.free_positions) == 0:
            return None # no more free positions - board full
        
        # pick random move 
        pick_index = random.randint(0, len(self.game.free_positions) - 1)
        pick = self.game.free_positions[pick_index]
        return pick