class utils:
    def __init__(self):
        pass

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

    
    def _log_game(self, game_id, winner, game_history):
        moves = []
        for row, column in game_history:
            moves.append(f"({row};{column})")
        self.total_moves += len(moves)

        missing_moves = self.max_moves - len(moves)
        moves.extend([""] * missing_moves) # pad the empty slots for the csv

        game_row = [game_id] + moves + [self.game.winner]
        self.results.append(game_row)

        self.update_score(winner)