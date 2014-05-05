import pygame
from pygame.locals import *
import sys
from ShipSelect import ShipSelect
from Instructions import Instructions

class TitleScreen:
    def __init__(self, gs):
        self.gs = gs
        self.titleRunning = True
        
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
            self.imperial_music.play()
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
                            self.imperial_music.stop()
                            selection_screen = ShipSelect(self.gs)
                            selection_screen.ship_select()
                            #make second 2 options disappear, show ship options as new buttons
                        #if mouse pos is in multiplayer box, wait for connection (?)
                        if self.player2pos.collidepoint(mouse_x, mouse_y):
                            print "Waiting for connection"
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

            self.gs.screen.fill(self.gs.black)
            self.gs.screen.blit(self.titleText, self.titlepos)
            self.gs.screen.blit(self.player1Text, self.player1pos)
            self.gs.screen.blit(self.player2Text, self.player2pos)
            self.gs.screen.blit(self.instructionText, self.instpos)

            pygame.display.flip()
        
