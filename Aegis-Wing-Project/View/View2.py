#turtle screen set up
import random
import turtle as turtle_module

import pygame

from Model.Agents.AgentInterface import AgentInterface
from View.PlayerBulletView import PlayerBulletView
from View.PlayerShipView import PlayerShipView
from View.EnemyShipSmallView import EnemyShipSmallView


class View2:
    def __init__(self):
        #self.window = turtle_module.Screen()
        self.lowest_x_cord_value = None
        self.max_x_cord_value = None
        self.lowest_y_cord_value = None
        self.max_y_cord_value = None

        self.turtle_ships = []
        self.turtle_dict = {}

        # create sprite groups
        self.spaceshipGroup = pygame.sprite.Group()
        self.bulletGroup = pygame.sprite.Group()
        self.enemySmallGroup = pygame.sprite.Group()

        """
        Define FPS
        """
        self.clock = pygame.time.Clock()
        self.fps = 60


    def set_coord_values(self, gameModel, min_x: int, max_x: int, min_y: int, max_y: int):
        self.model = gameModel
        self.lowest_x_cord_value = min_x
        self.max_x_cord_value = (max_x + 1) * 50
        self.lowest_y_cord_value = min_y
        self.maxY = max_y
        self.max_y_cord_value = (max_y + 1) * 50

        """
        Load images image
        """
        # background nebula
        self.nebula = pygame.image.load("../Assets/nebula_brown.png")
        self.nebula = pygame.transform.scale(self.nebula, (self.max_x_cord_value, self.max_y_cord_value))

        # background debris
        self.debris = pygame.image.load("../Assets/debris2_brown.png")
        self.debris = pygame.transform.scale(self.debris, (self.max_x_cord_value, self.max_y_cord_value))

        # object images
        # bulletSprite = pygame.image.load("../Assets/shot2.png")
        # enemySheetMedium = pygame.image.load("../Assets/enemyMedium.png")
        # enemyMediumScaled = pygame.transform.scale(enemySheetMedium, (300, 100))
        # enemySheetBig = pygame.image.load("../Assets/enemyBig.png")
        # enemyBigScaled = pygame.transform.scale(enemySheetBig, (840, 200))
        # explosionSpriteSheet = pygame.image.load("../Assets/explosion_alpha.png")

        # set screen
        self.screen = pygame.display.set_mode((self.max_x_cord_value, self.max_y_cord_value))
        pygame.display.set_caption('Aegis Wing')

        # create small enemies
        # enemySmall1 = EnemyShipSmallView(25 + 450, 25 + 50, 0)
        # self.enemySmallGroup.add(enemySmall1)


    # Setup PlayerShip
    def setupPlayerShip(self, playerAgent, view):
        x = (playerAgent.getX() * 50) + 25
        # x = (x * 50) + 25
        # y = abs((y - self.maxY) * 50) + 25
        y = abs(((playerAgent.getY() - self.maxY) * 50) + 25)
        playerShip = PlayerShipView(playerAgent, view, x, y, self.max_x_cord_value, self.max_y_cord_value)
        self.spaceshipGroup.add(playerShip)

    # Setup enemy ships - small
    def setupEnemyShipSmall(self, x, y):
        x = (x * 50) + 25
        y = abs((y - self.maxY) * 50) + 25
        enemyShip = EnemyShipSmallView(x, y, random.randint(0, 4))
        self.enemySmallGroup.add(enemyShip)

    # Setup enemy ships - small
    def setupPlayerBullets(self, view, x, y):
        playerBullet = PlayerBulletView(view, x, y, self.max_x_cord_value, self.max_y_cord_value)
        self.enemySmallGroup.add(playerBullet)

    def getView(self):
        return self


    def main(self):
        time = 0
        run = True

        while run:
            # frame rate
            self.clock.tick(self.fps)

            # draw and animate background
            time += 1
            wtime = (time / 4) % self.max_x_cord_value
            self.screen.blit(self.nebula, (0, 0))
            self.screen.blit(self.debris, (0 - wtime, 0))
            self.screen.blit(self.debris, (self.max_x_cord_value - wtime, 0))

            # event handlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # update spaceship
            self.spaceshipGroup.update()

            # # update
            # bulletGroup.update()
            self.enemySmallGroup.update()
            # enemyMediumGroup.update()
            # enemyBigGroup.update()
            # explosionGroup.update()

            # draw sprite groups
            self.spaceshipGroup.draw(self.screen)
            # bulletGroup.draw(screen)
            self.enemySmallGroup.draw(self.screen)
            # enemyMediumGroup.draw(screen)
            # enemyBigGroup.draw(screen)
            # explosionGroup.draw(screen)

            # update display
            pygame.display.update()

        pygame.quit()

    # def produce_turtle(self,x_pos, y_pos, isPlayer: bool = False):
    #     turtle_color = "black"
    #     if isPlayer == False:
    #         turtle_color = "red"
    #
    #     t = turtle_module.Turtle()
    #     t.hideturtle()
    #     t.shape("square")
    #     t.color(turtle_color)
    #     t.penup()
    #     t.shapesize(2,3,1)
    #     t.speed(0)
    #     t.setpos(x_pos,y_pos)
    #     t.showturtle()
    #
    #
    # def set_up_turtles(self, list_agents):
    #     #clears registry as well so clears onkey press
    #     self.window.clear() # delete all turtles, maybe add a delay for movement?
    #
    #     #for turtle in self.window.turtles():
    #         #turtle.reset()
    #
    #     self.turtle_ships = []
    #
    #     for i in range(len(list_agents)):
    #         each_enemy : AgentInterface = list_agents[i]
    #
    #         # if enemy turtle larger size than 1
    #         x_low, x_high = each_enemy.get_col_boundaries()
    #         y_low, y_high = each_enemy.get_row_boundaries()
    #
    #         x_range = x_high - x_low
    #         y_range = y_high - y_low
    #
    #         if each_enemy.isPlayer() == True:
    #             is_player_turtle = True
    #         else:
    #             is_player_turtle = False
    #
    #         # if length enemy > 1
    #         if x_range > 0:
    #             # make individual turtles to represent all segments
    #             #of current ship on that row
    #             # high + 1 because for loop is exclusive of last value
    #             for x_range_value in range(x_low, x_high + 1):
    #                 #more than 1 row tall
    #                 if y_range > 0:
    #                     for y_range_value in range(y_low, y_high + 1):
    #                         enemy_turtle = self.produce_turtle(x_range_value, y_range_value, is_player_turtle)
    #                         self.turtle_ships.append(enemy_turtle)
    #                 else:
    #                     enemy_turtle = self.produce_turtle(x_range_value, y_low, is_player_turtle)
    #                     self.turtle_ships.append(enemy_turtle)
    #         else:
    #             # if enemy only 1 unit long
    #             if y_range > 0:
    #                 for y_range_value in range(y_low, y_high + 1):
    #                     enemy_turtle = self.produce_turtle(x_low, y_range_value, is_player_turtle)
    #                     self.turtle_ships.append(enemy_turtle)
    #             else:
    #                 enemy_turtle = self.produce_turtle(x_low,y_low, is_player_turtle)
    #                 self.turtle_ships.append(enemy_turtle)