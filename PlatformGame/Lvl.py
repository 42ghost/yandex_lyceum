import pygame
import os
import sys
import time
import CharacterMod
import WallMod
import CameraMod
import CoinsMod


def Level(level, data_fon, font=None, namber="", columns=4, hp=3):
    pygame.init()
    size = WIDTH, HEIGHT = 1000, 512
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()

    score = 0

    def draw_win():
        font = pygame.font.Font(None, 92)
        string_rendered = font.render("Финиш", True, pygame.Color("#92f491"))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 240
        intro_rect.x = 380
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()

    def draw_lose():
        font = pygame.font.Font(None, 97)
        string_rendered = font.render(
            "Поражение", True, pygame.Color("#fb8754"))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 232
        intro_rect.x = 311
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()

    def load_image(name, colorkey=None):
        fullname = os.path.join("data", name)
        try:
            image = pygame.image.load(fullname).convert()
        except:
            print(f"Файл {name} не найден.")
            exit()

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()

        return image

    def load_level(filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        try:
            with open(filename, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]
        except:
            print("Нет карты")
            sys.exit()

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками (".")
        return list(map(lambda x: x.ljust(max_width, "."), level_map))

    # загружаем изображения
    wall_image = load_image(f"wall{namber}.png", -1)
    platform_image = load_image(f"platform{namber}.png", -1)
    front_wall_image = load_image(f"front_wall{namber}.png", -1)
    finish_image = load_image("finish.png", -1)
    health_image = load_image("health.png", -1)
    character_animation = (
        load_image(f"character{namber}.png", -1), columns, 1)
    enemy_animation = (
        load_image(f"enemy{namber}.png", -1), columns, 1)

    coin_animation = (
        load_image(f"coin{namber}.png", -1), columns, 1)

    tile_width = tile_height = 32

    # основной персонаж
    character = None

    # группы спрайтов
    tiles_group = pygame.sprite.Group()
    mortal_tiles_group = pygame.sprite.Group()
    character_group = pygame.sprite.Group()
    enemys_group = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    walls = []

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    wall = WallMod.Wall(
                        wall_image, x * tile_width, y * tile_height)
                    tiles_group.add(wall)
                    all_sprites.add(wall)
                    walls.append(wall)
                elif level[y][x] == '0':
                    wall = WallMod.Wall(
                        wall_image, x * tile_width, y * tile_height)
                    tiles_group.add(wall)
                    all_sprites.add(wall)
                elif level[y][x] == '-':
                    platform = WallMod.Wall(
                        platform_image, x * tile_width, y * tile_height)
                    tiles_group.add(platform)
                    all_sprites.add(platform)
                    walls.append(platform)
                elif level[y][x] == '_':
                    platform = WallMod.Wall(
                        platform_image, x * tile_width,
                        (y + 0.5) * tile_height)
                    tiles_group.add(platform)
                    all_sprites.add(platform)
                    walls.append(platform)
                elif level[y][x] == '+':
                    front_wall = WallMod.Wall(
                        front_wall_image, x * tile_width, y * tile_height)
                    tiles_group.add(front_wall)
                    all_sprites.add(front_wall)
                elif level[y][x] == '<':
                    finish = WallMod.Wall(
                        finish_image, x * tile_width, y * tile_height)
                    tiles_group.add(finish)
                    all_sprites.add(finish)
                elif level[y][x] == '@':
                    new_character = CharacterMod.Character(
                        x * tile_width, y * tile_height, *character_animation,
                        speed_x=3, speed_up=9, speed_down=0.5)
                    character_group.add(new_character)
                    all_sprites.add(new_character)
                elif level[y][x] == '&':
                    new_enemy = CharacterMod.Enemy(
                        x * tile_width, y * tile_height, *enemy_animation,
                        speed_x=2, speed_down=0.5)
                    enemys_group.add(new_enemy)
                    all_sprites.add(new_enemy)
                elif level[y][x] == '*':
                    new_coin = CoinsMod.Coin(
                        x * tile_width, y * tile_height, *coin_animation)
                    all_sprites.add(new_coin)
                    coins_group.add(new_coin)

            for i in range(0, len(level[y]) * tile_width, tile_width):
                mortal_wall = WallMod.Wall(
                    wall_image, i, len(level) * tile_height + 100)
                mortal_tiles_group.add(mortal_wall)
                all_sprites.add(mortal_wall)

        level_width = len(level[y]) * tile_width  # Высчитываем ширину уровня
        level_height = len(level) * tile_height  # высоту
        level_size = (level_width, level_height)

        # вернем игрока, а также размер поля в клетках
        return new_character, x, y, level_size, finish

    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + WIDTH / 2, -t + HEIGHT / 2

        l = min(0, l)  # Не двигаем дальше левой границы
        l = max(-(camera[2] - WIDTH), l)  # дальше правой границы
        t = max(-(camera[3] - HEIGHT), t)  # дальше нижней границы
        t = min(0, t)  # верхней границы

        return (l, t, w, h)


    level_name = level
    level = load_level(level)

    character, level_x, level_y, level_size, finish = generate_level(level)
    camera = CameraMod.Camera(camera_configure, *level_size)

    fon = pygame.transform.scale(load_image(data_fon), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            # закрываем уровень
            if event.type == pygame.QUIT:
                running = False

            # проверяем нажатие клавиши
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    character.move_up = True
                if event.key == pygame.K_d:
                    character.move_right = True
                if event.key == pygame.K_a:
                    character.move_left = True

            # проверяем отпускание клавиши
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    character.move_up = False
                if event.key == pygame.K_d:
                    character.move_right = False
                if event.key == pygame.K_a:
                    character.move_left = False

            # Выход, если персонаж пересёк флаг
            if pygame.sprite.collide_rect(character, finish):
                draw_win()
                time.sleep(1.5)
                running = False

        # двигаем персонажа
        character.move(walls, level_size[0])
        if pygame.sprite.spritecollide(character, coins_group, True):
            score += 50
        for c in coins_group:
            c.update_animation()

        for en in enemys_group:
            # двигаем врага, если его видно
            ogr_l = camera.apply(en)[0]
            if 100 + WIDTH >= ogr_l >= -100:
                en.move(walls, level_size[0])

            if pygame.sprite.collide_rect(character, en):
                # убираем врага и отбрасываем персонажа вверх,
                # если персонаж падает на врага
                if character.imp_y > character.speed_down:
                    en.kill()
                    character.imp_y = -character.speed_up
                    score += 100

                # иначе персонаж теряет жизнь, и уровень начинается заново
                else:
                    if hp - 1 != 0:
                        Level(level_name, data_fon, font, namber, columns, hp - 1)
                        running = False
                    else:
                        draw_lose()
                        time.sleep(2)
                        running = False

        # персонаж теряет жизнь, и уровень начинается заново,
        # если персонаж взаимодействует со смертельными тайлами
        if pygame.sprite.spritecollideany(character, mortal_tiles_group):
            if hp - 1 != 0:
                Level(level_name, data_fon, font, namber, columns, hp - 1)
            else:
                draw_lose()
                time.sleep(2)
            running = False

        camera.update(character)    # изменяем ракурс камеры

        # отрисовываем уровень
        screen.blit(fon, (0, 0))
        screen.blit(character.image, camera.apply(character))
        for sprite in all_sprites:
            if not type(sprite) is CharacterMod.Character:
                screen.blit(sprite.image, camera.apply(sprite))
        # Рисуем хп
        for i in range(hp):
            screen.blit(health_image, (i * tile_height, 5))
        # Рисуем счёт
        string_rendered = font.render(f"Score: {score}", True, pygame.Color("#ffeb0e"))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = tile_height + 5
        intro_rect.x = 5
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)
