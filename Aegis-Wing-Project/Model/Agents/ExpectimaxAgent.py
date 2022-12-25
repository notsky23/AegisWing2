import uuid
import random
from math import inf

from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class ExpectimaxAgent(AgentSuperClass):
    def __init__(self, lowest_row, least_col):
        super().__init__(1, 1, lowest_row, least_col)
        self.id = uuid.uuid4()

    def get_all_possible_raw_actions(self) -> list:
        allactions = [Actions.LEFT, Actions.DOWN, Actions.UP, Actions.RIGHT,
                      Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN, Actions.FIRELEFT,
                      Actions.FIRERIGHT]
        return allactions

    def isPlayer(self):
        return False

    def deepcopy(self):
        copy = ExpectimaxAgent(self.lowest_row, self.least_col)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.id = self.id
        return copy


    def autoPickAction(self, gameState: GameState = None) -> Actions:
        """
        Picks one of potentially many pre-defined actions randomly
        in a uniform distribution.
        :return:
        """
        """
        Recursion function
        """

        def expectimaxFunction(state, depth, agent):
            """
            get depth
            if it cycles back to player move down the tree
            """
            print("AGENT", agent)
            if (agent == 0):
                nextDepth = depth - 1
            else:
                nextDepth = depth

            """
            If state is end of game
            """
            if state is None:
                raise ValueError("GameState cannot be None for Heuristic Agent")

            """
            max = player
            min = ghosts
            """
            if (agent == 0):
                agentType = max
                bestValue = -inf

            else:
                agentType = min
                bestValue = inf
            # print("BEST OF", bestOf)
            # print("BEST VAL", bestVal)

            """
            modulo to keep reverting back and forth between pacman and ghosts
            """
            nextAgent = (agent + 1) % state.getNumAgents()

            """
            legal actions list available for an agent
            """
            legalActionsList = state.getLegalActions(agent)

            """
            If agents are not pacman
            """
            if (agent != 0):
                """
                Probability = branches of the node of possible agent moves
                """
                probability = 1.0 / len(legalActionsList)
                averageValue = 0

                """
                Loop - get all successor states and legal actions for ghosts
                """
                for legalAction in legalActionsList:
                    successorState = state.generateSuccessor(agent, legalAction)
                    nodeValue, direction = expectimaxFunction(successorState, nextDepth, nextAgent)
                    """
                    calculate for the average of all available nodes
                    """
                    averageValue += probability * nodeValue

                # print(agent, averageValue, legalAction)
                return averageValue, legalAction

            """
            Loop - get all successor states and legal actions for pacman
            """
            for legalAction in legalActionsList:
                successorState = state.generateSuccessor(agent, legalAction)
                actionValue, direction = expectimaxFunction(successorState, nextDepth, nextAgent)

                # print(actionValue, direction)

                """
                Decide on the best course of action by getting best value
                """
                if (agentType(bestValue, actionValue) == actionValue):
                    bestValue = actionValue
                    bestAction = legalAction
                    # print(agent, bestValue, bestAction)

            # if(agent == 0):
            #     print(agent, bestValue, bestAction)

            return bestValue, bestAction

        value, legalAction = expectimaxFunction(gameState, self.depth + 1, self.index)
        return legalAction

    def isExpectimaxAgent(self) -> bool:
        '''
        Returns True if agent requires player as a variable
        :return: {bool} Returns True if player variable requires updating, otherwise false
        '''
        return True

    def take_action(self, action: Actions):
        if action in self.get_all_possible_raw_actions():
            agent_copy = self.deepcopy()
            agent_copy.performAction(action)
            agent_copy.hasAlreadyMoved = True
            return agent_copy
        else:
            return self
