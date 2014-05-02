#Cody Barron
#PyGame Primer

import sys
#import os
import pygame
from pygame.locals import *
from Player import Player
from Enemy import Enemy
from Unit import Unit

class DragBox:
    def __init__(self, gs, team):
        self.gs = gs
        self.team = team
        self.start_x, self.start_y = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.start_x, self.start_y, 1, 1)

    def tick(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        width = mouse_x - self.start_x
        height = mouse_y - self.start_y
        self.rect = pygame.Rect(self.start_x, self.start_y, width, height)


class Background(pygame.sprite.Sprite):
    def __init__(self, gs):
        self.gs = gs
        self.image = pygame.transform.scale(pygame.image.load("media/trench1.jpg"), (gs.width, gs.height))
        self.rect = self.image.get_rect()

    def tick(self):
        self.rect = self.rect.move((-1,0))
        if self.rect.x <= -gs.width:
            self.rect = self.rect.move((2*gs.width, 0))


class GameSpace:
    def __init__(self):
        pygame.init()
        #pygame.key.set_repeat(1,50)
        self.lazer_sound = pygame.mixer.Sound("media/screammachine.wav")
        self.explosion_sound = pygame.mixer.Sound("media/explode.wav")

        self.size = self.width, self.height = 960, 540
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size)

        self.titlefont = pygame.font.Font("media/fonts/Starjedi.ttf",54)
        self.text = self.titlefont.render("Trench Run", 1, (5, 5, 5))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = self.screen.get_rect().centerx

        self.background = Background(self)
        self.background2 = Background(self)
        self.background2.rect = self.background2.rect.move((self.width, 0))

        self.clock = pygame.time.Clock()

        self.player = Player(self)
        self.enemy = Enemy(self)

        self.enemies = list()
        self.lazers = list()
        self.explosions = list()
        self.box = list()

        self.fps = 60

    def title(self):
        print "TITLE SCREEN"
        #set up game title
        self.titlefont = pygame.font.Font("media/fonts/Starjedi.ttf",86)
        self.titleText = self.titlefont.render("Trench Run", 1, (255, 255, 255))
        self.titlepos = self.titleText.get_rect()
        self.titlepos.centerx = self.screen.get_rect().centerx

        #single player title
        self.playerfont = pygame.font.Font("media/fonts/Starjedi.ttf", 36)
        self.player1Text = self.playerfont.render("Single Player", 1, (255, 0, 0))
        self.player1pos = self.player1Text.get_rect()
        self.player1pos.centerx = self.screen.get_rect().centerx
        self.player1pos.y = 165

        #multiplayer title
        self.player2Text = self.playerfont.render("Two Players", 1, (255, 0, 0))
        self.player2pos = self.player2Text.get_rect()
        self.player2pos.centerx = self.screen.get_rect().centerx
        self.player2pos.y = 265

        #instructions title
        self.instructionText = self.playerfont.render("instructions", 1, (255, 255, 255))
        self.instpos = self.instructionText.get_rect()
        self.instpos.centerx = self.screen.get_rect().centerx
        self.instpos.y = 365

        #blit text elements to screen
        self.screen.blit(self.titleText, self.titlepos)
        self.screen.blit(self.player1Text, self.player1pos)
        self.screen.blit(self.player2Text, self.player2pos)
        self.screen.blit(self.instructionText, self.instpos)

        pygame.display.flip()
        
        #loop to wait for clicks
        #while title running variable
        titleRunning = 1 #variable to keep track of when title options should be running
        while titleRunning:
            for event in pygame.event.get():
                if event.type == QUIT: #if user clicks red x in corner, exit
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]: #if left mouse button is clicked
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        #if event.button == 1: should do same thing
                        #if mouse pos is in single player box, get ship selection ready
                        if self.player1pos.collidepoint(mouse_x, mouse_y):
                            print "First option pressed"
                            self.screen.fill(self.black)
                            #make second 2 options disappear, show ship options as new buttons
                        #if mouse pos is in multiplayer box, wait for connection (?)
                        if self.player2pos.collidepoint(mouse_x, mouse_y):
                            print "Waiting for connection"
                            self.screen.fill(self.black)
                            #Add networking elements here
                        #if mouse pos is in instructions box, open instructions page
                        if self.instpos.collidepoint(mouse_x, mouse_y):
                            #bring up a new instructions screen
                            print "instructions options pressed"
                            self.screen.fill(self.black)
                            titleRunning = 0

            self.screen.blit(self.titleText, self.titlepos)

    
                    
                    
    def main(self):
        #enter loop
        while True:
            self.clock.tick(self.fps)

            #handle user inputs HERE
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    self.player.onKeyDown(event.key)
                elif event.type == KEYUP:
                    self.player.onKeyUp(event.key)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        drag_box = DragBox(self, 1)
                        self.box.append(drag_box)
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.box:
                            print Rect.colliderect(self.box[0].rect, self.enemy.rect)
                            self.box.pop()

            self.player.tick()
            self.screen.fill(self.black)
            self.enemy.tick()

            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(self.background2.image, self.background2.rect)
            self.background.tick()
            self.background2.tick()

            for lazer in self.lazers:
                lazer.tick()
                self.screen.blit(lazer.image, lazer.rect)
                if lazer.rect.x > self.width or lazer.rect.y > self.height or lazer.rect.x < 0 or lazer.rect.y < 0:
                    self.lazers.remove(lazer)

            if self.enemy.alive:
                self.screen.blit(self.enemy.image, self.enemy.rect)

            for explosion in self.explosions:
                explosion.tick()
                if explosion.exploding:
                    self.screen.blit(explosion.image, explosion.rect)
                else:
                    self.explosions.remove(explosion)

            for item in self.box:
                item.tick()
                pygame.draw.rect(self.screen, (50, 255, 50), item.rect, 1)

            self.screen.blit(self.player.image, self.player.rect)

            pygame.display.flip()

if __name__ == '__main__':
    gs = GameSpace()
    gs.title()
    gs.main()

