import random
import numpy as np
from src.Hyperparameters import *

class State:
    def __init__(self, name, reward, terminal, info, pmat, 
        utility, opt_pol, destinationTicker, actionTicker):
        self.name = name
        self.reward = reward
        self.terminal = terminal
        self.info = info
        self.pmat = pmat
        self.utility = utility
        self.opt_pol = opt_pol
        self.destinationTicker = destinationTicker
        self.actionTicker = actionTicker


    def bellmanExplore(self, isu, isp):
        """Bellman Equation to be used while exploring the grid to create the probablility matricies. 
        This function updates the utility of the State object."""
        sum_arr = []
        util_arr = []
        p_matrix = isp[int(self.name) - 1]
        for x in range(0, HYPER.NUM_ACTIONS):
            sum_arr = []
            for y in range(0, HYPER.NUM_STATES):
                temp = p_matrix.item((x,y)) * (isu[y])
                sum_arr.append(temp)
            util_arr.append(sum(sum_arr))

        try:
            explore = np.random.choice(np.arange(2), p = HYPER.EXPLORATION_RATE)
            if explore == 1:
                choice = random.randint(0, HYPER.NUM_ACTIONS - 1)
                self.updateTrackers(choice)
                self.opt_pol = self.encodePolicy(choice)
                self.utility = self.reward + ((HYPER.GAMMA) * util_arr[choice])
            if explore == 0:
                choice = util_arr.index(max(util_arr))
                self.updateTrackers(choice)
                self.opt_pol = self.encodePolicy(choice)
                self.utility = self.reward + ((HYPER.GAMMA) * max(util_arr))
        except IOError:
            return self.reward


    def bellmanOptimize(self, isu):
        """Computes the final utility and policy of the State object."""
        sum_arr = []
        util_arr = []

        for x in range(0, HYPER.NUM_ACTIONS):
            sum_arr = []
            for y in range(0, HYPER.NUM_STATES):
                temp = self.pmat.item((x,y)) * (isu[y])
                sum_arr.append(temp)
            util_arr.append(sum(sum_arr))
        choice = util_arr.index(max(util_arr))
        self.opt_pol = self.encodePolicy(choice)
        self.utility = (self.reward + ((HYPER.GAMMA) * max(util_arr)))


    def updateTrackers(self, choice):
        """Updates which action was taken and the result of that action from the current State."""
        tempMatrix = createMatrix(self.info)

        self.actionTicker[choice] += 1
        index = determineDestination(choice, tempMatrix)
        inc = self.destinationTicker.item((choice, index))
        self.destinationTicker.itemset((choice, index), inc + 1)

    def updatePMAT(self):
        """Updates the probability matrix of the current state with the new probabilities based on tracking info."""
        if self.terminal == 1:
            return np.zeros((HYPER.NUM_ACTIONS, HYPER.NUM_STATES))
        else:
            mat = np.zeros((HYPER.NUM_ACTIONS, HYPER.NUM_STATES))
            for x in range(0, HYPER.NUM_ACTIONS):
                for y in range(0, HYPER.NUM_STATES):
                    mat.itemset((x,y), (self.destinationTicker.item((x,y)) / float(self.actionTicker[x])))
            return(mat)


    def encodePolicy(self, input):
        """Encodes the given choice into a directional string."""
        if(input == 0):
            return "Up"
        if(input == 1):
            return "Left"
        if(input == 2):
            return "Down"
        if(input == 3):
            return "Right"
        else:
            return "None"
# -----------------------------------------------------------------------------

def createMatrix(filename):
        """Creates a matrix from the states information file stored in State.info"""
        with open('data/' + str(filename)) as state_file:
            # lines = state_file.readlines()
            lines = state_file.read().splitlines()
            temp = lines[0].split(" ")
            actions, states = int(temp[0]), int(temp[1])
            matrix = np.zeros((actions, states))
            indexCounter = 0

            for x in range(1, len(lines)):
                temp = lines[x].split(" ")

                for val in temp:
                    matrix.itemset((indexCounter), float(val))
                    indexCounter = indexCounter + 1
        state_file.close()
        return(matrix)


def determineDestination(choice, matrix):
    """Chooses a random destination based on the available choices of that state."""
    return(np.random.choice(np.arange(0, HYPER.NUM_STATES), p = matrix[choice]))