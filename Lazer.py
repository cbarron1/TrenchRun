import pygame
from pygame.locals import *
import math

class Lazer(pygame.sprite.Sprite):
    def __init__(self, gs=None, parent=None, angle=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.parent = parent
        self.image = pygame.image.load("media/laser.png")
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width

        self.start_x = self.parent.rect.x + 3*self.parent.rect.width/4
        self.start_y = self.parent.rect.y + self.parent.rect.height/2
        self.rect = self.rect.move((self.start_x, self.start_y))
        self.orig_img = self.image
        self.angle = angle

        self.active = True

        #print self.angle
        #print "COS: "+ str(math.cos(self.angle))
        #print "SIN: "+ str(math.sin(self.angle))
        self.tick_count = 0

        self.move_speed = 20
        self.move_x = self.move_speed * math.cos(self.angle)
        self.move_y = self.move_speed * math.sin(self.angle)

        #print self.move_x
        #print self.move_y

    def tick(self):
        displace_x = self.tick_count * self.move_x
        displace_y = self.tick_count * self.move_y
        self.rect = self.image.get_rect(x=self.start_x+displace_x, y=self.start_y + displace_y)
        self.tick_count += 1
