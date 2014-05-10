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
            self.image=pygame.image.load("media/Empire/sw_tief.png")
            #self.tieImage = pygame.transform.scale(self.tieImage, (,)) not sure what size to do
            self.image=pygame.transform.rotate(self.image, -90)

            self.rect=self.image.get_rect()
            self.shipType = 2 #differentiate between ship types
            self.hp = 2
            self.alive = True
            start_x = self.gs.width
            start_y = random.randint(65, gs.height-65)
            self.rect=self.rect.move(start_x, start_y)

    def tick(self):
        if self.alive:
            self.rect = self.rect.move(-5, 0)
            collision_list = Rect.collidelistall(self.rect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1
            if self.hp <= 0:
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.rect.x, self.rect.y)
                self.gs.explosions.append(new_explosion)

class TieBomber(pygame.sprite.Sprite):
    def __init__(self, gs= None):
            pygame.sprite.Sprite.__init__(self)
            self.gs=gs
            self.image=pygame.image.load("media/Empire/tie_bomber.png")
            self.image=pygame.transform.rotate(self.image, 90)
            self.rect=self.image.get_rect()
            self.shipType = 3 #differentiate between ship types
            self.hp = 3
            self.alive = True
            start_x = self.gs.width
            start_y = random.randint(65, gs.height-65)
            self.rect=self.rect.move(start_x, start_y)

    def tick(self):
        if self.alive:
            self.rect = self.rect.move(-5, 0)
            collision_list = Rect.collidelistall(self.rect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1
            if self.hp <= 0:
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.rect.x, self.rect.y)
                self.gs.explosions.append(new_explosion)

class TieInterceptor(pygame.sprite.Sprite):
    def __init__(self, gs= None):
            pygame.sprite.Sprite.__init__(self)
            self.gs=gs
            self.image=pygame.image.load("media/Empire/tie_interceptor.png")
            self.image=pygame.transform.rotate(self.image, 90)
            self.rect=self.image.get_rect()
            self.shipType = 1 #differentiate between ship types
            self.hp = 1
            self.alive = True
            start_x = self.gs.width
            start_y = random.randint(65, gs.height-65)
            self.rect=self.rect.move(start_x, start_y)

    def tick(self):
        if self.alive:
            self.rect = self.rect.move(-5, 0)
            collision_list = Rect.collidelistall(self.rect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1
            if self.hp <= 0:
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.rect.x, self.rect.y)
                self.gs.explosions.append(new_explosion)

class LaserTurret(pygame.sprite.Sprite):
    def __init__(self, gs = None):
        pygame.sprite.Sprite.__init__(self)
        self.gs=gs
        self.image=pygame.image.load("media/turret.png")
        self.image=pygame.transform.rotate(self.image, 210)
        self.image = pygame.transform.scale(self.image, (70,140))
        self.rect=self.image.get_rect()
        self.laserImage=pygame.image.load("media/Laser_Beam.png")
        self.laserImage=pygame.transform.scale(self.laserImage, (70,400))
        self.laserRect=self.laserImage.get_rect()
        self.laserRect.bottom=gs.height-250
        self.shipType = 4
        self.hp = 4
        self.alive = True
        
        start_x = self.gs.width
        choice = random.randint(1,2)#choose between top or bottom of screen
        if choice == 1:
            start_y = 30
            self.image=pygame.transform.rotate(self.image, 180)
        else:
            start_y = gs.height-150
        #self.laserRect=self.laserRect.move(start_x, self.gs.height / 2)
        self.rect=self.rect.move(start_x, start_y)
        self.laserRect=self.laserRect.move(start_x, 200)
        print "turret made"

    def tick(self):
        if self.alive:
            self.rect=self.rect.move(-3,0)
            self.laserRect=self.laserRect.move(-3,0)
            collision_list = Rect.collidelistall(self.rect, self.gs.lazers)
            for collision in collision_list:
                if self.gs.lazers[collision].active:
                    self.gs.lazers[collision].active = False
                    self.hp -= 1
            if self.hp <= 0:
                self.gs.explosion_sound.play()
                self.alive = False
                new_explosion = Explosion(self.rect.x, self.rect.y)
                self.gs.explosions.append(new_explosion)
