from master import master

def get_board_size():
    while True:
        try:
            size = int(input("\nChoose the board size: "))

            if size >= 3:
                return size

            print("The board must be at least 3x3!")

        except ValueError:
            print("Please enter a valid integer.")


def main():
    print("\n" + "=" * 45)
    print("      WELCOME TO TIC TAC TOE(S) WITH ML!")
    print("=" * 45)

    board_size = get_board_size()

    master_of_puppets = master(board_size)

    agent = master_of_puppets.pick_agent()

    print(f"\n{agent.getName()} is ready for action!")

    # Next steps, once all agent methods are implemented:
    #
    # master_of_puppets.train_agent(10000)
    # master_of_puppets.play(100)


if __name__ == "__main__":
    main()
