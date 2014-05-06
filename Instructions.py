#Instructions.py
#The instructions screen for Trench Run

import pygame
from pygame.locals import *
import sys

class Instructions:
    def __init__(self, gs):
        self.gs = gs
        self.controls = True
        self.centerX = self.gs.screen.get_rect().centerx
        self.centerY = self.gs.screen.get_rect().centery
        self.reading = True #false when user clicks back button

        #Instructions title
        self.titlefont = pygame.font.Font("media/fonts/Starjedi.ttf", 64)
        self.instructionsText = self.titlefont.render("instructions", 1, (255, 255, 255))
        self.instPos = self.instructionsText.get_rect()
        self.instPos.centerx = self.gs.screen.get_rect().centerx

        #Commands
        self.instFont = pygame.font.Font("media/fonts/Starjedi.ttf", 28)
        self.controlText = self.instFont.render("Game Controls", 1, (255, 0, 0))
        self.controlPos = self.controlText.get_rect()
        self.controlPos.left = 430
        self.controlPos.centery = 172
        self.wText = self.instFont.render("W -- up", 1, (255, 255, 255))#W
        self.wPos = self.wText.get_rect()
        self.wPos.left = 450
        self.wPos.centery = 200
        self.aText = self.instFont.render("A -- left", 1, (255, 255, 255))#A
        self.aPos = self.aText.get_rect()
        self.aPos.left = 450
        self.aPos.centery = 228
        self.sText = self.instFont.render("S -- down", 1, (255, 255, 255))#S
        self.sPos = self.sText.get_rect()
        self.sPos.left = 450
        self.sPos.centery = 256
        self.dText = self.instFont.render("D -- right", 1, (255, 255, 255))#D
        self.dPos = self.dText.get_rect()
        self.dPos.left = 450
        self.dPos.centery = 284
        self.fireText = self.instFont.render("space -- fire", 1, (255, 255, 255))#space
        self.firePos = self.fireText.get_rect()
        self.firePos.left = 450
        self.firePos.centery = 312
        self.objFont = pygame.font.Font("media/fonts/Starjedi.ttf", 20)
        self.objText1 = self.objFont.render("objective: Destroy enemy fighters", 1, (255, 255, 255))
        self.objPos1 = self.objText1.get_rect()
        self.objPos1.left = 450
        self.objPos1.centery = 340
        self.objText2 = self.objFont.render("and laser cannons as you approach", 1, (255, 255, 255))
        self.objPos2 = self.objText2.get_rect()
        self.objPos2.left = 470
        self.objPos2.centery = 360
        self.objText3 = self.objFont.render("the Death Star's exhaust port. Fire", 1, (255, 255, 255))
        self.objPos3 = self.objText3.get_rect()
        self.objPos3.left = 470
        self.objPos3.centery = 380
        self.objText4 = self.objFont.render("at it to destroy the Death Star!", 1, (255, 255, 255))
        self.objPos4 = self.objText4.get_rect()
        self.objPos4.left = 470
        self.objPos4.centery = 400

        #back button
        self.back_start_font = pygame.font.Font("media/fonts/Starjedi.ttf", 32)
        self.backText = self.back_start_font.render("Back", 1, (255, 255, 255))
        self.backTextPos = self.backText.get_rect()
        self.backTextPos.centerx = self.gs.width / 3
        self.backTextPos.centery = 484

        #network button
        self.net_font = pygame.font.Font("media/fonts/Starjedi.ttf", 32)
        self.net_text = self.net_font.render("Network", 1, (255, 255, 255))
        self.net_text_pos = self.net_text.get_rect()
        self.net_text_pos.centerx = 2 * self.gs.width / 3
        self.net_text_pos.centery = 484

        #controls button
        self.cont_font = self.back_start_font
        self.cont_text = self.cont_font.render("Controls", 1, (255, 255, 255))
        self.cont_text_pos = self.cont_text.get_rect()
        self.cont_text_pos.centerx = 2 * self.gs.width / 3
        self.cont_text_pos.centery = 484


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
                        if self.cont_text_pos.collidepoint(mouse_x, mouse_y) or self.net_text_pos.collidepoint(mouse_x, mouse_y):
                            self.controls = not self.controls


            self.gs.screen.fill(self.gs.black)
            self.gs.screen.blit(self.instructionsText, self.instPos)
            self.gs.screen.blit(self.backText, self.backTextPos)

            if self.controls:
                self.gs.screen.blit(self.net_text, self.net_text_pos)
                self.gs.screen.blit(self.keyImage, self.key_rect)
                self.gs.screen.blit(self.wText, self.wPos)
                self.gs.screen.blit(self.aText, self.aPos)
                self.gs.screen.blit(self.sText, self.sPos)
                self.gs.screen.blit(self.dText, self.dPos)
                self.gs.screen.blit(self.fireText, self.firePos)
                self.gs.screen.blit(self.controlText, self.controlPos)
                self.gs.screen.blit(self.objText1, self.objPos1)
                self.gs.screen.blit(self.objText2, self.objPos2)
                self.gs.screen.blit(self.objText3, self.objPos3)
                self.gs.screen.blit(self.objText4, self.objPos4)
            else:
                self.gs.screen.blit(self.cont_text, self.cont_text_pos)

            pygame.display.flip()
            
                
