#Cody Barron
#PyGame Primer

import sys
#import os
import pygame
from pygame.locals import *
from Player import Player
from Enemy import Enemy, TieFighter, TieBomber, TieInterceptor
from Unit import Unit
from TitleScreen import TitleScreen

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
        #self.tie = TieFighter(self)
        #self.bomber=TieBomber(self)
        
        self.enemies = list()
        self.lazers = list()
        self.explosions = list()
        self.box = list()

        self.fps = 60

    def title(self):
        self.titleScreen = TitleScreen(self)
        self.titleScreen.title()
                    
    def main(self):
        distanceTravelled = 0
        #enter loop
        while True:
            self.clock.tick(self.fps)
            
            #create enemy ships based on distanceTravelled
            if ((distanceTravelled % 5) < 3):
                interceptor=TieInterceptor(self)
                self.enemies.append(interceptor)
            elif (distanceTravelled == 4) or (distanceTravelled == 5):
                tie=TieFighter(self)
                self.enemies.append(tie)
            else:
                self.bomber=TieBomber(self)
                self.enemies.append(bomber)
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
            distanceTravelled = distanceTravelled + 1 #add to distance travelled

            #control enemy ships
            for enemy in self.enemies:
                bomber.tick()
                self.screen.blit(bomber.bomberImage, bomber.bomberRect)
            for tie in self.enemies:
                tie.tick()
                self.screen.blit(tie.tieImage, tie.tieRect)
            for interceptor in self.enemies:
                interceptor.tick()
                self.screen.blit(interceptor.interceptorImage, interceptor.interceptorRect)
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

