from pygame import sprite
import pygame


class Coin(sprite.Sprite):
    def __init__(
            self, pos_x, pos_y, sheet, columns, rows):
        sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            pos_x + 8, pos_y + 8)

        self.animation_timer = 0
        self.speed_animation = 5

    # нарезка атласа на кадры анимации
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, 0)
                frame = sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))
                self.frames.append(frame)

    def update_animation(self):

        # меняем кадр при необходимости
        self.animation_timer = \
            (self.animation_timer + 1) % self.speed_animation
        if self.animation_timer == 0:
                self.cur_frame = \
                    (self.cur_frame + 1) % len(self.frames)
                self.image = \
                    self.frames[self.cur_frame]
