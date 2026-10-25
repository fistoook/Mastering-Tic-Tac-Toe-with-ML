from terminalUI import TerminalUI as TUI

EXIT = 22
DEFAULT_TRAIN_COUNT = 10000

class Parser:
    ''' 
    The parser is in charge of getting user input and parsing the commands.
    As a terminal enthusisat, I could not be happier to make this into a command line tool.
    the parser has two states: user mode, and agent mode; kinda like an OS I guess ?.. :P
    user mode it the initial mode, which has command like help, clear, agents.
    once you enter agent {id/name} you enter agent mode for that agent, where you can train or play it.
    '''
    def __init__(self, master, ui=None):
        self.ui = ui if ui is not None else TUI()
        self.master = master

        self.available_agents = master.available_agents
        self.agent_id = None

    def run(self):
        # greet the user
        self.ui.greet()

        while True:
            try:
                # read user command
                command = self.ui.read_command(self.get_agent_name())
            except (EOFError, KeyboardInterrupt):
                # on error, bye bye
                self.ui.goodbye()
                break

            # parse the user command
            if self.parse_command(command) == EXIT:
                break

    def parse_command(self, command) -> int:
        # remove whiespaces, send to lowercase and split into words
        words = command.strip().casefold().split()

        if not words: return 1 # empty

        # IDK what it is but I think match cases are so much nicer then ifs
        match words:
            case ["help" | "h"]:
                # print help
                self.ui.print_help(self.get_agent_name())
            case ["agents"]:
                # print agents
                self.ui.print_agents(self.available_agents)
            case ["clear"]:
                # clear screen (You're welcome)
                self.ui.clear()
            case ["exit"]:
                # exit
                self.ui.goodbye()
                return EXIT # exit code
            case _:
                # default case
                if self.agent_id is None: self.parse_selection(words) 
                else: self.parse_agent_command(words) # agent mode has special commands
        return 1

    def get_agent_name(self):
        return None if self.agent_id is None else self.available_agents[self.agent_id][0]

    def get_agent_status(self):
        return None if self.agent_id is None else self.master.agents.get(self.agent_id)

    def parse_selection(self, words):
        match words:
            case ["status"] | ["train", *_] | ["play", *_] | ["back"]:
                # running aget mode command in user mode
                self.ui.err_no_agent()
            case ["agent"]:
                # invalid usage
                self.ui.err_usage("agent <aid or name>")
            case ["agent", choice] | [choice]:
                # pick agent
                self.pick_agent(choice)
            case ["board", "size", size]:
                self.master.board_size = self.ui.pick_board_size()
                self.master.utils.modify_board_size(self.master.board_size)
            case _:
                self.ui.err_usage("agent <aid or name>")

    
    def parse_agent_command(self, words):
        match words:
            case ["status"]:
                self.ui.print_status(self.get_agent_name(), self.get_agent_status())
            case ["train", *arguments]:
                self.parse_train(arguments)
            case ["play", *arguments]:
                self.parse_play(arguments)
            case ["back"]:
                self.agent_id = None
                self.ui.print_back()
            case _:
                self.ui.err_invalid_command()

    def find_agent(self, choice):
        choice = choice.strip().casefold()
        for aid, details in self.available_agents.items():
            if choice == str(aid).casefold() or choice == details[0].casefold():
                return aid
        return None

    def pick_agent(self, choice):
        aid = self.find_agent(choice)
        if aid is None:
            self.ui.err_unknown_agent(choice)
            return

        self.agent_id = aid
        self.ui.print_selection(self.get_agent_name())

    def parse_count(self, value):
        try:
            count = int(value)
        except ValueError:
            self.ui.err_count()
            return None

        if count < 1:
            self.ui.err_count()
            return None
        return count

    def parse_train(self, arguments):
        if len(arguments) > 1:
            self.ui.err_usage("train [count]")
            return

        count = DEFAULT_TRAIN_COUNT
        if arguments:
            count = self.parse_count(arguments[0])
            if count is None:
                return

        try:
            success = self.master.train_agent(self.agent_id, count)
            if success:
                self.ui.print_train_request(self.get_agent_name(), count)
        except FileNotFoundError as f:
            print(f)

    def parse_play(self, arguments):
        if len(arguments) > 2:
            self.ui.err_usage("play [rival] [count]")
            return

        if arguments:
            rival_id = self.find_agent(arguments[0])
            if rival_id is None:
                self.ui.err_unknown_agent(arguments[0])
                return
        else:
            rival_id = next(iter(self.available_agents))

        count = 1
        if len(arguments) == 2:
            count = self.parse_count(arguments[1])
            if count is None:
                return

        rival_name = self.available_agents[rival_id][0]
        results = self.master.play(self.agent_id, rival_id, count)
        self.ui.print_play_request(self.get_agent_name(), rival_name, count, results)
