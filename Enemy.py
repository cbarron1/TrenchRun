import pygame
from pygame.locals import *
import math
from Explosion import Explosion


class Enemy(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.image = pygame.image.load("media/Alderaan.png")
        scale_image = pygame.transform.scale(self.image, (200, 200))
        self.image = scale_image

        self.death_image = pygame.image.load("media/globe_red100.png")
        scale_deathimage = pygame.transform.scale(self.death_image, (200, 200))
        self.death_image = scale_deathimage

        self.rect = self.image.get_rect()
        self.orig_img = self.image

        self.hp = 100
        self.alive = True

        start_x = self.gs.width - self.rect.width
        start_y = self.gs.height - self.rect.height

        self.rect = self.rect.move((start_x, start_y))

    def tick(self):
        if self.alive:
            collision_list = Rect.collidelistall(self.rect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1

            if self.hp <= 0:
                self.image = self.death_image
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.rect.x, self.rect.y)
                self.gs.explosions.append(new_explosion)
