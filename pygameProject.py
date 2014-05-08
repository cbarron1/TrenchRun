#Cody Barron & Laura Cronin
#Trench Run

import sys
#import os
import pygame
from pygame.locals import *
from Player import Player
from Enemy import Enemy, TieFighter, TieBomber, TieInterceptor, LaserTurret, ExhaustPort
from Unit import Unit
from TitleScreen import TitleScreen
from GameOver import GameOver
import random
import pickle
from twisted.internet.protocol import Protocol, ClientFactory, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

connections = dict()

class GameHostConn(Protocol):
    def connectionMade(self):
        print "Connection Made"
        reactor.callLater(1.0/60.0, gs.main)

    def dataReceived(self, data):
        #only thing we get from client is key press
        x = pickle.loads(data)
        if x[0] == KEYDOWN:
            print "MOVE PLAYER 2", x[1]
            reactor.callLater(1.0/60.0, gs.player2.onKeyDown, x[1])
        elif x[0] == KEYUP:
            print "STOP MOVING"
            reactor.callLater(1.0/60.0, gs.player2.onKeyUp, x[1])

    def connectionLost(self, reason):
        print "Connection Lost"
        print reason

class GameHostConnFactory(Factory):
    def buildProtocol(self, addr):
        connections['client'] = GameHostConn()
        return connections['client']


class GameClientConn(Protocol):
    def connectionMade(self):
        print "Connected to host"

    def dataReceived(self, data):
        if data == 'gameover':
            print "GAME OVER"
            gameOver_screen = GameOver(gs)
            gameOver_screen.gameResult(0)
        elif data == 'win':
            print "YOU WIN"
            gameOver_screen = GameOver(gs)
            gameOver_screen.gameResult(1)
        else:
            x = pickle.loads(data)
            gs.client_blit_list = x

    def connectionLost(self, reason):
        print "Connection Lost"
        print reason

