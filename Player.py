import pygame
import math
from pygame.locals import *
from Lazer import Lazer

class Player(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)

        player_type = 3
        self.gs = gs
        if player_type == 1:
            self.image = pygame.image.load("media/Rebel/sw_xwing.png")
            self.image = pygame.transform.scale(self.image, (45, 39))
            self.move_speed = 15
        elif player_type == 2:
            self.image = pygame.image.load("media/laser.png")
            self.image = pygame.transform.scale(self.image, (80, 60))
            self.move_speed = 10
        elif player_type == 3:
            self.image = pygame.image.load("media/Rebel/falcon.png")
            self.image = pygame.transform.scale(self.image, (80, 105))
            self.move_speed = 5
        self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()
        self.rect.centery = self.gs.screen.get_rect().centery
        print "Height: ", self.rect.height
        print "Width: ", self.rect.width

        self.orig_img = self.image
        self.angle = 0
        self.to_fire = False

        #self.move_speed = 5
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def tick(self):
        mx, my = pygame.mouse.get_pos()

        if self.to_fire:
            new_lazer = Lazer(self.gs, self)
            self.gs.lazers.append(new_lazer)

        self.move()

    def onClick(self):
        self.to_fire = True

    def onRelease(self):
        self.to_fire = False

    def move(self):
        if self.move_right:
            if self.rect.x + self.move_speed < 240:
                self.rect = self.rect.move((self.move_speed, 0))
        elif self.move_left:
            if self.rect.x - self.move_speed > 0:
                self.rect = self.rect.move((-self.move_speed, 0))
        if self.move_up:
            if self.rect.y - self.move_speed > 60:
                self.rect = self.rect.move((0, -self.move_speed))
        elif self.move_down:
            if self.rect.y + self.rect.height + self.move_speed < self.gs.height - 60:
                self.rect = self.rect.move((0, self.move_speed))

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
