import random

from Model.Agents.AgentInterface import AgentInterface
from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class BasicCounterAgent(AgentSuperClass):
    """
    This agent can move left, down, up, or fire.
    This agent
    """

    def __init__(self, lowest_row, least_col, count: int, ideal_x: int, ideal_y: int):
        super().__init__(1, 1, lowest_row, least_col)
        self.counter = count
        self.ideal_x = ideal_x
        self.ideal_y = ideal_y
        self.atIdealPos = False

    def get_all_possible_raw_actions(self) -> list:

        allactions = [Actions.LEFT, Actions.DOWN, Actions.UP, Actions.RIGHT,
                      Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN, Actions.FIRELEFT,
                      Actions.FIRERIGHT]
        return allactions

    def isPlayer(self):
        return False

    def isBasicCounter(self) -> bool:
        return True


    def deepcopy(self):
        copy = BasicCounterAgent(self.lowest_row, self.least_col, self.counter, self.ideal_x, self.ideal_y)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        return copy

    def autoPickAction(self, state: GameState = None) -> Actions:
        """
        If the agent is in the proper position then it stays and fires.
        If not it moves towards that position and increments the counter
            to keep it alive until it reaches position.
        Once the counter is finished it moves left off the screen.
        :return:
        """

        if self.counter <= 0:
            return Actions.LEFT

        if self.ideal_y == self.lowest_row and self.ideal_x == self.least_col:
            self.counter -= 1
            return Actions.FIRE

        elif self.ideal_y == self.lowest_row:

            if self.least_col < self.ideal_x:
                return Actions.RIGHT

            elif self.least_col > self.ideal_x:
                return Actions.LEFT
        else:
            if self.lowest_row < self.ideal_y:
                return Actions.UP

            elif self.lowest_row > self.ideal_y:
                return Actions.DOWN

    def getCount(self) -> int:
        return self.counter

    # TODO, Hi Dan, this is from Ramzi, I had to add these to make spawning them work
    @staticmethod
    def convert_agentInterface_to_BasicCounter(agent: AgentInterface):
        return BasicCounterAgent(agent.get_position()[0], agent.get_position()[1],agent.getCount(), 0, 0)

    def set_ideal_row(self, ideal_row: int) -> None:
        self.ideal_y = ideal_row

    def set_ideal_col(self, ideal_col: int) -> None:
        self.ideal_x = ideal_col

    def getPointValue(self) -> int:
        return 20

    def __str__(self):
        return f"BasicCounterAgent at col/x = {self.get_position()[1]}\t row/y = {self.get_position()[0]},\t count: {self.counter}"

    def isCounterAgent(self) -> bool:
        return True

    def getAgentType(self) -> int:
        return 5
