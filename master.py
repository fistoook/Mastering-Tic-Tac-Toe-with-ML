from Game import AGENT, RIVAL, DRAW, Game
from agents import randy, carlos
from utils import utils
class Master:
    ''' 
    Manages and trains the agents, and then exploits them
    for his own good!
    '''
    def __init__(self, board_size=3):
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
        self.agents = {}
        self.agent_count = len(self.available_agents)
        self.max_moves = self.board_size ** 2
        self.summary = []
        self.results = {
            "agent_wins": 0,
            "rival_wins": 0,
            "draws": 0,
            "total_moves": 0
        }
        self.games_list = []
        self.utils = utils(board_size)

    def train_agent(self, agent_id, count) -> bool:
        try:
            agent = self.get_agent(agent_id)
        except ValueError:
            return False

        game = Game(self.board_size, randy(), randy())
        for game_id in range(1, count+1): 
            #play game
            results = game.play() 

            # unpack results
            winner = results[0]
            game_history = results[1]
            boards_log = results[2]

            # record results
            self._update_score(winner)
            self.utils.log_game(self, game_id, winner, game_history)

            # learn! learn!
            agent.learn(winner, boards_log)

            # reset before starting over
            game.reset_game()

        # log games into games.csv
        success = self.utils.log_results(self)

        # save to dictionary for carlos
        agent.save_knowledge()

        agent.ready = True

        return agent.ready

    def get_agent(self, agent_id):
        if agent_id not in self.available_agents:
            raise ValueError(f"Unknown agent ID: {agent_id}")

        if agent_id not in self.agents:
            agent_class = self.available_agents[agent_id][2]
            self.agents[agent_id] = agent_class()

        return self.agents[agent_id]

    def play(self, agent_id, rival_id, count) -> dict:
        try: 
            agent = self.get_agent(agent_id)
            rival = self.get_agent(rival_id)
        except ValueError:
            raise RuntimeError("Agent id inavlid")
        
        if count < 1:
            raise ValueError("Number of games must be positive.")

        # Reset statistics for this tournament
        for key in self.results: self.results[key] = 0

        # create the game instance
        game = Game(self.board_size, agent, rival)

        for game_id in range(1, count + 1):
            game.reset_game()

            try:
                winner, game_history, boards_log = game.play()
            except RuntimeError as r:
                print(r)
            except FileNotFoundError as f:
                print(f)
            except KeyError as k:
                print(k)

            self._update_score(winner)
            self.results["total_moves"] += len(boards_log)

        return self.results

    def _update_score(self, winner):
        if winner == AGENT: self.results["agent_wins"] += 1
        elif winner == RIVAL: self.results["rival_wins"] += 1
        else: self.results["draws"] += 1