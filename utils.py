import numpy as np

class utils:
    def __init__(self, board_size):
        self.board_size = board_size
        self.max_moves = self.board_size ** 2

    def modify_board_size(self, new_size):
        self.board_size = new_size
        self.max_moves = self.board_size ** 2

    def _print_game_dict(self, limit=70):
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

    
    def log_game(self, master, game_id, winner, game_history):
        moves = []
        for row, column in game_history:
            moves.append(f"({row};{column})")

        missing_moves = self.max_moves - len(moves)
        moves.extend([""] * missing_moves) # pad the empty slots for the csv

        game_row = [game_id] + moves + [winner]
        master.games_list.append(game_row)


    def log_results(self, master) -> bool:
        try:
            headers = ["game_id"]

            for move_number in range(1, master.max_moves + 1):
                headers.append(f"move_{move_number}")

            headers.append("winner")

            results_array = np.asarray(self.results, dtype=str)

            np.savetxt(
                self.csv_filepath,
                results_array,
                delimiter=",",
                fmt="%s",
                header=",".join(headers),
                comments="",
                encoding="utf-8"
            )

            return True 
        except: 
            return False