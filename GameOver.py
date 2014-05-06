#GameOver

import pygame
from pygame.locals import *
import sys

class GameOver:
    def __init__(self, gs):
        self.gs = gs
        
        #Title
        self.titlefont = pygame.font.Font("media/fonts/Starjedi.ttf", 40)
        #play again button
        self.subFont = pygame.font.Font("media/fonts/Starjedi.ttf", 28)
        self.playText = self.subFont.render("Play Again", 1, (255, 255, 255))
        self.playPos = self.playText.get_rect()
        self.playPos.centerx = 600
        self.playPos.centery = 400
        self.gs.screen.blit(self.playText, self.playPos)

        
    def gameResult(self, success):
        #set background based on success
        while True:
            if success == 1:
                self.image = pygame.transform.scale(pygame.image.load("media/Victory_Celebration.png"), (self.gs.width, self.gs.height))
                self.titleText = self.titlefont.render("Mission Success!", 1, (255, 255, 255))
                self.subText = self.subFont.render("You're a hero to the Rebel Alliance!", 1, (255, 215, 0))
            else:
                self.image = pygame.transform.scale(pygame.image.load("media/DeathStarLaser.jpg"), (self.gs.width, self.gs.height))
                self.titleText = self.titlefont.render("You have failed for the last time", 1, (255, 255, 255))
                self.subText = self.subFont.render("The Rebel base is destroyed.", 1, (255, 215, 0))
            self.rect = self.image.get_rect()
            
            #set title text
            self.titlePos = self.titleText.get_rect()
            self.titlePos.centerx = self.gs.screen.get_rect().centerx

            #set subtitle text
            self.subPos = self.subText.get_rect()
            self.subPos.centerx = self.gs.screen.get_rect().centerx
            self.subPos.centery = self.gs.screen.get_rect().height / 3
            self.gs.screen.blit(self.image, self.rect)
            self.gs.screen.blit(self.titleText, self.titlePos)
            self.gs.screen.blit(self.subText, self.subPos)

            for event in pygame.event.get():
                    if event.type == QUIT:  #if user clicks red x in corner, exit
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:  #if left mouse button is clicked
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            if self.playPos.collidepoint(mouse_x, mouse_y):
                                print "play again" #yes, the player wants to play again
            pygame.display.flip()

        
        
        
        
