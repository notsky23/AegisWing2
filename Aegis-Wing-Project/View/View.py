import pygame
import os
from pygame.locals import *


# Ship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = spriteSheet.subsurface(0, 0, 50, 50)
        self.image2 = spriteSheet.subsurface(50, 0, 50, 50)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
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
        #set movement speed
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
        if (key[pygame.K_DOWN] or key[pygame.K_s])\
                and (self.rect.bottom < screenHeight)\
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
                and (self.rect.right < screenWidth)\
                and (timeNow - self.lastMove > cooldown):
            self.thrusters_on()
            self.rect.x += speed
            self.lastMove = timeNow

        if key[pygame.K_SPACE] and (timeNow - self.lastShot > cooldown):
            bullet = Bullets(self.rect.right, self.rect.centery)
            bulletGroup.add(bullet)
            self.lastShot = timeNow

        if not any(key):
            self.thrusters_off()

        # collision
        if pygame.sprite.spritecollide(self, enemySmallGroup, True, pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 1)
            explosionGroup.add(explosion)
        elif pygame.sprite.spritecollide(self, enemyMediumGroup, True, pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 2)
            explosionGroup.add(explosion)
        elif pygame.sprite.spritecollide(self, enemyBigGroup, True, pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 3)
            explosionGroup.add(explosion)


# Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletSprite
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x += 10
        if self.rect.left > screenWidth:
            self.kill()

        #collision
        if pygame.sprite.spritecollide(self, enemySmallGroup, True, pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 1)
            explosionGroup.add(explosion)
        elif pygame.sprite.spritecollide(self, enemyMediumGroup, True, pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 2)
            explosionGroup.add(explosion)
        elif pygame.sprite.spritecollide(self, enemyBigGroup, True, pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 3)
            explosionGroup.add(explosion)


class EnemySmall(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, x, y, frame):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = spriteSheet.subsurface((frame * 50), 0, 50, 50)
        self.image = pygame.transform.rotate(self.image1, 90)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        #update mask
        self.mask = pygame.mask.from_surface(self.image)


class EnemyMedium(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, x, y, frame):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = spriteSheet.subsurface((frame * 100), 0, 100, 100)
        self.image = pygame.transform.rotate(self.image1, 90)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # update mask
        self.mask = pygame.mask.from_surface(self.image)


class EnemyBig(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, x, y, frame):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = spriteSheet.subsurface((frame * 200) + (frame * 10), 0, 200, 200)
        self.image = pygame.transform.rotate(self.image1, 90)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # update mask
        self.mask = pygame.mask.from_surface(self.image)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        # img = img.subsurface((10 * 200), 0, 200, 200)
        # self.images.append(img)

        for frame in range(0, 24):
            if size == 1:
                img = pygame.transform.scale(spriteSheet, (1200, 50))
                img = img.subsurface((frame * 50), 0, 50, 50)
            elif size == 2:
                img = pygame.transform.scale(spriteSheet, (2400, 100))
                img = img.subsurface((frame * 100), 0, 100, 100)
            elif size == 3:
                img = pygame.transform.scale(spriteSheet, (4800, 200))
                img = img.subsurface((frame * 200), 0, 200, 200)
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        if self.index < len(self.images) - 1:
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1:
            self.kill()



