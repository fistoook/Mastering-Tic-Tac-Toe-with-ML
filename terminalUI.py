import os

class TerminalUI:
    def greet(self):
        print("\n" + "=" * 45)
        print("      WELCOME TO TIC TAC TOE(S) WITH ML!")
        print("=" * 45)
        print("Type 'help' to see the manual.")

    def read_command(self, agent_name=None):
        if agent_name is None:
            return input("> ")
        return input(f"{agent_name}> ")

    def print_help(self, agent_name=None):
        print("\n" + "=" * 45)
        if agent_name is None:
            print("        COMMANDS")
        else:
            print(f"        {agent_name.upper()} COMMANDS")
        print("=" * 45)

        print("\nhelp / h")
        print("   Show this manual")
        print("\nagents")
        print("   Meet the agents")
        print("\nboard size [size]")
        print("   Change the board size")

        if agent_name is None:
            print("\nagent <aid or name>")
            print("   Pick an agent")
        else:
            print("\nstatus")
            print("   Show this agent's readiness.")
            print("\ntrain [count]")
            print("   Request training.")
            print("\nplay [rival] [count]")
            print("   Pick a rival by id or name.")
            print("\nback")
            print("   Return to agent selection.")

        print("\nclear")
        print("   Clear the terminal.")

        print("\nexit")
        print("   Close the program.")
        print("\nNames and commands ignore case.")
        print("=" * 45)

    def print_agents(self, available_agents):
        print("\n" + "=" * 45)
        print("        CHOOSE YOUR AGENT")
        print("=" * 45)

        for aid, details in available_agents.items():
            name, description = details[:2]
            print(f"\n{aid}. {name}")
            print(f"   {description}")

        print("\nPick one by id or name.")
        print("=" * 45)

    def print_selection(self, agent_name):
        print(f"\nYou selected {agent_name}!")

    def print_status(self, agent_name, agent):
        if agent is None: status = "not trained"
        elif agent.ready: status = "trained"
        else: status = "not trained"
        print(f"{agent_name} is {status}")

    def print_train_request(self, agent_name, count):
        print(f"\n{agent_name} was trained on {count} games succefully. ")

    def print_play_request(self, agent_name, rival_name, count, results):
        print(f"\nStatistics for: {agent_name} vs {rival_name}, {count} games.")
        print(f"Agent {agent_name} won", results["agent_wins"], "times")
        print(f"Rival {rival_name}, won", results["rival_wins"], "times")
        print("there were", results["draws"], "draws")
        print("with an average of", round(results["total_moves"] / count), "moves per game")
    

    def print_back(self):
        print("\nBack to agent selection.")

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def goodbye(self):
        print("\nSee you!")

    def err_invalid_command(self):
        print("Invalid command. Try 'help' to see the manual.")

    def err_unknown_agent(self, choice):
        print(f"Unknown agent: {choice}. Try 'agents' to see the list.")

    def err_no_agent(self):
        print("Pick an agent first. Try 'agents' to see the list.")

    def err_usage(self, usage):
        print(f"Usage: {usage}")

    def err_count(self):
        print("The number of games must be a positive integer.")

# made with luv by fistook :)