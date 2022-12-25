import time

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameModel import GameModel
from SimpleTurtleView import SimpleTurtleView

class SimplePlayerController:
    # TODO change viewtype to interface
    def __init__(self, view: SimpleTurtleView, gameModel: GameModel):
        self.view = view
        self.model = gameModel
        self.model.gameState.turns_left = 100
        min_x, max_x, min_y, max_y = self.model.gameState.gameBoard.getBoardBoundaries()
        self.view.set_coord_values(min_x, max_x, min_y, max_y)

        enemy_1 = SimpleGoLeftAgent(6, 7)
        enemy_2 = SimpleGoLeftAgent(6, 6)
        enemy_3 = SimpleGoLeftAgent(5, 5)

        self.model.gameState.addAgent(enemy_1)
        self.model.gameState.addAgent(enemy_2)
        self.model.gameState.addAgent(enemy_3)

        self.player_action = Actions.STOP
        self.state = self.model.gameState

    def move_enemies(self):
        for each_index in range(1, len(self.state.current_agents)):
            try:
                each_agent: AgentInterface = self.state.current_agents[each_index]
            except IndexError:
                # means list was shortened because enemy agent died or exited board
                # 3 cases
                # case 1 agent in middle of list disappeared
                each_agent: AgentInterface = self.state.current_agents[each_index - 1]
                # case agent at end of list died/disappeared
                # no more agents to move
                if each_agent.hasMoved():
                    self.state.decrement_turn()
                    break
                else:
                    each_index -= 1
                # continue otherwise

            agent_action = each_agent.autoPickAction()

            # len of current agents may change here, potentiall causing index error
            self.state = self.state.generateSuccessorState(each_index, agent_action)

        for each_index in range(1, len(self.state.current_agents)):
            each_agent: AgentInterface = self.state.current_agents[each_index]
            print(each_index, ": ", each_agent.get_position())

        self.state.reset_agents_move_status()
        self.view.set_up_turtles(self.state.current_agents)
        self.re_register_actions()

    def re_register_actions(self):
        """
        This is needed because turtle.Screen.clear is called meaning onkey registers
        need to be registered again
        :return:
        """
        self.view.window.onkeypress(self.player_right, "Right")
        self.view.window.onkeypress(self.player_up, "Up")
        self.view.window.onkeypress(self.player_down, "Down")
        self.view.window.onkeypress(self.player_left, "Left")
        self.view.window.listen()



    def player_right(self):
        self.player_action = Actions.RIGHT

        # move player first
        self.state = self.state.generateSuccessorState(0, self.player_action)
        self.move_enemies()


    def player_up(self):
        self.player_action = Actions.UP

        # move player first
        self.state = self.state.generateSuccessorState(0, self.player_action)
        self.move_enemies()
        print(self.state)

    def player_down(self):
        self.player_action = Actions.DOWN

        # move player first
        self.state = self.state.generateSuccessorState(0, self.player_action)
        self.move_enemies()

    def player_left(self):
        self.player_action = Actions.LEFT

        # move player first
        self.state = self.state.generateSuccessorState(0, self.player_action)
        self.move_enemies()


    def go(self):

        screen = self.view.window
        self.re_register_actions()

        screen.mainloop()








    # Main loop must go in the controller
