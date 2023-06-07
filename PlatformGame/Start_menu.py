import pygame
import os
from Lvl import Level


pygame.init()
running = True
FPS = 60


def load_image(name, colour_key=None):
    try:
        image = pygame.image.load(name).convert()
    except:
        print(f'Не существует файла {name}')
        exit()
    if colour_key is not None:
        if colour_key == -1:
            colour_key = image.get_at((0, 0))
        image.set_colorkey(colour_key)
    else:
        image = image.convert_alpha()
    return image

def load_font(name):
    fullname = os.path.join("data", name)
    try:
        font_menu = pygame.font.Font(fullname, 42)
        font_level = pygame.font.Font(fullname, 32)
    except:
        print(f'Не существует файла {name}')
        exit()

    return font_menu, font_level

fonts = load_font("font.ttf")

def draw_fon(n):
    width, height = 1000, 512
    screen = pygame.display.set_mode((width, height))
    fon_list = [("data/fon_start_1.jpg", "#e0ff7a", "#5b99ea"),
                ("data/fon_start_2.jpg", "#e0ff7a", "#ff0036"),
                ("data/fon_start_3.jpg", "#e0ff7a", "#93ec00"),
                ("data/fon_start_4.jpg", "#e0ff7a", "#5b99ea")]
    name_fon = fon_list[n][0]
    color_text_lvl = fon_list[n][1]
    color_text_down = fon_list[n][2]
    fon = pygame.transform.scale(load_image(name_fon), (width, height))
    screen.blit(fon, (0, -2))

    # "Кнопки уровней"
    intro_text = ["Уровень 1", "Уровень 2", "Уровень 3", "Уровень 4"]

    font = pygame.font.Font(None, 46)
    text_coord = 51
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color(color_text_lvl))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 57
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # "Кнопка выхода"
    font = pygame.font.Font(None, 30)
    text_coord = 485
    string_rendered = font.render("Выход", True, pygame.Color(color_text_down))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 50
    screen.blit(string_rendered, intro_rect)

    # "Кнопка фона"
    font = pygame.font.Font(None, 30)
    text_coord = 485
    string_rendered = font.render(
        "Сменить фон", True, pygame.Color(color_text_down))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 830
    screen.blit(string_rendered, intro_rect)


def start_screen():
    sound = pygame.mixer.Sound("data/fon_muse.mp3")
    sound.set_volume(0.2)
    sound.play(True)
    n = 0
    draw_fon(n)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # начинаем игру. Запускается карта по клику
                if 53 <= event.pos[0] <= 215 and 70 <= event.pos[1] <= 100:
                    Level("levelex.txt", "fon_1.jpg", font=fonts[1])
                    draw_fon(n)
                elif 53 <= event.pos[0] <= 215 and 125 <= event.pos[1] <= 156:
                    Level("levelex_2.txt", "fon_2.jpg",
                          font=fonts[1], namber="_2", columns=6)
                    draw_fon(n)
                elif 53 <= event.pos[0] <= 215 and 155 <= event.pos[1] <= 206:
                    Level("levelex_3.txt", "fon_3.jpg",
                          font=fonts[1], namber="_3", columns=6)
                    draw_fon(n)
                elif 53 <= event.pos[0] <= 215 and 225 <= event.pos[1] <= 256:
                    Level("levelex_4.txt", "fon_4.jpg",
                          font=fonts[1], namber="_3", columns=6)
                    draw_fon(n)
                elif 47 <= event.pos[0] <= 120 and 480 <= event.pos[1] <= 505:
                    exit()
                elif 825 <= event.pos[0] <= 963 and 480 <= event.pos[1] <= 505:
                    n = (n + 1) % 4
                    draw_fon(n)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
