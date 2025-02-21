import pygame
import sys

from random import randint

from CheckRecord import Record
from PlatformClass import Platform
from DoodleClass import Doodle

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню")

# Подгрузка изображений фона
bg_image_menu = pygame.image.load("images/menu.png")
bg_image_game = pygame.image.load("images/game.png")
bg_image_finish = pygame.image.load("images/finish.png")

# Подгрузка шрифтов
font = pygame.font.Font('fonts/DoodleJump_v2.ttf', 50)
font_record = pygame.font.Font('fonts/DoodleJump_v2.ttf', 45)

# Переменные, константы
x_change, speed, pos = 0, 7, 1
clock = pygame.time.Clock()

# Рекорды текущий/лучший
score = 0
high_score = Record().read_score()

# Индекс текущего окна
win_index = 0

# Класс окна меню
class MenuWindow:
    def __init__(self):
        # Список кнопок
        self.options = ["Играть", "Выйти"]
        self.option_index = 0
        # Положение группы кнопок (чтобы было удобно перемещать при необходимости)
        self.button_group_location = (270, 230)
        self.score_surface = font.render(f'Рекорд: {high_score}', True, (70, 70, 70))
        self.score_rect = self.score_surface.get_rect(center=(self.button_group_location[0], self.button_group_location[1] + 60 * 2))

    # Отрисовка кнопок
    def draw(self):
        for index, option in enumerate(self.options):
            # Закрашивание выбранной кнопки красным (выбранная определяется из self.option_index в зависимости от того, куда была наведена мышь крайний раз)
            if index == self.option_index:
                text_surface = font.render(option, True, (255, 0, 0))
            else:
                text_surface = font.render(option, True, (70, 70, 70))
            # Отрисовка текста
            text_rect = text_surface.get_rect(center=(self.button_group_location[0], self.button_group_location[1] + index * 60))
            screen.blit(text_surface, text_rect)
        screen.blit(self.score_surface, self.score_rect)

    # Выбор кнопки для self.option_index, чтобы красным закрашивалась, по наведению на нее мышью
    def update_selection(self, mouse_pos):
        for index in range(len(self.options)):
            text_surface = font.render(self.options[index], True, (70, 70, 70))
            text_rect = text_surface.get_rect(center=(self.button_group_location[0], self.button_group_location[1] + index * 60))
            if text_rect.collidepoint(mouse_pos):
                self.option_index = index
                return True

    # Непосредственно открытие выбранного окна в зависимости от self.option_index. Вызывается нажатием на ЛКМ
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


# Класс окна самой игры
class GameWindow:
    def __init__(self):
        # Инициализация PyGame
        pygame.init()
        # Настройки экрана
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump")

        # Создание групп спрайтов. Группа платформ и группа персонажа (doodle)
        self.platform_sprites = pygame.sprite.Group()
        self.doodle_sprite = pygame.sprite.Group()

        # Создание спрайта персонажа и добавление его в группу
        self.doodle = Doodle(self.doodle_sprite, 160, 350)

        # Создание первой платформы (Делается под игроком, чтобы сразу не провалиться)
        Platform(self.platform_sprites, self.doodle.rect.x, (HEIGHT / 4) * 3)
        # Создание еще 3 платформ для начала игры. Положение по x определяется рандомно, по y поровну на всю высоту экрана
        for i in range(3):
            Platform(self.platform_sprites, randint(10, 320), (HEIGHT / 4) * i)


