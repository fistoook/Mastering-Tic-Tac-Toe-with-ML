from TicTacToeTournament import Tournament

if __name__ == "__main__":
    tournament = Tournament(3, 100000)
    tournament.run_tournament()
    tournament.print_results()