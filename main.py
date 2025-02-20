import pygame
import sys

from random import randint

from CheckRecord import Record
from PlatformClass import Platform
from DoodleClass import Doodle

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT, clock = 400, 600, pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню")

# Загрузка изображений фона
bg_image_menu = pygame.image.load("images/menu.png")
bg_image_game = pygame.image.load("images/game_fon.png")

# Шрифт
font = pygame.font.Font('fonts/DoodleJump_v2.ttf', 50)

# Переменные
x_change, speed, pos = 0, 7, 1

# Индекс текущего окна
win_index = 0

# Класс окна меню
class MenuWindow:
    def __init__(self):
        self.options = ["Играть", "Выйти"]
        self.score = Record().read_score()
        self.option_index = 0
        self.score_surface = font.render(f'Рекорд: {self.score}', True, (70, 70, 70))
        self.score_rect = self.score_surface.get_rect(center=(270, 350))

    # Отрисовка кнопок
    def draw(self):
        for index, option in enumerate(self.options):
            # Закрашивание выбранной кнопки красным цветом
            if index == self.option_index:
                text_surface = font.render(option, True, (255, 0, 0))
            else:
                text_surface = font.render(option, True, (70, 70, 70))
            text_rect = text_surface.get_rect(center=(270, 230 + index * 60))
            screen.blit(text_surface, text_rect)
        screen.blit(self.score_surface, self.score_rect)

    # Выбор опции по наведении на него мышки
    def update_selection(self, mouse_pos):
        for index in range(len(self.options)):
            text_surface = font.render(self.options[index], True, (70, 70, 70))
            text_rect = text_surface.get_rect(center=(270, 230 + index * 60))
            if text_rect.collidepoint(mouse_pos):
                self.option_index = index
                return True

    # Непосредственно открытие выбранной опции по нажатию на ЛКМ
    def select_with_mouse(self, mouse_pos):
        global win_index
        last_index = win_index
        if self.update_selection(mouse_pos):
            if self.option_index == 0:
                win_index = 1
            elif self.option_index == 1:
                pygame.quit()
                sys.exit()
            if last_index != win_index:
                return True


class GameWindow:
    def __init__(self):
        # Инициализация PyGame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump")

        # Загрузка изображения фона игры
        self.bg_image_game = pygame.image.load("images/game_fon.png")

        self.platform_sprites = pygame.sprite.Group()
        self.doodle_sprite = pygame.sprite.Group()

        self.doodle = Doodle(self.doodle_sprite, 160, 350)

        Platform(self.platform_sprites, self.doodle.rect.x, (HEIGHT / 5) * 4)
        for i in range(4):
            Platform(self.platform_sprites, randint(10, 320), (HEIGHT / 5) * i)


# Функция запуска главного меню
def menu_window(menu):
    running = True
    global win_index
    # Основной игровой цикл
    while running:
        # Обновление выбранной кнопки по наведению мыши
        menu.update_selection(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running, win_index = False, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and menu.select_with_mouse(pygame.mouse.get_pos()):
                    running = False

        # Наложение изображения на фон меню
        screen.blit(bg_image_menu, (0, 0))
        # Отрисовка кнопок
        menu.draw()
        # Обновление кадра
        pygame.display.flip()


# Функция запуска игры
def game_window(game_object):
    global win_index, x_change, pos
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -speed
                    pos = -1
                if event.key == pygame.K_RIGHT:
                    x_change = speed
                    pos = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_RIGHT:
                    x_change = 0
        # Отрисовка фона
        game_object.screen.blit(bg_image_game, (0, 0))
        # Отрисовка спрайта дудла
        game_object.doodle_sprite.draw(game_object.screen)
        game_object.doodle_sprite.update(game_object.platform_sprites, x_change, pos)
        # Отрисовка спрайтов платформ
        game_object.platform_sprites.draw(game_object.screen)
        game_object.platform_sprites.update(game_object.doodle.rect.x, game_object.doodle.rect.y, game_object.doodle.y_change)
        game_object.screen.blit(font.render(f'Результат: {int(Platform.score)}', True, (70, 70, 70)), (0, 0))
        pygame.display.flip()


# Главный цикл
while win_index is not None:
    if win_index == 0:
        menu_window(MenuWindow())
    if win_index == 1:
        game_window(GameWindow())

# Выход
sys.exit()
