import pygame

# Класс персонажа (дудла)
class Doodle(pygame.sprite.Sprite):
    # Подгрузка изображения дудла
    image_r = pygame.transform.scale(pygame.image.load("sprites/doodle.png"), (60, 60))
    image_l = pygame.transform.flip(image_r, True, False)

    def __init__(self, all_sprites, x, y):
        super().__init__(all_sprites)
        self.live = True # проверка живой ли
        self.jump = False # проверка: прыгаем или нет
        self.y_change = 0
        self.image = Doodle.image_r
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    # Проверка столкновения дудла с каким-либо спрайтом платформы
    def check_collision(self, platform):
        collision = pygame.sprite.spritecollide(self, platform, False)
        # Проверка, что столкновение именно сверху идет, а не снизу
        if (collision and self.y_change > 0) or (collision and self.y_change < 0 and collision[0].rect.y - self.rect.y >= 60):
            return True
        else:
            return False

    # Обновление позиции спрайта
    def update(self, platform, x_change, pos):
        jump_h = 10 # высота прыжка (можно удобно менять)
        g = 0.6 # значение гравитации (можно удобно менять)
        # Отзеркаливание дудла в зависимости от того, в какую сторону крайний раз было движение
        if pos < 0:
            self.image = Doodle.image_l
        else:
            self.image = Doodle.image_r
        # Если прыгнули(отскочили от платформы), то изменение по Y меняет направление
        if self.jump:
            self.y_change = -jump_h
            self.jump = False
        # Изменение координаты Y дудла на переменную изменения Y
        self.rect.y += self.y_change
        # Изменение изменения Y (прошу прощения за тавтологию) в зависимости от гравитации (имитация свободного падения)
        self.y_change += g
        # Если оттолкнулись, то прыгаем
        self.jump = self.check_collision(platform)
        # Изменение X от нажатия стрелок
        self.rect.x += x_change
        # Чтобы игрок уходя вправо появлялся слева
        self.rect.x %= 400
        # Проверка на смерть. Умирает, если ушел ниже экрана
        if self.rect.y > 600:
            self.kill()
            self.live = False
