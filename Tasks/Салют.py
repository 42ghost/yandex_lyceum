import os
import pygame
import random


pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
running = True
GRAVITY = 1


def load_image(name, colour_key=-1):
    try:
        image = pygame.image.load(name).convert()
    except:
        print('Не существует файла')
        exit()
    if colour_key is not None:
        if colour_key == -1:
            colour_key = image.get_at((0, 0))
        image.set_colorkey(colour_key)
    else:
        image = image.convert_alpha()
    return image


def create_particles(position):
    particle_count = 20
    numbers = range(-15, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Particle(pygame.sprite.Sprite):
    fire = [load_image("data/fireball.png")]
    for scale in (1, 5, 10, 15, 20, 25):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        if not self.rect.colliderect(screen_rect):
            self.kill()


all_sprites = pygame.sprite.Group()
screen_rect = (0, 0, width, height)
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # создаём частицы по щелчку мыши
            #print(pygame.mouse.get_pos())
            create_particles(pygame.mouse.get_pos())
    # Генерация в случайных точках
    #create_particles((random.randint(50, 300), random.randint(50, 300)))
    screen.fill('black')
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(25)
pygame.quit()