"""
The game event loop
"""
def main():
    time = 0
    run = True

    while run:
        #frame rate
        clock.tick(fps)

        #draw and animate background
        time += 1
        wtime = (time / 4) % screenWidth
        screen.blit(nebula, (0, 0))
        screen.blit(debris, (0 - wtime, 0))
        screen.blit(debris, (600 - wtime, 0))

        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #update spaceship
        spaceshipGroup.update()

        #update sprites
        bulletGroup.update()
        enemySmallGroup.update()
        enemyMediumGroup.update()
        enemyBigGroup.update()
        explosionGroup.update()

        #draw sprite groups
        spaceshipGroup.draw(screen)
        bulletGroup.draw(screen)
        enemySmallGroup.draw(screen)
        enemyMediumGroup.draw(screen)
        enemyBigGroup.draw(screen)
        explosionGroup.draw(screen)

        #update display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    """
    Set variables
    """
    screenWidth = 800
    screenHeight = 600

    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('Aegis Wing')

    """
    Define FPS
    """
    clock = pygame.time.Clock()
    fps = 60

    """
    Load images image
    """
    # background nebula
    nebula = pygame.image.load("../Assets/nebula_brown.png")
    nebula = pygame.transform.scale(nebula, (screenWidth, screenHeight))

    # background debris
    debris = pygame.image.load("../Assets/debris2_brown.png")
    debris = pygame.transform.scale(debris, (screenWidth, screenHeight))

    # object images
    playerSpriteSheet = pygame.image.load("../Assets/double_ship.png")
    playerSpriteScaled = pygame.transform.scale(playerSpriteSheet, (100, 50))
    bulletSprite = pygame.image.load("../Assets/shot2.png")
    enemySheetSmall = pygame.image.load("../Assets/enemySmall.png")
    enemySmallScaled = pygame.transform.scale(enemySheetSmall, (250, 50))
    enemySheetMedium = pygame.image.load("../Assets/enemyMedium.png")
    enemyMediumScaled = pygame.transform.scale(enemySheetMedium, (300, 100))
    enemySheetBig = pygame.image.load("../Assets/enemyBig.png")
    enemyBigScaled = pygame.transform.scale(enemySheetBig, (840, 200))
    explosionSpriteSheet = pygame.image.load("../Assets/explosion_alpha.png")

    # Sounds
    # soundMixer = pygame.mixer
    # soundMixer.init()
    # thrusterSound = soundMixer.Sound("../Assets/thrust.mp3")

    # create sprite group
    spaceshipGroup = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group()
    enemySmallGroup = pygame.sprite.Group()
    enemyMediumGroup = pygame.sprite.Group()
    enemyBigGroup = pygame.sprite.Group()
    explosionGroup = pygame.sprite.Group()

    # create player
    playerShip = Spaceship(playerSpriteScaled, 25, 25)
    spaceshipGroup.add(playerShip)

    # small enemies
    enemySmall1 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 50, 0)
    enemySmall2 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 0, 1)
    enemySmall3 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 100, 2)
    enemySmall4 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 150, 3)
    enemySmall5 = EnemySmall(enemySmallScaled, 25 + 450, 25 + 200, 4)
    enemySmallGroup.add(enemySmall1)
    enemySmallGroup.add(enemySmall2)
    enemySmallGroup.add(enemySmall3)
    enemySmallGroup.add(enemySmall4)
    enemySmallGroup.add(enemySmall5)

    # medium enemies
    enemyMedium1 = EnemyMedium(enemyMediumScaled, 50 + 500, 50, 0)
    enemyMedium2 = EnemyMedium(enemyMediumScaled, 50 + 500, 150, 1)
    enemyMedium3 = EnemyMedium(enemyMediumScaled, 50 + 500, 250, 2)
    enemyMediumGroup.add(enemyMedium1)
    enemyMediumGroup.add(enemyMedium2)
    enemyMediumGroup.add(enemyMedium3)

    # big enemies
    enemyBig1 = EnemyBig(enemyBigScaled, 100 + 600, 100, 0)
    enemyBig2 = EnemyBig(enemyBigScaled, 100 + 600, 100 + 200, 1)
    enemyBig3 = EnemyBig(enemyBigScaled, 100 + 600, 100 + 400, 3)
    enemyBig4 = EnemyBig(enemyBigScaled, 100 + 400, 100 + 400, 2)
    enemyBigGroup.add(enemyBig1)
    enemyBigGroup.add(enemyBig2)
    enemyBigGroup.add(enemyBig3)
    enemyBigGroup.add(enemyBig4)

    # explosion
    # explosion = Explosion(explosionSpriteSheet, 200, 200, 3)
    # explosionGroup.add(explosion)

    main()
