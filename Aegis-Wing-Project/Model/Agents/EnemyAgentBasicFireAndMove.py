import random

from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class EnemyAgentBasicFireAndMove(AgentSuperClass):
    """
    This agent can move left, down, up, or fire
    """
    def __init__(self, lowest_row, least_col):
        super().__init__(1, 1, lowest_row, least_col)

    def get_all_possible_raw_actions(self) -> list:
        return [Actions.LEFT, Actions.DOWN, Actions.UP, Actions.FIRE, Actions.STOP]

    def isPlayer(self):
        return False

    def deepcopy(self):
        copy = EnemyAgentBasicFireAndMove(self.lowest_row, self.least_col)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        return copy

    def autoPickAction(self, state=None) -> Actions:
        """
        Picks one of potentially many pre-defined actions randomly
        in a uniform distribution.
        :return:
        """
        return random.choice(self.get_all_possible_raw_actions())

    def getPointValue(self) -> int:
        return 25

    def __str__(self):
        return f"BasicFireAndMove at col/x = {self.get_position()[1]}\t row/y = {self.get_position()[0]}"

    def getAgentType(self) -> int:
        return 3