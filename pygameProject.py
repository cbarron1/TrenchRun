#Cody Barron & Laura Cronin
#Trench Run

import sys
#import os
import pygame
from pygame.locals import *
from Player import Player
from Enemy import Enemy, TieFighter, TieBomber, TieInterceptor, LaserTurret
from Unit import Unit
from TitleScreen import TitleScreen
from GameOver import GameOver
import random


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
        self.lazer_sound = pygame.mixer.Sound("media/audio/blaster.wav")
        self.explosion_sound = pygame.mixer.Sound("media/audio/explode.wav")

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

        self.player = Player(1, self)
        self.enemy = Enemy(self)
        
        self.enemies = list()
        self.lazers = list()
        self.explosions = list()
        self.box = list()

        self.computerImage = pygame.image.load("media/navComputer.png")
        self.compRect = self.computerImage.get_rect()
        self.compRect.centerx = self.screen.get_rect().centerx # center of screen
        self.compRect.centery = 465 #?
        self.navCompFont = pygame.font.Font("media/fonts/Starjedi.ttf", 15) # change font?

        self.fps = 60

    def title(self):
        self.titleScreen = TitleScreen(self)
        self.titleScreen.title()

    def endScreen(self, success):
        self.finalScreen = GameOver(self)
        if success == 1:
            self.finalScreen.gameResult(1)
        else:
            self.finalScreen.gameResult(0)
                    
    def main(self):
        distanceTravelled = 0
        toGo = 0
        success = 1
        #enter loop
        while True:
            self.clock.tick(self.fps)
            shipDecider = random.randint(1,200)
            #create enemy ships based on distanceTravelled
            if (shipDecider < 3):
                interceptor=TieInterceptor(self)
                self.enemies.append(interceptor)
            elif (shipDecider == 4) or (shipDecider== 5):
                tie=TieFighter(self)
                self.enemies.append(tie)
            elif shipDecider == 6:
                bomber=TieBomber(self)
                self.enemies.append(bomber)
            elif shipDecider == 7:
                turret=LaserTurret(self)
                self.enemies.append(turret)
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

            self.player.tick()

            self.screen.fill(self.black)
            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(self.background2.image, self.background2.rect)
            self.background.tick()
            self.background2.tick()

            #print len(self.enemies)
             
            if (distanceTravelled % 50) == 0:
                gameTime = distanceTravelled / 50
                toGo = 203-gameTime #may want to speed up this timing
                #print gameTime
            distanceTravelled = distanceTravelled + 1 #add to distance travelled
                
            #control enemy ships
            for enemy in self.enemies:
                if enemy.alive == False or enemy.rect.x < 0:
                    self.enemies.remove(enemy)
                    continue
                enemy.tick()
                self.screen.blit(enemy.image, enemy.rect)
                if enemy.hp == 4:#the enemy is a laser turret
                    self.screen.blit(enemy.laserImage, enemy.laserRect)

            for lazer in self.lazers:
                lazer.tick()
                self.screen.blit(lazer.image, lazer.rect)
                if lazer.rect.x > self.width or lazer.rect.y > self.height or lazer.rect.x < 0 or lazer.rect.y < 0:
                    self.lazers.remove(lazer)

            for explosion in self.explosions:
                explosion.tick()
                if explosion.exploding:
                    self.screen.blit(explosion.image, explosion.rect)
                else:
                    self.explosions.remove(explosion)
            print "player hp:"
            print self.player.hp 
            if self.player.hp <= 0:
                self.screen.fill(self.black)
                gameOver_screen = GameOver(self)
                gameOver_screen.gameResult(1)
            self.screen.blit(self.player.image, self.player.rect)

            #Navigation Computer graphic
            if toGo == 10:
                self.navSound = pygame.mixer.Sound("media/audio/computerOff.wav")
                self.navSound.play()
            if toGo > 10 :
                self.screen.blit(self.computerImage, self.compRect)
                toGoStr = str(toGo)
                self.compText = self.navCompFont.render(toGoStr, 1, (255, 0, 0))
                self.compTextPos = self.compText.get_rect()
                self.compTextPos.centerx = 480
                self.compTextPos.centery = 530 #?
                self.screen.blit(self.compText, self.compTextPos)

            pygame.display.flip()

if __name__ == '__main__':
    gs = GameSpace()
    #while True:
    gs.title()
    gs.main()

            
            

