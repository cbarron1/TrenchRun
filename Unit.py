import pygame

class Unit(pygame.sprite.Sprite):
    def __init__(self, gs, location, type, team):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.x, self.y = location

        self.type = type
        self.team = team
        if self.team == 1:
            print "Rebels"
            if self.type == 1:
                print "X-Wing"
                self.hp = 10
                self.image = pygame.image.load("media/Rebel/sw_xwing.png")
                self.rect = self.image.get_rect(x=self.x,y=self.y)
            elif self.type == 2:
                print "Y-Wing"
                self.hp = 15
                self.image = pygame.image.load("media/Rebel/sw_ywing.png")
                self.rect = self.image.get_rect(x=self.x,y=self.y)
            elif self.type == 3:
                print "A-Wing"
                self.hp = 5
                self.image = pygame.image.load("media/Rebel/sw_awing.png")
                self.rect = self.image.get_rect(x=self.x,y=self.y)
            elif self.type == 4:
                print "Falcon"
                self.hp = 20
                self.image = pygame.image.load("media/Rebel/falcon.png")
                self.rect = self.image.get_rect(x=self.x,y=self.y)
            elif self.type == 5:
                print "MonCal Cruiser"
                self.hp = 30
                self.image = pygame.image.load("media/Rebel/mc80_liberty.png")
                self.rect = self.image.get_rect(x=self.x,y=self.y)
            elif self.type == 6:
                print "Home One"
                self.hp = 50
                self.image = pygame.transform.scale(pygame.image.load("media/Rebel/home_one_big.png"), (58,240))
                self.image = pygame.transform.rotate(self.image,-90)
                self.rect = self.image.get_rect(x=self.x,y=self.y)
        elif self.team == 2:
            print "Empire"
            if self.type == 1:
                print "TIE Fighter"
                self.hp = 10
            elif self.type == 2:
                print "TIE Bomber"
                self.hp = 20
            elif self.type == 3:
                print "TIE Interceptor"
                self.hp = 5
            elif self.type == 4:
                print "Star Destroyer"
                self.hp = 35
            elif self.type == 5:
                print "Executor"
                self.hp = 60

        print self.hp
