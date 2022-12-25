import uuid

from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class PlayerAgent(AgentSuperClass):
    def __init__(self, agent_length: int = 1, agent_height: int = 1, lowest_row: int = 0, least_col: int = 0):
        super().__init__(agent_length, agent_height, lowest_row, least_col)
        self.isInvulnerable = False
        self.turnsUntilInvulnerabilityOver = 0
        self.spawn_x = least_col
        self.spawn_y = lowest_row
        self.id = "1"

    def get_all_possible_raw_actions(self) -> list:
        """
        The player agent should be able to perform all actions
        :return: {list(Action)}
        """
        return [Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE]

    def isPlayer(self) -> bool:
        """
        Since this is a player agent it should return True
        :return: {bool} true
        """
        return True

    def deepcopy(self):
        """
        Need this to be shallow copy??. This is a helper method
        to takeAction method.
        :return:
        """
        copy = PlayerAgent(self.agent_length,self.agent_height,self.lowest_row, self.least_col)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.hp = self.get_hp()
        return copy


    #TODO test this method if necessary, use when player dies and has another life left
    def respawnPlayer(self):
        #TODO would be an issue if game has more than 1 player life beacuse health not copied over
        respawned =  PlayerAgent(self.agent_length,self.agent_height,self.spawn_y, self.spawn_x)
        return respawned


    def getId(self):
        return self.id

    def getX(self):
        return self.spawn_x

    def getY(self):
        return self.spawn_y

    def getPointValue(self) -> int:
        return -100

    def getAgentType(self) -> int:
        return 1
    def __str__(self):
        return f"PlayerAgent at col/x = {self.get_position()[1]}\t row/y = {self.get_position()[0]}"