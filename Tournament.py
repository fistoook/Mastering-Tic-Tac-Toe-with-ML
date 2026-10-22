import numpy as np
from Game import *
import pickle
class Tournament:
    def __init__(self, board_size, count, hyper_param):
        self.game = Game(board_size)
        self.count = count
        self.max_moves = board_size ** 2
        self.results = []
        self.total_agent_wins = 0
        self.total_rival_wins = 0
        self.draws = 0
        self.total_moves = 0 # in all games
        self.game_dict = {}
        self.hyper_param = hyper_param
        self.boards_processed = 0

    def run_tournament(self):
        for game_id in range(1, self.count+1):
            results = self.game.play() 
            winner = results[0]
            game_history = results[1]
            boards_log = results[2]
            self.log_game(game_id, winner, game_history)
            self.update_dict(winner, boards_log)
            self.game.reset_game()

        self.save_results("TicTacToeGames.csv")

    def log_game(self, game_id, winner, game_history):
        moves = []
        for row, column in game_history:
            moves.append(f"({row};{column})")
        self.total_moves += len(moves)

        missing_moves = self.max_moves - len(moves)
        moves.extend([""] * missing_moves) # pad the empty slots for the csv

        game_row = [game_id] + moves + [self.game.winner]
        self.results.append(game_row)

        if winner == AGENT: self.total_agent_wins += 1
        elif winner == RIVAL: self.total_rival_wins += 1
        else: self.draws += 1

    def update_dict(self, winner, boards):
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
        print("with an average of", round(self.total_moves / self.count), "moves per game")
        self.print_game_dict()

    def print_game_dict(self, limit=70):
        # Convert the numerical board representation into symbols
        symbols = {
            1: "X",
            -1: "O",
            0: " "
        }

        # Sort dictionary entries by appearance count
        sorted_boards = sorted(
            self.game_dict.items(), # turn dict key + value into tuple (key, value)
            key=lambda item: item[1][1],
            reverse=True
        )

        # Keep only the requested number of boards
        sorted_boards = sorted_boards[:limit]

        # Print each board and its statistics
        for index, (board, data) in enumerate(sorted_boards, start=1):
            score, count = data
            print(f"\n{'=' * 35}")
            print(f"BOARD #{index}")
            print(f"Score: {score:.4f}")
            print(f"Appearances: {count}")
            print("-" * 35)

            # Print the board row by row
            for row_index, row in enumerate(board):

                # Convert each cell to its corresponding symbol
                cells = [symbols[cell] for cell in row]

                print(" " + " | ".join(cells))

                # Separate rows (except after the last one)
                if row_index < 2:
                    print("---+---+---")

        print(f"\nTotal unique boards: {len(self.game_dict)}")