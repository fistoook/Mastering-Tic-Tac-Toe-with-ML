from Tournament import Tournament

def main():
    tournament = Tournament(3, 100, 0.8)
    tournament.run_tournament()
    tournament.print_results()


if __name__ == "__main__":
    main()