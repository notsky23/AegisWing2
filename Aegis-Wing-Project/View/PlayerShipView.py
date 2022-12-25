import pygame

from View.PlayerBulletView import PlayerBulletView


class PlayerShipView(pygame.sprite.Sprite):
    def __init__(self, playerAgent, view, x, y, maxX, maxY):
        pygame.sprite.Sprite.__init__(self)
        self.playerAgent = playerAgent
        self.view = view
        playerSpriteSheet = pygame.image.load("../Assets/double_ship.png")
        playerSpriteScaled = pygame.transform.scale(playerSpriteSheet, (100, 50))
        self.image1 = playerSpriteScaled.subsurface(0, 0, 50, 50)
        self.image2 = playerSpriteScaled.subsurface(50, 0, 50, 50)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.maxX = maxX
        self.maxY = maxY
        # self.sound = thrusterSound
        self.thrusters_off()
        self.lastShot = pygame.time.get_ticks()
        self.lastMove = pygame.time.get_ticks()


    def thrusters_off(self):
        self.image = self.image1
        # self.sound.stop()

    def thrusters_on(self):
        self.image = self.image2
        # if not soundMixer.get_busy():
        #    self.sound.play(-1)

    def update(self):
        # pass
        # set movement speed
        speed = 50
        cooldown = 100 #milliseconds
        timeNow = pygame.time.get_ticks()

        #get key press
        key = pygame.key.get_pressed()
        #movement of ship
        if (key[pygame.K_UP] or key[pygame.K_w])\
                and (self.rect.top > 0)\
                and (timeNow - self.lastMove > cooldown):
            self.thrusters_on()
            self.rect.y -= speed
            self.lastMove = timeNow

            # self.player_action = Actions.UP
            # self.state = self.state.generateSuccessorState(0, self.player_action)

            # print(self.playerAgent.getX(), self.playerAgent.getY())
            # print(self.state.current_agents[0])

        if (key[pygame.K_DOWN] or key[pygame.K_s])\
                and (self.rect.bottom < self.maxY)\
                and (timeNow - self.lastMove > cooldown):
            self.thrusters_on()
            self.rect.y += speed
            self.lastMove = timeNow
        if (key[pygame.K_LEFT] or key[pygame.K_a])\
                and (self.rect.left > 0)\
                and (timeNow - self.lastMove > cooldown):
            self.thrusters_on()
            self.rect.x -= speed
            self.lastMove = timeNow
        if (key[pygame.K_RIGHT] or key[pygame.K_d])\
                and (self.rect.right < self.maxX)\
                and (timeNow - self.lastMove > cooldown):
            self.thrusters_on()
            self.rect.x += speed
            self.lastMove = timeNow

        if key[pygame.K_SPACE] and (timeNow - self.lastShot > cooldown):
            # bullet = PlayerBulletView(self.rect.right, self.rect.centery)
            # bulletGroup.add(bullet)
            self.view.setupPlayerBullets(self.view, self.rect.right, self.rect.centery)
            self.lastShot = timeNow

        if not any(key):
            self.thrusters_off()
        #
        # # collision
        # if pygame.sprite.spritecollide(self, enemySmallGroup, True, pygame.sprite.collide_mask):
        #     self.kill()
        #     explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 1)
        #     explosionGroup.add(explosion)
        # elif pygame.sprite.spritecollide(self, enemyMediumGroup, True, pygame.sprite.collide_mask):
        #     self.kill()
        #     explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 2)
        #     explosionGroup.add(explosion)
        # elif pygame.sprite.spritecollide(self, enemyBigGroup, True, pygame.sprite.collide_mask):
        #     self.kill()
        #     explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 3)
        #     explosionGroup.add(explosion)