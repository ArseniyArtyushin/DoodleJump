import pygame
from random import randint, choice

from CheckRecord import Record


class Platform(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("sprites/platform.png"), (70, 20))
    score = Record().read_score()

    def __init__(self, all_sprites, x, y):
        self.platform_sprites = all_sprites
        super().__init__(self.platform_sprites)
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y

    def update(self, x, y, y_change):
        if y < 250 and y_change < 0:
            self.rect.y -= y_change
            Platform.score += 0.2
        if self.rect.y > 600:
            self.kill()
            Platform(self.platform_sprites, randint(10, 320), randint(-50, -10))
#         choice([randint(0, x) + 10, randint(x, 400) - 80])
