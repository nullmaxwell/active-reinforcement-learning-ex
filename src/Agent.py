import numpy as np
from src.State import *
from src.Exceptions import *
from src.Hyperparameters import * 

class Agent:
    """Acting agent through the environment."""
    @staticmethod
    def checkIterationArg(arg):
        """Ensures the iteration commandline argument is the correct format."""
        try:
            arg = int(arg)
        except ValueError as exc:
            raise ArgumentTypeError(arg) from exc

        if arg <= 0:
            raise IterationRangeError(arg)
        else:
            return(arg)

    @staticmethod
    def checkErrorArg(arg):
        """Ensures the max error commandline argument is the correct format."""
        try:
            arg = float(arg)
        except ValueError as exc:
            raise ArgumentTypeError(arg) from exc

        if arg <= 1.0 and arg > 0.0:
            return arg
        else:
            raise IterationRangeError(arg)

    @staticmethod
    def initialize():
        """Reads problem data in from data folder and initializes select Hyperparameters."""
        with open('data/reinforcement_maze.txt') as init_file:
            arr = []
            lines = init_file.read().splitlines()
            lineCount = len(lines)

            for x in range(0, int(lineCount/3)):
                mult = (3 * x)

                if(mult == 0):
                    HYPER.NUM_ACTIONS = int(lines[0])
                    HYPER.NUM_STATES = int(lines[1])
                    HYPER.GAMMA = float(lines[2])
                else:
                    temp_state = State(
                        str(x), 
                        float(lines[mult]),
                        bool(int(lines[mult + 1])),
                        str(lines[mult + 2]),
                        np.zeros((HYPER.NUM_ACTIONS, HYPER.NUM_STATES)),
                        0,
                        "None",
                        np.zeros((HYPER.NUM_ACTIONS, HYPER.NUM_STATES)),  
                        [1,1,1,1]
                    )
                    arr.append(temp_state)

        init_file.close()
        HYPER.STATES = arr

    @staticmethod
    def explore():
        """Builds probability statistics for the state's probability matrix by tracking possible and past decisions."""
        print(" ")
        print("Exploring and Building statistics...")
        print(" ")

        iteration_counter = 0

        while True:
            iteration_counter += 1
            isu = [] # Iteration State Utilities
            isp = [] # Iteration State Probability Matricies

            for iter in HYPER.STATES:
                isu.append(iter.utility)
                isp.append(iter.pmat)

            for state in HYPER.STATES:
                prev_util = state.utility                
                state.bellmanExplore(isu, isp) # utility updates
                state.pmat = state.updatePMAT()

            if(state.utility - prev_util > HYPER.DELTA):
                    HYPER.DELTA = state.utility - prev_util

            # Breaking Condition
            if(HYPER.DELTA < ((HYPER.MAX_ERROR)*(1-HYPER.GAMMA)/(HYPER.GAMMA)) or iteration_counter > HYPER.ITERATIONS):
                break

    @staticmethod
    def calcOptimal():
        """Calculates the final state utility and writes the optimal policy for that state."""
        for x in range(0, HYPER.ITERATIONS):
            isu = []
            isp = []
            for iter in HYPER.STATES:
                isu.append(iter.utility)
                isp.append(iter.pmat)

            for state in HYPER.STATES:
                state.bellmanOptimize(isu) # utility updates
                if state.terminal == True:
                    state.opt_pol = state.encodePolicy(46)

    @staticmethod
    def showOptimalPolicy():
        """Prints the optimal policy for each state in a legible format."""
        print("Optimal Policy: ")
        print(" ")
        for state in HYPER.STATES:
            print("State " + str(state.name) + " Utility: " + format(state.utility, '.3f') + " Decision: " + str(state.opt_pol))