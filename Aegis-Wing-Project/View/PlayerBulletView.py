# Bullets class
import pygame


class PlayerBulletView(pygame.sprite.Sprite):
    def __init__(self, view, x, y, maxX, maxY):
        pygame.sprite.Sprite.__init__(self)
        self.view = view
        bulletSprite = pygame.image.load("../Assets/shot2.png")
        self.image = bulletSprite
        self.maxX= maxX
        self.maxY = maxY
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x += 10
        if self.rect.left > self.maxX:
            self.kill()

        #collision
        #enemy sprite instead of pygame sprite
        # if pygame.sprite.spritecollide(self, self.view.enemySmallGroup, True, pygame.sprite.collide_mask):
        #     # self.kill()
        #     print("KILL")
            # explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 1)
            # explosionGroup.add(explosion)
        # elif pygame.sprite.spritecollide(self, enemyMediumGroup, True, pygame.sprite.collide_mask):
        #     self.kill()
        #     explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 2)
        #     explosionGroup.add(explosion)
        # elif pygame.sprite.spritecollide(self, enemyBigGroup, True, pygame.sprite.collide_mask):
        #     self.kill()
        #     explosion = Explosion(explosionSpriteSheet, self.rect.centerx, self.rect.centery, 3)
        #     explosionGroup.add(explosion)