# Класс окна проигрыша
class FinishWindow:
    def __init__(self):
        # Список кнопок
        self.options = ["Запустить заново", "Выйти"]
        self.option_index = 0
        # Также, как в меню, задача положения группе кнопок и рекорда, чтобы удобно было потом перемещать
        self.button_group_location = (200, 500)
        self.record_lable_loc = (200, 320)
        # Создание текста для отображения рекорда. Текущего и максимального
        self.score_surface = font_record.render(f'Текущий результат: {score}', True, (70, 70, 70))
        self.score_rect = self.score_surface.get_rect(center=(self.record_lable_loc[0], self.record_lable_loc[1] + 60))
        self.high_score_surface = font_record.render(f'Рекорд: {high_score}', True, (70, 70, 70))
        self.high_score_rect = self.high_score_surface.get_rect(center=(self.record_lable_loc[0], self.record_lable_loc[1] + 60 * 2))

    # Отрисовка кнопок
    def draw(self):
        for index, option in enumerate(self.options):
            # Закрашивание выбранной кнопки красным цветом. Аналогично той же функции в классе MenuWindow
            if index == self.option_index:
                text_surface = font.render(option, True, (255, 0, 0))
            else:
                text_surface = font.render(option, True, (70, 70, 70))
            text_rect = text_surface.get_rect(center=(self.button_group_location[0], self.button_group_location[1] + index * 60))
            screen.blit(text_surface, text_rect)
        screen.blit(self.score_surface, self.score_rect)
        screen.blit(self.high_score_surface, self.high_score_rect)

    # Выбор опции по наведении на него мышки, аналогично MenuWindow
    def update_selection(self, mouse_pos):
        for index in range(len(self.options)):
            text_surface = font.render(self.options[index], True, (70, 70, 70))
            text_rect = text_surface.get_rect(center=(self.button_group_location[0], self.button_group_location[1] + index * 60))
            if text_rect.collidepoint(mouse_pos):
                self.option_index = index
                return True

    # Непосредственно открытие выбранной опции по нажатию на ЛКМ. Также аналогично MenuWindow
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


# Функция запуска главного меню
def menu_window(menu_object):
    global win_index
    running = True
    # Основной игровой цикл
    while running:
        # Обновление выбранной кнопки (self.option_index) по наведению на нее мыши
        menu_object.update_selection(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running, win_index = False, None
            # Обработка нажатий клавиши
            if event.type == pygame.KEYDOWN:
                # При нажатии на R игра запускается
                if event.key == pygame.K_r:
                    running, win_index = False, 1
                # При нажатии ESC все окна закрываются. Выход из игры
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
            # Обработка нажатия на ЛКМ и вызов функции для открытия окна в соответствии с текущей выбранной кнопкой (self.option_index)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and menu_object.select_with_mouse(pygame.mouse.get_pos()):
                    running = False
        # Наложение изображения на фон меню
        screen.blit(bg_image_menu, (0, 0))
        # Отрисовка кнопок
        menu_object.draw()
        # Обновление кадра
        pygame.display.flip()


# Функция запуска игры
def game_window(game_object):
    global win_index, x_change, pos, score, high_score
    running = True
    # Основной игровой цикл
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            # Обработка нажатия на клавиши
            if event.type == pygame.KEYDOWN:
                # При нажатии на стрелку влево, изменение по координате x становится отрицательной константой скорости (потом передается в update класса спрайта персонажа)
                if event.key == pygame.K_LEFT:
                    x_change = -speed
                    pos = -1
                # Как и с нажатием на стрелку влево, только стрелка вправо
                if event.key == pygame.K_RIGHT:
                    x_change = speed
                    pos = 1
                # На ESC можно выйти в главное меню
                if event.key == pygame.K_ESCAPE:
                    running, win_index = False, 0
            # При отпускании стрелок влево/вправо изменение по X снова равно 0
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
        # Текущий счет
        score = int(Platform.score)
        # Отрисовка счета в углу игрового окна
        game_object.screen.blit(font.render(f'{score}', True, (70, 70, 70)), (0, 0))
        # Обработка смерти персонажа
        if not game_object.doodle.live:
            # Запись нового рекорда (если побил)
            if int(Platform.score) > high_score:
                high_score = int(Platform.score)
                Record().write_score(int(Platform.score))
            running, win_index = False, 2
        # Обновление кадра
        pygame.display.flip()


# Функция запуска окна поражения (похож на класс MenuWindow)
def finish_window(finish_object):
    global win_index
    running = True
    # Основной игровой цикл
    while running:
        # Обновление выбранной кнопки по наведению мыши
        finish_object.update_selection(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running, win_index = False, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running, win_index = False, 1
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and finish_object.select_with_mouse(pygame.mouse.get_pos()):
                    running = False
        # Наложение изображения на фон меню
        screen.blit(bg_image_finish, (0, 0))
        # Отрисовка кнопок
        finish_object.draw()
        # Обновление кадра
        pygame.display.flip()


# Главный цикл. Проверяется, какое окно должно быть открыто и открывает его
while win_index is not None:
    if win_index == 0:
        # Открытие окна меню
        menu_window(MenuWindow())
    if win_index == 1:
        # Сброс текущего счета
        score, Platform.score = 0, 0
        # Открытие окна игры
        game_window(GameWindow())
    if win_index == 2:
        # Открытие окна поражения
        finish_window(FinishWindow())

# Выход
sys.exit()
