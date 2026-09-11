import numpy as np
from TicTacToe import Game

class Tournament:
    def __init__(self, board_size, count):
        self.game = Game(board_size)
        self.count = count
        self.max_moves = board_size ** 2
        self.results = []
        self.total_agent_wins = 0
        self.total_rival_wins = 0
        self.draws = 0
        self.total_moves = 0

    def run_tournament(self):
        for game_id in range(1, self.count+1):
            self.game.play()
            self.log_game(game_id)
            self.game.reset_game()

        self.save_results("TicTacToeGames.csv")

    def log_game(self, game_id ):
        moves = []
        for row, column in self.game.game_history:
            moves.append(f"({row};{column})")
        self.total_moves += len(moves)
        missing_moves = self.max_moves - len(moves)
        moves.extend([""] * missing_moves)
        game_row = [game_id] + moves + [self.game.winner]
        if self.game.winner == 1: self.total_agent_wins+=1
        elif self.game.winner == -1: self.total_rival_wins+=1
        else: self.draws+=1
        self.results.append(game_row)

    def save_results(self, file_path):
        headers = ["game_id"]

        for move_number in range(1, self.max_moves + 1):
            headers.append(f"move_{move_number}")

        headers.append("winner")

        results_array = np.asarray(self.results, dtype=str)

        np.savetxt(
            file_path,
            results_array,
            delimiter=",",
            fmt="%s",
            header=",".join(headers),
            comments="",
            encoding="utf-8"
        )

    def print_results(self):
        print("Agent won", self.total_agent_wins, "times")
        print("Rival won", self.total_rival_wins, "times")
        print("there were", self.draws, "draws")
        print("with an average of", round(self.total_moves/100000), "moves per game")

