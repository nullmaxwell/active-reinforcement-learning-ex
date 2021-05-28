import sys
from src.State import *
from src.Solution import *
from src.Hyperparameters import *

def main(argv):
    sys.tracebacklimit = 0
    Solution.initialize()

    HYPER.ITERATIONS = Solution.checkIterationArg(argv[0])
    HYPER.MAX_ERROR = Solution.checkErrorArg(argv[1])

    Solution.explore()
    Solution.calcOptimal()
    Solution.showOptimalPolicy()
if __name__ == '__main__':
    main(sys.argv[1:])