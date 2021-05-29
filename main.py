import sys
from src.State import *
from src.Agent import *
from src.Hyperparameters import *

def main(argv):
    sys.tracebacklimit = 0
    Agent.initialize()

    HYPER.ITERATIONS = Agent.checkIterationArg(argv[0])
    HYPER.MAX_ERROR = Agent.checkErrorArg(argv[1])

    Agent.explore()
    Agent.calcOptimal()
    Agent.showOptimalPolicy()
if __name__ == '__main__':
    main(sys.argv[1:])