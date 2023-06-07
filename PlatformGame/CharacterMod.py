from pygame import sprite
import pygame


class Character(sprite.Sprite):
    def __init__(
            self, pos_x, pos_y, sheet, columns,
            rows, speed_x=2, speed_up=10, speed_down=0.5):
        sprite.Sprite.__init__(self)
        self.frames = [[], []]
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[0][0][self.cur_frame]
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)

        self.imp_x = 0
        self.imp_y = 0

        self.speed_x = speed_x
        self.speed_up = speed_up
        self.speed_down = speed_down

        self.on_ground = False
        self.move_right = False
        self.move_left = False
        self.move_up = False

        self.animation_timer = 0
        self.state = 0
        self.speed_animation = 5
        self.side = 0

    def move(self, group, level_width):
        # обнуляем горизонтальную скорость персонажа,
        # если не зажата нужная клавиша или персонаж на краю уровня
        if not(self.move_left or self.move_right) or\
                (self.rect.x + self.rect.w) > level_width or\
                self.rect.x < 0:
            self.imp_x = 0
            self.state = 0

        # увеличиваем горизонтальную скорость персонажа,
        # если он на земле и зажата нужная клавиша
        if self.move_right and self.on_ground and\
                (self.rect.x + self.rect.w) < level_width:
            self.imp_x = self.speed_x
            self.state = 1
            self.side = 0

        # уменьшаем горизонтальную скорость персонажа,
        # если он на земле и зажата нужная клавиша
        if self.move_left and self.on_ground and self.rect.x > 0:
            self.imp_x = -self.speed_x
            self.state = 1
            self.side = 1

        # уменьшаем вертикальную скорость персонажа,
        # если он на земле и зажата нужная клавиша
        if self.move_up and self.on_ground:
            self.imp_y = -self.speed_up
            self.state = 2

        # увеличиваем вертикальную скорость персонажа,
        # если он не на земле
        if not self.on_ground:
            self.imp_y += self.speed_down

        # двигаем и проверяем персонажа
        # на взаимодействие с уровнем
        self.on_ground = False

        self.rect.y += self.imp_y
        self.collide(group, 0, self.imp_y)

        self.rect.x += self.imp_x
        self.collide(group, self.imp_x, 0)

        # обновляем анимацию
        self.update_animation()

    def collide(self, walls, imp_x, imp_y):
        for w in walls:
            if sprite.collide_rect(self, w):
                # корректируем положение персонажа
                # относительно обьектов
                if imp_x > 0:
                    self.rect.right = w.rect.left

                if imp_x < 0:
                    self.rect.left = w.rect.right

                if imp_y > 0:
                    self.rect.bottom = w.rect.top
                    self.on_ground = True
                    self.imp_y = 0

                if imp_y < 0:
                    self.rect.top = w.rect.bottom
                    self.imp_y = 0

    # нарезка атласа на кадры анимации
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // (rows * 4))
        for t in range(4):
            self.frames[0].append([])
            self.frames[1].append([])
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * (j + t))
                    frame = sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size))
                    self.frames[0][t].append(frame)
                    self.frames[1][t].append(
                        pygame.transform.flip(frame, True, False))

    def update_animation(self):
        # корректируем задержку смены кадров
        if self.state == 0:
            self.speed_animation = 10
        elif self.state == 2:
            self.speed_animation = 10
        elif self.state == 1:
            self.speed_animation = 6
        elif self.state == 1:
            self.speed_animation = 6

        # меняем кадр при необходимости
        if not (self.cur_frame == 3 and self.state == 2):
            self.animation_timer = \
                (self.animation_timer + 1) % self.speed_animation
            if self.animation_timer == 0:
                self.cur_frame = \
                    (self.cur_frame + 1) % len(self.frames[0][0])
                self.image = \
                    self.frames[self.side][self.state][self.cur_frame]


class Enemy(Character):
    def __init__(
            self, pos_x, pos_y, sheet, columns,
            rows, speed_x=2, speed_up=10, speed_down=0.5):
        super().__init__(
            pos_x, pos_y, sheet, columns,
            rows, speed_x, speed_up, speed_down)
        self.side = 0
        self.move_left = True

    def collide(self, walls, imp_x, imp_y):
        for w in walls:
            if sprite.collide_rect(self, w):
                # корректируем положение
                # и направление движения врага
                # относительно обьектов
                if imp_x > 0:
                    self.rect.right = w.rect.left
                    self.move_right = False
                    self.move_left = True

                if imp_x < 0:
                    self.rect.left = w.rect.right
                    self.move_left = False
                    self.move_right = True

                if imp_y > 0:
                    self.rect.bottom = w.rect.top
                    self.on_ground = True
                    self.imp_y = 0

                if imp_y < 0:
                    self.rect.top = w.rect.bottom
                    self.imp_y = 0
