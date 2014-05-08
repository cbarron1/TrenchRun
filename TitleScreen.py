import pygame
from pygame.locals import *
import sys
from ShipSelect import ShipSelect
from Instructions import Instructions

class TitleScreen:
    def __init__(self, gs):
        self.gs = gs
        self.titleRunning = True
        self.connections = False
        
        self.titlefont = pygame.font.Font("media/fonts/Starjedi.ttf", 86)
        self.titleText = self.titlefont.render("Trench Run", 1, (255, 255, 255))
        self.titlepos = self.titleText.get_rect()
        self.titlepos.centerx = self.gs.screen.get_rect().centerx

        #single player title
        self.playerfont = pygame.font.Font("media/fonts/Starjedi.ttf", 36)
        self.player1Text = self.playerfont.render("Single Player", 1, (255, 0, 0))
        self.player1pos = self.player1Text.get_rect()
        self.player1pos.centerx = self.gs.screen.get_rect().centerx
        self.player1pos.y = 165

        #multiplayer title
        self.player2Text = self.playerfont.render("Two Players", 1, (255, 0, 0))
        self.player2pos = self.player2Text.get_rect()
        self.player2pos.centerx = self.gs.screen.get_rect().centerx
        self.player2pos.y = 265

        #instructions title
        self.instructionText = self.playerfont.render("instructions", 1, (255, 255, 255))
        self.instpos = self.instructionText.get_rect()
        self.instpos.centerx = self.gs.screen.get_rect().centerx
        self.instpos.y = 365

        #host/join
        self.hostText = self.playerfont.render("host game", 1, (255, 255, 255))
        self.hostPos = self.hostText.get_rect()
        self.hostPos.centerx = self.gs.screen.get_rect().width / 3
        self.hostPos.y = 265

        self.joinText = self.playerfont.render("join game", 1, (255, 255, 255))
        self.joinPos = self.joinText.get_rect()
        self.joinPos.centerx = 2* self.gs.screen.get_rect().width / 3
        self.joinPos.y = 265

        #blit text elements to screen
        self.gs.screen.blit(self.titleText, self.titlepos)
        self.gs.screen.blit(self.player1Text, self.player1pos)
        self.gs.screen.blit(self.player2Text, self.player2pos)
        self.gs.screen.blit(self.instructionText, self.instpos)

        pygame.display.flip()

    def title(self):
        print "TITLE SCREEN"
        #set up game title
        self.imperial_music = pygame.mixer.Sound("media/audio/imperialMarch.wav")
        #loop to wait for clicks
        #while title running variable
          #variable to keep track of when title options should be running
        while self.titleRunning:
            #self.imperial_music.play()
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
                        #if event.button == 1: should do same thing
                        #if mouse pos is in single player box, get ship selection ready
                        if self.player1pos.collidepoint(mouse_x, mouse_y):
                            print "First option pressed"
                            self.gs.screen.fill(self.gs.black)
                            #self.imperial_music.stop()
                            selection_screen = ShipSelect(self.gs)
                            selection_screen.ship_select()
                            #make second 2 options disappear, show ship options as new buttons
                        #if mouse pos is in multiplayer box, wait for connection (?)
                        if self.player2pos.collidepoint(mouse_x, mouse_y):
                            self.connections = not self.connections
                            self.gs.screen.fill(self.gs.black)
                            #Add networking elements here
                        #if mouse pos is in instructions box, open instructions page
                        if self.instpos.collidepoint(mouse_x, mouse_y):
                            #bring up a new instructions screen
                            print "instructions options pressed"
                            self.gs.screen.fill(self.gs.black)
                            instruction_screen = Instructions(self.gs)
                            instruction_screen.readInstructions()
                            #self.titleRunning = False
                        if self.hostPos.collidepoint(mouse_x, mouse_y) and self.connections:
                            selection_screen = ShipSelect(self.gs)
                            selection_screen.ship_select()
                            self.gs.HOST = 1
                        elif self.joinPos.collidepoint(mouse_x, mouse_y) and self.connections:
                            print "NOT HOST"
                            self.gs.HOST = 2
                            self.titleRunning = False

            self.gs.screen.fill(self.gs.black)
            self.gs.screen.blit(self.titleText, self.titlepos)
            if not self.connections:
                self.gs.screen.blit(self.player1Text, self.player1pos)
                self.gs.screen.blit(self.player2Text, self.player2pos)
                self.gs.screen.blit(self.instructionText, self.instpos)
            else:
                self.gs.screen.blit(self.hostText, self.hostPos)
                self.gs.screen.blit(self.joinText, self.joinPos)

            pygame.display.flip()
        
