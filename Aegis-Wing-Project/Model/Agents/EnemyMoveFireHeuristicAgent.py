import random

from Model.GameState import GameState
from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass


class EnemyMoveFireHeuristicAgent(AgentSuperClass):
    """
    This agent can move left, down, up, or fire
    """

    def __init__(self, lowest_row, least_col, count: int = 10):
        super().__init__(1, 1, lowest_row, least_col)
        self.counter = count

    def get_all_possible_raw_actions(self) -> list:

        allactions = [Actions.LEFT, Actions.DOWN, Actions.UP, Actions.RIGHT,
                      Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN, Actions.FIRELEFT,
                      Actions.FIRERIGHT]
        return allactions

    def isPlayer(self):
        return False

    def deepcopy(self):
        copy = EnemyMoveFireHeuristicAgent(self.lowest_row, self.least_col, count=self.counter)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        return copy

    def autoPickAction(self, state: GameState = None) -> Actions:
        """
        Picks one of potentially many pre-defined actions randomly
        in a uniform distribution.
        :return:
        """
        if self.counter is not None and self.counter <= 0:
            return Actions.FIRELEFT

        agent_copy = self.deepcopy()
        list_enemy_agents = state.current_agents[1:]

        list_enemy_agents.remove(self)

        # extract player agent position from state
        if state is None:
            raise ValueError("GameState cannot be None for Heuristic Agent")
        player_y, player_x = state.getPlayerPos()
        playerAgent = state.getPlayer()
        ideal_pos = player_x + 2

        if self.is_same_height_agent(playerAgent):
            if ideal_pos > self.least_col > player_x - 4:
                allActions = [Actions.FIREDOWN, Actions.FIREUP]
            elif self.least_col < ideal_pos:
                agent_copy.performAction(Actions.RIGHT)
                overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
                agent_copy.performAction(Actions.LEFT)
                if overlaps:
                    allActions = [Actions.FIRERIGHT, Actions.FIREUP, Actions.FIREDOWN]
                else:
                    allActions = [Actions.FIRERIGHT]
            elif self.least_col > ideal_pos:
                agent_copy.performAction(Actions.LEFT)
                overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
                agent_copy.performAction(Actions.RIGHT)
                if overlaps:
                    allActions = [Actions.FIRERIGHT, Actions.FIRELEFT, Actions.FIRE, Actions.FIREUP, Actions.FIREDOWN]
                else:
                    allActions = [Actions.FIRELEFT]
            else:
                allActions = [Actions.FIRE, Actions.FIRERIGHT]

        if self.lowest_row > player_y:
            if ideal_pos > self.least_col > player_x - 4:
                return Actions.FIRERIGHT
            agent_copy.performAction(Actions.DOWN)
            overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
            agent_copy.performAction(Actions.UP)
            if overlaps:
                allActions = [Actions.FIREDOWN, Actions.FIRERIGHT, Actions.FIRE]
            else:
                allActions = [Actions.FIREDOWN]
        elif self.lowest_row < player_y:
            if ideal_pos > self.least_col > player_x - 4:
                return Actions.FIRERIGHT
            agent_copy.performAction(Actions.UP)
            overlaps = any([self.is_overlapping_other_agent(other) for other in list_enemy_agents])
            agent_copy.performAction(Actions.DOWN)
            if overlaps:
                allActions = [Actions.FIREUP, Actions.FIRERIGHT, Actions.FIRE]
            else:
                allActions = [Actions.FIREUP]

        return random.choice(allActions)

    def isHeuristicAgent(self) -> bool:
        '''
        Returns True if agent requires player as a variable
        :return: {bool} Returns True if player variable requires updating, otherwise false
        '''
        return True

    def take_action(self, action: Actions):
        if action in self.get_all_possible_raw_actions():
            agent_copy = self.deepcopy()
            if agent_copy.counter is not None and agent_copy.counter > 0:
                agent_copy.counter -= 1
            agent_copy.performAction(action)
            agent_copy.hasAlreadyMoved = True
            return agent_copy
        else:
            return self

    def getPointValue(self) -> int:
        return 50

    def getCount(self) -> int:
        return self.counter

    def __str__(self):
        return f"HeuristicMoveFire at col/x = {self.get_position()[1]}\t row/y = {self.get_position()[0]},\t count: {self.counter}"

    def isCounterAgent(self) -> bool:
        if self.counter is not None:
            return True
        else:
            return False

    def getAgentType(self) -> int:
        return 4
