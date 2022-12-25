import unittest
import pygame

from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameBoard import GameBoard
from View import View


class TestGameBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.board = GameBoard(16, 12) #10 columns, 8 rows
        self.playerShip = PlayerAgent()

    def testView(self):
        # set variables
        screenWidth = (self.board.getBoardBoundaries()[1] + 1) * 50
        screenHeight = (self.board.getBoardBoundaries()[3] + 1) * 50

        screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption('Aegis Wing')

        """
        Load images image
        """
        # # background nebula
        # nebula = pygame.image.load("../Assets/nebula_brown.png")
        # nebula = pygame.transform.scale(nebula, (screenWidth, screenHeight))
        #
        # # background debris
        # debris = pygame.image.load("../Assets/debris2_brown.png")
        # debris = pygame.transform.scale(debris, (screenWidth, screenHeight))
        #
        # # object images
        playerSpriteSheet = pygame.image.load("../Assets/double_ship.png")
        playerSpriteScaled = pygame.transform.scale(playerSpriteSheet, (100, 50))
        # bulletSprite = pygame.image.load("../Assets/shot2.png")
        # enemySheetSmall = pygame.image.load("../Assets/enemySmall.png")
        # enemySmallScaled = pygame.transform.scale(enemySheetSmall, (300, 50))
        # enemySheetMedium = pygame.image.load("../Assets/enemyMedium.png")
        # enemyMediumScaled = pygame.transform.scale(enemySheetMedium, (300, 100))
        # enemySheetBig = pygame.image.load("../Assets/enemyBig.png")
        # enemyBigScaled = pygame.transform.scale(enemySheetBig, (820, 200))
        # explosionSpriteSheet = pygame.image.load("../Assets/explosion_alpha.png")

        # Sounds
        # soundMixer = pygame.mixer
        # soundMixer.init()
        # thrusterSound = soundMixer.Sound("../Assets/thrust.mp3")

        # create sprite group
        spaceshipGroup = pygame.sprite.Group()
        # bulletGroup = pygame.sprite.Group()
        # enemySmallGroup = pygame.sprite.Group()
        # enemyMediumGroup = pygame.sprite.Group()
        # enemyBigGroup = pygame.sprite.Group()
        # explosionGroup = pygame.sprite.Group()

        # create player
        playerShip = View.Spaceship(playerSpriteScaled, 25, 25)
        spaceshipGroup.add(playerShip)

        # # small enemies
        # enemySmall1 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 50, 0)
        # enemySmall2 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 0, 1)
        # enemySmall3 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 100, 2)
        # enemySmall4 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 150, 3)
        # enemySmall5 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 200, 4)
        # enemySmallGroup.add(enemySmall1)
        # enemySmallGroup.add(enemySmall2)
        # enemySmallGroup.add(enemySmall3)
        # enemySmallGroup.add(enemySmall4)
        # enemySmallGroup.add(enemySmall5)
        #
        # # medium enemies
        # enemyMedium1 = EnemyMedium(enemyMediumScaled, 50 + 500, 50, 0)
        # enemyMedium2 = EnemyMedium(enemyMediumScaled, 50 + 500, 150, 1)
        # enemyMedium3 = EnemyMedium(enemyMediumScaled, 50 + 500, 250, 2)
        # enemyMediumGroup.add(enemyMedium1)
        # enemyMediumGroup.add(enemyMedium2)
        # enemyMediumGroup.add(enemyMedium3)
        #
        # # big enemies
        # enemyBig1 = EnemyBig(enemyBigScaled, 100 + 600, 100, 0)
        # enemyBig2 = EnemyBig(enemyBigScaled, 100 + 600, 100 + 200, 1)
        # enemyBig3 = EnemyBig(enemyBigScaled, 100 + 600, 100 + 400, 3)
        # enemyBig4 = EnemyBig(enemyBigScaled, 100 + 400, 100 + 400, 2)
        # enemyBigGroup.add(enemyBig1)
        # enemyBigGroup.add(enemyBig2)
        # enemyBigGroup.add(enemyBig3)
        # enemyBigGroup.add(enemyBig4)
        #
        # # explosion
        # # explosion = Explosion(explosionSpriteSheet, 200, 200, 3)
        # # explosionGroup.add(explosion)

        # View.main(screenWidth, screenHeight, screen, playerShip)