class GameClientConnFactory(ClientFactory):
    def buildProtocol(self,addr):
        connections['host'] = GameClientConn()
        return connections['host']

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
        self.player2 = Player(2, self)
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

        ### LOAD ALL IMAGES SO CLIENT HAS ACCESS TO THEM ###
        #background image
        self.background_image = self.background.image
        #player ship images
        self.x_image = pygame.image.load("media/Rebel/sw_xwing.png")
        self.x_image = pygame.transform.scale(self.x_image, (45, 39))
        self.x_image = pygame.transform.rotate(self.x_image, -90)
        self.s_image = pygame.image.load("media/Rebel/seraph.png")
        self.s_image = pygame.transform.scale(self.s_image, (80, 60))
        self.s_image = pygame.transform.rotate(self.s_image, -90)
        self.f_image = pygame.image.load("media/Rebel/falcon.png")
        self.f_image = pygame.transform.scale(self.f_image, (80, 105))
        self.f_image = pygame.transform.rotate(self.f_image, -90)
        #enemy ship images
        self.tie_image = pygame.image.load("media/Empire/sw_tief.png")
        self.tie_image = pygame.transform.rotate(self.tie_image, -90)
        self.bomber_image = pygame.image.load("media/Empire/tie_bomber.png")
        self.bomber_image = pygame.transform.rotate(self.bomber_image, 90)
        self.interceptor_image = pygame.image.load("media/Empire/tie_interceptor.png")
        self.interceptor_image = pygame.transform.rotate(self.interceptor_image, 90)
        #turret related images
        self.turret_image = pygame.image.load("media/turret.png")
        self.turret_image = pygame.transform.rotate(self.turret_image, 210)
        self.turret_image = pygame.transform.scale(self.turret_image, (70,140))
        self.laser_2_image=pygame.image.load("media/Laser_Beam.png")
        self.laser_2_image=pygame.transform.scale(self.laser_2_image, (70,400))
        #laser image
        self.laser_image = pygame.image.load("media/laser.png")

        self.fps = 60

        self.distanceTravelled = 0
        self.bombers = 0
        self.ties = 0
        self.interceptors = 0
        self.toGo = 0
        self.success = 1

        self.HOST = 3

        self.client_blit_list = list()

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

        ######################################################
        ### ALL LISTS NEEDED FOR BLITTING OF CLIENT PLAYER ###
        c_backgrounds = list()
        c_players = list() # will have types as well as rects
        c_ties = list()
        c_bombers = list()
        c_interceptors = list()
        c_turrets = list()
        c_tlasers = list()
        c_lasers = list()
        c_explosions = list()
        ######################################################

        #enter loop
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
                reactor.stop()
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    reactor.stop()
                    pygame.quit()
                    return
                self.player.onKeyDown(event.key)
            elif event.type == KEYUP:
                self.player.onKeyUp(event.key)

        self.player.tick()
        self.player2.tick()

        self.screen.fill(self.black)
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.background2.image, self.background2.rect)

        c_backgrounds.append(self.background.rect)
        c_backgrounds.append(self.background2.rect)

        self.background.tick()
        self.background2.tick()

        #print len(self.enemies)
         
        if (self.distanceTravelled % 50) == 0:
            self.gameTime = self.distanceTravelled / 50
            self.toGo = 200-(self.gameTime) #may want to speed up this timing
            #print gameTime
        self.distanceTravelled = self.distanceTravelled + 1 #add to distance travelled
            
        #control enemy ships
        for enemy in self.enemies:
            if enemy.alive == False or enemy.rect.x < 0:
                self.enemies.remove(enemy)
                continue
            enemy.tick()
            self.screen.blit(enemy.image, enemy.rect)
            if enemy.shipType == 1:
                c_interceptors.append(enemy.rect)
            elif enemy.shipType == 2:
                c_ties.append(enemy.rect)
            elif enemy.shipType == 3:
                c_bombers.append(enemy.rect)
            elif enemy.shipType== 4:#the enemy is a laser turret
                self.screen.blit(enemy.laserImage, enemy.laserRect)
                c_turrets.append(enemy.rect)
                c_tlasers.append(enemy.laserRect)
            #check collision with player
            if enemy.rect.colliderect(self.player.rect):
                enemy.alive = False
                self.player.hp -= 1
            if enemy.rect.colliderect(self.player2.rect):
                enemy.alive = False
                self.player2.hp -= 1

        for lazer in self.lazers:
            lazer.tick()
            self.screen.blit(lazer.image, lazer.rect)
            c_lasers.append(lazer.rect)
            if lazer.rect.x > self.width or lazer.rect.y > self.height or lazer.rect.x < 0 or lazer.rect.y < 0:
                self.lazers.remove(lazer)

        for explosion in self.explosions:
            explosion.tick()
            if explosion.exploding:
                self.screen.blit(explosion.image, explosion.rect)
                c_explosions.append(explosion.rect)
            else:
                self.explosions.remove(explosion)

        if self.player.hp <= 0:
            self.screen.fill(self.black)
            gameOver_screen = GameOver(self)
            gameOver_screen.gameResult(0)
        self.screen.blit(self.player.image, self.player.rect)
        if self.HOST is not 3:
            self.screen.blit(self.player2.image, self.player2.rect)

        c_players.append([self.player.player_type, self.player.rect])
        c_players.append([self.player2.player_type, self.player2.rect])

        coords_to_send = list()
        coords_to_send.append(c_backgrounds)
        coords_to_send.append(c_players)
        coords_to_send.append(c_ties)
        coords_to_send.append(c_bombers)
        coords_to_send.append(c_interceptors)
        coords_to_send.append(c_turrets)
        coords_to_send.append(c_tlasers)
        coords_to_send.append(c_lasers)
        coords_to_send.append(c_explosions)

        if self.HOST is not 3:
            s = pickle.dumps(coords_to_send)
            connections['client'].transport.write(str(s))

        #Navigation Computer graphic--turn off when nearing target!
        if self.toGo == 10:
            self.navSound = pygame.mixer.Sound("media/audio/computerOff.wav")
            self.navSound.play()
        if self.toGo > 0 :### change this back!
            self.screen.blit(self.computerImage, self.compRect)
            toGoStr = str(self.toGo)
            self.compText = self.navCompFont.render(toGoStr, 1, (255, 0, 0))
            self.compTextPos = self.compText.get_rect()
            self.compTextPos.centerx = 480
            self.compTextPos.centery = 530 #?
            self.screen.blit(self.compText, self.compTextPos)
        #Create Exhaust Port if toGo < 5
        if self.toGo == 5:
            target=ExhaustPort(self)
            self.screen.blit(target.image, target.rect)
        if self.toGo < 5 and target.rect.x < 0: #if you passed the target and didn't hit it
            self.screen.fill(self.black)
            connections['client'].transport.write('gameover')
            gameOver_screen = GameOver(self)
            gameOver_screen.gameResult(0)
        if self.toGo < 5:
            self.screen.blit(target.image, target.rect)
            target.tick()
            if target.alive == False:
                self.screen.fill(self.black)
                connections['client'].transport.write('win')
                gameOver_screen = GameOver(self)
                gameOver_screen.gameResult(1)

        pygame.display.flip()
        reactor.callLater(1.0/60.0, self.main)

    def clientMain(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                reactor.stop()
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                event_info = [KEYDOWN, event.key]
                s = pickle.dumps(event_info)
                connections['host'].transport.write(str(s))
                #connections['host'].transport.write(str(event.key))
            elif event.type == KEYUP:
                event_info = [KEYUP, event.key]
                s = pickle.dumps(event_info)
                connections['host'].transport.write(str(s))
        self.screen.fill(self.black)
        self.client_blit()
        pygame.display.flip()
        reactor.callLater(1.0/60.0, self.clientMain)

    def client_blit(self):
        #print self.client_blit_list
        if bool(self.client_blit_list):
            for background_rect in self.client_blit_list[0]:
                self.screen.blit(self.background_image, background_rect)
            for player in self.client_blit_list[1]:
                if player[0] == 1:
                    self.screen.blit(self.x_image, player[1])
                elif player[0] == 2:
                    self.screen.blit(self.s_image, player[1])
                elif player[0] == 3:
                    self.screen.blit(self.f_image, player[1])
            for tie_rect in self.client_blit_list[2]:
                self.screen.blit(self.tie_image, tie_rect)
            for bomber_rect in self.client_blit_list[3]:
                self.screen.blit(self.bomber_image, bomber_rect)
            for interceptor_rect in self.client_blit_list[4]:
                self.screen.blit(self.interceptor_image, interceptor_rect)
            for turret_rect in self.client_blit_list[5]:
                self.screen.blit(self.turret_image, turret_rect)
            for tlaser_rect in self.client_blit_list[6]:
                self.screen.blit(self.laser_2_image, tlaser_rect)
            for laser_rect in self.client_blit_list[7]:
                self.screen.blit(self.laser_image, laser_rect)

if __name__ == '__main__':
    gs = GameSpace()
    gs.title()
    if gs.HOST == 1:
        reactor.listenTCP(9100, GameHostConnFactory())
    elif gs.HOST == 2:
        #read input from command line
        hostname = str(raw_input("Enter Host Address: "))
        reactor.connectTCP(hostname, 9100, GameClientConnFactory())
        reactor.callLater(1.0/60.0, gs.clientMain)
    elif gs.HOST == 3:
        gs.main()
    reactor.run()

            
            

