import pygame


class EnemyShipSmallView(pygame.sprite.Sprite):
    def __init__(self, x, y, frame):
        pygame.sprite.Sprite.__init__(self)
        enemySheetSmall = pygame.image.load("../Assets/enemySmall.png")
        enemySmallScaled = pygame.transform.scale(enemySheetSmall, (250, 50))
        image1 = enemySmallScaled.subsurface((frame * 50), 0, 50, 50)
        self.image = pygame.transform.rotate(image1, 90)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        #update mask
        self.mask = pygame.mask.from_surface(self.image)