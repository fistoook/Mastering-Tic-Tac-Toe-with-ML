from Game import AGENT, RIVAL, DRAW
from agents import randy, carlos

class master:
    ''' 
    Manages and trains the agents, and then exploits them
    for his own good!
    '''
    def __init__(self, board_size):
        self.board_size = board_size
        self.available_agents = {
            "1": (
                "Randy",
                "Randy is a dum dum. randomly picks moves.",
                randy
            ),
            "2": (
                "Carlos",
                "Carlos uses reinforcment learning with a monte carlo built dictionary",
                carlos
            )
        }
        self.agent_count = len(self.available_agents)
        self.agent = None
        self.game = None
        self.max_moves = board_size ** 2
        self.summary = []
        self.results = {
            "agent_wins": 0,
            "rival_wins": 0,
            "draws": 0,
            "total_moves": 0
        }

    def _init_agent(self, agent_class):
        self.agent = agent_class(self.board_size)
        self.game = self.agent.game

    def pick_agent(self):
        print("\n" + "=" * 45) # you can do that?! 
        print("        CHOOSE YOUR AGENT")
        print("=" * 45) # I am never coming back to manully holding = again

        for number, (name, description, _) in self.available_agents.items():
            print(f"\n{number}. {name}")
            print(f"   {description}")

        print("\n" + "=" * 45)

        while True:
            choice = input(f"\nYour choice (1-{self.agent_count}): ").strip()

            if choice not in self.available_agents:
                print("Bruh")
                continue

            name, description, agent_class = self.available_agents[choice]

            self._init_agent(agent_class)

            print(f"\nYou selected {name}!")
            return self.agent

    def train_agent(self, count):
        # notice we do not train the here
        # we just ask them to train :)
        # they train in agents.py
        if self.agent is None:
            raise RuntimeError("Please select an agent first.")

        self.agent.train(count)

    def play(self, count):
        if self.agent is None:
            raise RuntimeError("Please select an agent first.")
        if count < 1:
            raise ValueError("Number of games must be positive.")

        # Reset statistics for this tournament
        for key in self.results: self.results[key] = 0

        for game_id in range(1, count + 1):
            self.game.reset_game()

            winner, game_history, boards_log = self.game.play()

            self._update_score(winner)
            self.results["total_moves"] += len(boards_log)

        self._print_results(count)

    def _update_score(self, winner):
        if winner == AGENT: self.results["agent_wins"] += 1
        elif winner == RIVAL: self.results["rival_wins"] += 1
        else: self.results["draws"] += 1

    def _print_results(self):
        print(f"Agent {self.agent.getName()} won", self.total_agent_wins, "times")
        print("Rival won", self.total_rival_wins, "times")
        print("there were", self.draws, "draws")
        print("with an average of", round(self.total_moves / self.count), "moves per game")