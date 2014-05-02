import pygame
from Player import Player
from pygame.locals import *
import sys

class ShipSelect:
    def __init__(self, gs):
        self.gs = gs
        self.selecting = True
        self.my_ship = 1
        self.centerX = self.gs.screen.get_rect().centerx

        self.goodluck_sound = pygame.mixer.Sound("media/audio/goodluck.wav")
        self.junk_sound = pygame.mixer.Sound("media/audio/whatjunk.wav")

        self.selected_rect = pygame.Rect(0, 0, 140, 140)
        self.selected_rect.centerx = self.centerX - (self.gs.width / 3)
        self.selected_rect.centery = 236

        self.x_rect = pygame.Rect(0, 0, 140, 140)
        self.x_rect.centerx = self.centerX - (self.gs.width / 3)
        self.x_rect.centery = 236

        self.s_rect = pygame.Rect(0, 0, 140, 140)
        self.s_rect.centerx = self.centerX
        self.s_rect.centery = 236

        self.f_rect = pygame.Rect(0, 0, 140, 140)
        self.f_rect.centerx = self.centerX + (self.gs.width / 3) - 10
        self.f_rect.centery = 236

        self.selectionFont = pygame.font.Font("media/fonts/Starjedi.ttf", 54)
        self.selectionText = self.selectionFont.render("Choose  a  Starfighter", 1, (255, 255, 255))
        self.selectTextPos = self.selectionText.get_rect()
        self.selectTextPos.centerx = self.centerX

        self.shipNameFont = pygame.font.Font("media/fonts/Starjedi.ttf", 24)
        self.descriptionFont = pygame.font.Font("media/fonts/Starjedi.ttf", 16)

        self.back_start_font = pygame.font.Font("media/fonts/Starjedi.ttf", 32)
        self.backText = self.back_start_font.render("Back", 1, (255, 255, 255))
        self.backTextPos = self.backText.get_rect()
        self.backTextPos.centerx = self.gs.width / 3
        self.backTextPos.centery = 484

        self.startText = self.back_start_font.render("Start", 1, (255, 255, 255))
        self.startTextPos = self.startText.get_rect()
        self.startTextPos.centerx = 2*self.gs.width / 3
        self.startTextPos.centery = 484

        self.xwingText = self.shipNameFont.render("T-65 x-Wing", 1, (255, 255, 255))
        self.xTextPos = self.xwingText.get_rect()
        self.xTextPos.centerx = self.centerX - (self.gs.width / 3)
        self.xTextPos.centery = 128

        self.seraphText = self.shipNameFont.render("xi-38 Seraph", 1, (255, 255, 255))
        self.sTextPos = self.seraphText.get_rect()
        self.sTextPos.centerx = self.centerX
        self.sTextPos.centery = 128

        self.falconText = self.shipNameFont.render("Millenium Falcon", 1, (255, 255, 255))
        self.fTextPos = self.falconText.get_rect()
        self.fTextPos.centerx = self.centerX + (self.gs.width / 3) - 10
        self.fTextPos.centery = 128

        self.xwing_img = pygame.image.load("media/Rebel/sw_xwing.png")
        self.xwing_rect = self.xwing_img.get_rect()
        self.xwing_rect.centerx = self.centerX - (self.gs.width / 3)
        self.xwing_rect.centery = 236

        self.seraph_img = pygame.image.load("media/laser.png")

        self.falcon_img = pygame.image.load("media/Rebel/falcon.png")
        self.falcon_rect = self.falcon_img.get_rect()
        self.falcon_rect.centerx = self.centerX + (self.gs.width / 3) - 10
        self.falcon_rect.centery = 236

    def ship_select(self):

        while self.selecting:
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
                        if self.x_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_rect.centerx = self.x_rect.centerx
                            self.my_ship = 1
                        elif self.s_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_rect.centerx = self.s_rect.centerx
                            self.my_ship = 2
                        elif self.f_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_rect.centerx = self.f_rect.centerx
                            self.my_ship = 3
                        elif self.backTextPos.collidepoint(mouse_x, mouse_y):
                            self.selecting = False
                            print "GO BACK"
                            break
                        elif self.startTextPos.collidepoint(mouse_x, mouse_y):
                            self.gs.player = Player(self.my_ship,self.gs)
                            if self.my_ship == 1:
                                self.goodluck_sound.play()
                                pygame.time.delay(3000)
                            elif self.my_ship == 3:
                                self.junk_sound.play()
                                pygame.time.delay(1600)

                            self.selecting = False
                            self.gs.titleScreen.titleRunning = False



            if self.my_ship == 1:
                self.move_star = "*****"
                self.dura_star = "*"
                self.fire_star = "*****"
                self.damg_star = "**"
            elif self.my_ship == 2:
                self.move_star = "***"
                self.dura_star = "***"
                self.fire_star = "****"
                self.damg_star = "****"
            elif self.my_ship == 3:
                self.move_star = "*"
                self.dura_star = "*****"
                self.fire_star = "**"
                self.damg_star = "*****"

            self.move_text = self.descriptionFont.render("Movement:  " + self.move_star, 1, (255, 255, 255))
            self.m_text_rect = self.move_text.get_rect()
            #self.m_text_rect.centerx = self.centerX
            self.m_text_rect.x = 387
            self.m_text_rect.centery = 340


            self.dura_text = self.descriptionFont.render("Durability: " + self.dura_star, 1, (255, 255, 255))
            self.du_text_rect = self.dura_text.get_rect()
            #self.du_text_rect.centerx = self.centerX
            self.du_text_rect.x = 387
            self.du_text_rect.centery = 368
            #print self.du_text_rect.x
            #LEFT EDGE IS AT 387

            self.fire_text = self.descriptionFont.render("Fire Rate:   " + self.fire_star, 1, (255, 255, 255))
            self.fi_text_rect = self.fire_text.get_rect()
            #self.fi_text_rect.centerx = self.centerX
            self.fi_text_rect.x = 387
            self.fi_text_rect.centery = 396

            self.damg_text = self.descriptionFont.render("Damage:      " + self.damg_star, 1, (255, 255, 255))
            self.da_text_rect = self.damg_text.get_rect()
            #self.da_text_rect.centerx = self.centerX
            self.da_text_rect.x = 387
            self.da_text_rect.centery = 424

            self.gs.screen.fill(self.gs.black)
            self.gs.screen.blit(self.selectionText, self.selectTextPos)
            self.gs.screen.blit(self.xwingText, self.xTextPos)
            self.gs.screen.blit(self.seraphText, self.sTextPos)
            self.gs.screen.blit(self.falconText, self.fTextPos)

            self.gs.screen.blit(self.move_text, self.m_text_rect)
            self.gs.screen.blit(self.dura_text, self.du_text_rect)
            self.gs.screen.blit(self.fire_text, self.fi_text_rect)
            self.gs.screen.blit(self.damg_text, self.da_text_rect)

            self.gs.screen.blit(self.backText, self.backTextPos)
            self.gs.screen.blit(self.startText, self.startTextPos)

            self.gs.screen.blit(self.xwing_img, self.xwing_rect)
            self.gs.screen.blit(self.falcon_img, self.falcon_rect)

            pygame.draw.rect(self.gs.screen, (64, 64, 255), self.selected_rect, 1)

            pygame.display.flip()