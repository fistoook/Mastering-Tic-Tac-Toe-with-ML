from Tournament import Tournament

def main():
    tournament = Tournament(3, 100000)
    tournament.run_tournament()
    tournament.print_results()


if __name__ == "__main__":
    main()