import time

import pygame

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameModel import GameModel
from SimpleTurtleView import SimpleTurtleView
from View import View2


class Controller:
    def __init__(self, view: View2, gameModel: GameModel):
        self.view = view
        self.model = gameModel
        self.model.gameState.turns_left = 100
        min_x, max_x, min_y, max_y = self.model.gameState.gameBoard.getBoardBoundaries()
        self.view.set_coord_values(self.model, min_x, max_x, min_y, max_y)

        enemy_1 = SimpleGoLeftAgent(6, 7)
        enemy_2 = SimpleGoLeftAgent(6, 6)
        enemy_3 = SimpleGoLeftAgent(5, 5)

        self.model.gameState.addAgent(enemy_1)
        self.model.gameState.addAgent(enemy_2)
        self.model.gameState.addAgent(enemy_3)

        # self.player_action = Actions.STOP
        self.state = self.model.gameState

        self.playerAgent = self.state.current_agents[0]
        self.enemyAgents = self.state.current_agents[1:]

        self.view.setupPlayerShip(self.playerAgent, self.view)

        for each in self.enemyAgents:
            self.view.setupEnemyShipSmall(each.getX(), each.getY())

        print(self.model.gameState.current_agents)
        print(self.playerAgent.getX(), self.playerAgent.getY())


    def go(self):

        screen = self.view.screen

        # self.re_register_actions()

        self.view.main()