import pygame
from pygame.locals import *
import math


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, rect=None):
        self.fps = 240
        self.num_frames = 17
        self.delay = self.fps / self.num_frames
        self.last_tick = pygame.time.get_ticks()
        #the image will be changed to use the size of the object that has exploded
        self.image = pygame.transform.scale(pygame.image.load("media/explosion/frames000a.png"), (200, 200))
        self.rect = self.image.get_rect()
        self.current_frame = 0

        self.rect = self.rect.move(x, y)

        self.exploding = True

    def tick(self):
        t = pygame.time.get_ticks()
        #print t
        if t - self.last_tick > self.delay:
            self.current_frame += 1
            #new_image = str()
            if self.current_frame < 10:
                new_image = "media/explosion/frames00" + str(self.current_frame) + "a.png"
            elif self.current_frame < 16:
                new_image = "media/explosion/frames0" + str(self.current_frame) + "a.png"
            else:
                new_image = "media/empty.png"
                self.exploding = False

            self.image = pygame.transform.scale(pygame.image.load(new_image), (200, 200))
        self.last_tick = t
