from parser import Parser
from master import Master

def main():
    master = Master()
    parser = Parser(master=master)
    parser.run()


if __name__ == "__main__":
    main()
