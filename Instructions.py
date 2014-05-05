#Instructions.py
#The instructions screen for Trench Run

import pygame
from pygame.locals import *
import sys

class Instructions:
    def __init__(self, gs):
        self.gs = gs
        self.centerX = self.gs.screen.get_rect().centerx
        self.centerY = self.gs.screen.get_rect().centery
        self.reading = True #false when user clicks back button

        #Instructions title
        self.titlefont = pygame.font.Font("media/fonts/Starjedi.ttf", 64)
        self.instructionsText = self.titlefont.render("instructions", 1, (255, 255, 255))
        self.instPos = self.instructionsText.get_rect()
        self.instPos.centerx = self.gs.screen.get_rect().centerx

        #back button
        self.back_start_font = pygame.font.Font("media/fonts/Starjedi.ttf", 32)
        self.backText = self.back_start_font.render("Back", 1, (255, 255, 255))
        self.backTextPos = self.backText.get_rect()
        self.backTextPos.centerx = self.gs.width / 3
        self.backTextPos.centery = 484

        #setting image of WASD keys
        self.keyImage = pygame.image.load("media/keys_wasd.png")
        self.keyImage = pygame.transform.scale(self.keyImage, (185, 115))
        self.key_rect = self.keyImage.get_rect()
        self.key_rect.centerx = self.centerX - (self.gs.width / 5)
        self.key_rect.centery = 265
                                          
    def readInstructions(self):
        while self.reading:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if self.backTextPos.collidepoint(mouse_x, mouse_y):
                            self.reading = False
                            break

            self.gs.screen.fill(self.gs.black)
            self.gs.screen.blit(self.instructionsText, self.instPos)
            self.gs.screen.blit(self.keyImage, self.key_rect)
            self.gs.screen.blit(self.backText, self.backTextPos)
            pygame.display.flip()
            
                
