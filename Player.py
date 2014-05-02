import pygame
import math
from pygame.locals import *
from Lazer import Lazer

class Player(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)

        self.gs = gs
        self.image = pygame.image.load("media/deathstar.png")
        self.image = pygame.transform.rotate(self.image, -45)
        self.rect = self.image.get_rect()

        self.orig_img = self.image
        self.angle = 0
        self.to_fire = False

        self.move_speed = 5
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def tick(self):
        mx, my = pygame.mouse.get_pos()

        if self.to_fire:
            new_lazer = Lazer(self.gs, self, self.angle)
            self.gs.lazers.append(new_lazer)
        else:
            self.move()

            px = self.rect.centerx
            py = self.rect.centery

            tx = mx - px
            ty = my - py

            #print str(tx) + ":" + str(ty)
            self.angle = math.atan2(ty,tx)
            #print angle
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.orig_img, math.degrees(-self.angle))
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def onClick(self):
        self.to_fire = True

    def onRelease(self):
        self.to_fire = False

    def move(self):
        if self.move_right:
            new_pos = self.rect.move((self.move_speed, 0))
            self.rect = new_pos
        elif self.move_left:
            new_pos = self.rect.move((-self.move_speed, 0))
            self.rect = new_pos
        if self.move_up:
            new_pos = self.rect.move((0, -self.move_speed))
            self.rect = new_pos
        elif self.move_down:
            new_pos = self.rect.move((0, self.move_speed))
            self.rect = new_pos

    def onKeyDown(self, key):
        #print pygame.time.get_ticks()
        if key == K_SPACE:
            self.gs.lazer_sound.play()
            self.onClick()
        elif key == K_a:
            self.move_left = True
        elif key == K_d:
            self.move_right = True
        elif key == K_w:
            self.move_up = True
        elif key == K_s:
            self.move_down = True

    def onKeyUp(self, key):
        if key == K_SPACE:
            self.onRelease()
        elif key == K_a:
            self.move_left = False
        elif key == K_d:
            self.move_right = False
        elif key == K_w:
            self.move_up = False
        elif key == K_s:
            self.move_down = False
