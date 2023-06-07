import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_image, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = wall_image
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
