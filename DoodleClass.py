import pygame

class Doodle(pygame.sprite.Sprite):
    image_r = pygame.transform.scale(pygame.image.load("sprites/right_jump.png"), (60, 60))
    image_l = pygame.transform.scale(pygame.image.load("sprites/left_jump.png"), (60, 60))

    def __init__(self, all_sprites, x, y):
        super().__init__(all_sprites)
        self.jump = False
        self.y_change = 0
        self.image = Doodle.image_r
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y

    def check_collision(self, platform):
        collision = pygame.sprite.spritecollide(self, platform, False)
        if (collision and self.y_change > 0) or (collision and self.y_change < 0 and collision[0].rect.y - self.rect.y >= 59):
            return True
        else:
            return False

    def update(self, platform, x_change, pos):
        jump_h = 10
        g = 0.5
        if pos < 0:
            self.image = Doodle.image_l
        else:
            self.image = Doodle.image_r
        if self.jump:
            self.y_change = -jump_h
            self.jump = False
        self.rect.y += self.y_change
        self.y_change += g
        self.jump = self.check_collision(platform)
        self.rect.x += x_change
        self.rect.x %= 400
        return self.y_change
