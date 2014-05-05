import pygame
from pygame.locals import *
import math
from Explosion import Explosion
import random
from Lazer import Lazer


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

class TieFighter(pygame.sprite.Sprite):
    def __init__(self, gs= None):
            pygame.sprite.Sprite.__init__(self)
            self.gs=gs
            self.tieImage=pygame.image.load("media/Empire/sw_tief.png")
            #self.tieImage = pygame.transform.scale(self.tieImage, (,)) not sure what size to do
            self.tieImage=pygame.transform.rotate(self.tieImage, -90)

            self.tieRect=self.tieImage.get_rect()
            self.orig_tImage=self.tieImage
            self.shipType = 2 #differentiate between ship types
            self.hp = 30
            self.alive = True
            start_x = self.gs.width
            start_y = random.randint(65, gs.height-65)
            self.tieRect=self.tieRect.move(start_x, start_y)

    def tick(self):
        if self.alive:
            self.tieRect = self.tieRect.move(-5, 0)
            collision_list = Rect.collidelistall(self.tieRect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1
            if self.hp <= 0:
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.tieRect.x, self.tieRect.y)
                self.gs.explosions.append(new_explosion)

class TieBomber(pygame.sprite.Sprite):
    def __init__(self, gs= None):
            pygame.sprite.Sprite.__init__(self)
            self.gs=gs
            self.bomberImage=pygame.image.load("media/Empire/tie_bomber.png")
            self.bomberImage=pygame.transform.rotate(self.bomberImage, -90)
            self.bomberRect=self.bomberImage.get_rect()
            self.orig_bImage=self.bomberImage#not sure if this is necessary
            self.shipType = 1 #differentiate between ship types
            self.hp = 40
            self.alive = True
            start_x = self.gs.width
            start_y = random.randint(65, gs.height-65)
            self.bomberRect=self.bomberRect.move(start_x, start_y)

    def tick(self):
        if self.alive:
            self.bomberRect = self.bomberRect.move(-5, 0)
            collision_list = Rect.collidelistall(self.bomberRect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1
            if self.hp <= 0:
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.bomberRect.x, self.bomberRect.y)
                self.gs.explosions.append(new_explosion)

class TieInterceptor(pygame.sprite.Sprite):
    def __init__(self, gs= None):
            pygame.sprite.Sprite.__init__(self)
            self.gs=gs
            self.interceptorImage=pygame.image.load("media/Empire/tie_interceptor.png")
            self.interceptorImage=pygame.transform.rotate(self.interceptorImage, -90)
            self.interceptorRect=self.interceptorImage.get_rect()
            self.orig_iImage=self.interceptorImage#not sure if this is necessary
            self.shipType = 3 #differentiate between ship types
            self.hp = 20
            self.alive = True
            start_x = self.gs.width
            start_y = random.randint(65, gs.height-65)
            self.interceptorRect=self.interceptorRect.move(start_x, start_y)

    def tick(self):
        if self.alive:
            self.interceptorRect = self.interceptorRect.move(-5, 0)
            collision_list = Rect.collidelistall(self.interceptorRect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1
            if self.hp <= 0:
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.interceptorRect.x, self.interceptorRect.y)
                self.gs.explosions.append(new_explosion)
