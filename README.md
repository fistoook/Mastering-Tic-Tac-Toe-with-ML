# Tic Tac Toe(s) with Machine Learning

I forced my machine to play millions of games of Tic Tac Toe. Poor thing.

This project's purpose is to learn different machine learning techniques by using them to teach agents to excel at Tic Tac Toe.

## Project structure

### `main.py`

The entry point: it creates the `Master` and `Parser`, then starts the command loop.

### `parser.py` and `terminalUI.py`

The parser gets user commands from the terminal using `TerminalUI`, implemented in `terminalUI.py`. The commands are predefined and can be viewed with `help`. I am a huge lover of command line tools, so this was really fun to play around with, and I honestly love the final result.

The parser handles simple commands like viewing the manual (`help`) or listing the available agents (`agents`), which are simple prints. More complex commands involving the agents themselves are passed on to the `Master`, which you can find in `master.py`.

### `master.py`

The Master is the orchestrator of the agents: he initializes their objects, stores them in a dictionary by agent ID, and manages training and matches. When a command like `train` comes in through the terminal, the parser passes the instruction to the Master with the corresponding agent. The Master runs practice games and passes their results and boards to that agent's `learn()` method.

### `agents.py`

The move selection and learning code for the different agents lives in `agents.py`. There you will find agents such as Randy (the random move picker) and Carlos (based on Monte Carlo learning), which inherit basic properties and methods from the base class, `agent`.

All agents share methods with the same names and signatures for compatibility and scalability. The Master does not need special handling for each agent, which makes things a lot easier and clearer.

### `Game.py`

The game logic is implemented in the `Game` class in `Game.py`. This includes the straightforward game loop and functions like checking whether the game has ended:

```text
Pick a move -> Apply it -> Check whether the game has ended -> Repeat
```

### `utils.py`

The `utils` class mainly contains "pretty" printing functions for debugging and CSV saving functions for, well, also debugging. Training games are saved to `outputs/games.csv`.

## About the agents

### Randy

Randy just randomly picks a legal move and, well, that's it.

### Carlos

Carlos uses Monte Carlo learning to build a dictionary of `{board: [rating, visit_count]}` by observing a ton of games between two Randys and evaluating their outcomes.

The ratings estimate the average discounted reward from the first player's (`+1`) point of view. A win for that player starts with a reward of `1`, a draw with `0.2`, and a loss with `0`. Earlier boards receive discounted rewards.

When Carlos plays, he checks all the possible next boards and their ratings. As the first player, he picks the highest-rated board; as the second player (`-1`), he picks the lowest-rated one.

More agents will appear as I actually code them :)

## How can you play around with this?

You will need Git and **Python 3.10 or newer**. The code also uses NumPy, which you can install below.

Clone the repo from your terminal of choice, enter the project folder, install NumPy, and run `main.py`:

```sh
git clone https://github.com/fistoook/Mastering-Tic-Tac-Toe-with-ML.git
cd Mastering-Tic-Tac-Toe-with-ML
python -m pip install numpy
python main.py
```

If your system uses `python3` for Python 3, use that instead of `python` in the commands above.
(if you are on windows it is probably just pyhton)

Run the program from the project folder so it can find Carlos's saved dictionary (`dict`) and write the training log (`outputs/games.csv`). The `outputs` directory must exist for CSV export; it is included in the repo.

Once you are in, try:

```text
> help
> agents
> agent randy
Randy> play randy 100
Randy> back
> exit
```

You can select an agent by ID or name, with or without the `agent` prefix. The prompt changes to the selected agent's name. Use `help` or `h` in either mode to see the available commands.

To try Carlos, select him with `agent carlos`, then use `play randy 100`. He loads the saved `dict` file when he first needs it. You can also use `train [count]` to train him on more random games; the default is 10,000 games. Training saves his current in-memory dictionary to `dict`, replacing the existing file.

### Current limitation

Carlos currently stops a match if any candidate board is missing from his dictionary. Training on more games can help, but it does not guarantee that every board will be covered. Start with the default 3x3 board; a different board size needs training data for that size.

## A note about pickle

Only download and use the code if you trust it.

The code uses `pickle` to save and load Carlos's dictionary. Loading an untrusted pickle file can execute arbitrary code, so only use a `dict` file you trust. All I am saying is use it with caution. I have absolutely no intent of doing anything bad :) This code is free so that others can learn from it :)
