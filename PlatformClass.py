import pygame
from random import randint, choice

from CheckRecord import Record


# Класс для создания спрайтов платформ
class Platform(pygame.sprite.Sprite):
    # Подгрузка изображения платформы и установление текущего счета
    image = pygame.transform.scale(pygame.image.load("sprites/platform.png"), (70, 20))
    score = 0

    def __init__(self, all_sprites, x, y):
        self.platform_sprites = all_sprites
        super().__init__(self.platform_sprites)
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    # Функция перерисовка спрайта
    def update(self, x, y, y_change):
        # Сдвиг всех платформ вниз, если персонаж выше определенного уровня и он идет вверх (имитация движения вверх)
        if y < 400 and y_change < 0:
            self.rect.y -= y_change * 1.5
            # Добавление счета. Зависит от того, насколько съехали платформы вниз
            Platform.score += 0.2
        # Обработка платформ ушедших ниже экрана
        if self.rect.y > 600:
            # Убивает ушедшую платформу
            self.kill()
            # Выбор координат x для новой платформы. Зависит от значения x координаты персонажа, чтобы она не создавалась прям над ним
            if 80 < x < 260:
                # Если персонаж в центральной части поля, то платформа делается везде, кроме прям над персонажем
                x_plat = choice([randint(10, x - 70), randint(x + 60, 320)])
            elif x < 80:
                # Если персонаж слева где-то, то платформа в правой части
                x_plat = randint(140, 320)
            else:
                # Если персонаж справа где-то, то платформа в левой части, соответственно
                x_plat = randint(10, 250)
            # Создает новую платформу выше
            Platform(self.platform_sprites, x_plat, randint(-20, -10))
