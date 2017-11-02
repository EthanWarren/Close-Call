import pygame
import constants
pygame.init()
damagesound=pygame.mixer.Sound("data/sounds/damage.wav")
class Player() :
    def __init__(self,x,y) :
        self.landsound=pygame.mixer.Sound("data/sounds/land.wav")
        self.playedland=True
        self.walkvalue=0
        self.walktimer=15
        self.colliding=False
        self.dead=False
        self.maxhp=10
        self.hp=self.hp=self.maxhp
        self.maxjump=50
        self.jumptimer=0
        self.falling=True
        self.image=pygame.image.load("data/images/player_idle.png")
        self.rect=self.image.get_rect(x=x,y=y)
        self.xspeed=0
        self.yspeed=0
    def update(self) :
        self.rect.x+=self.xspeed
        self.rect.y+=self.yspeed
        if self.rect.y >= 600 and not self.playedland :
            self.landsound.play()
            self.playedland=True
        if self.rect.y < 600 :
            self.playedland=False
        if self.jumptimer <= 0 and self.falling and self.rect.y < 600 :
            self.image=pygame.image.load("data/images/player_fall.png")
            self.yspeed=8
        else :
            self.yspeed=0
        if self.jumptimer > 0 :
            self.image=pygame.image.load("data/images/player_jump.png")
            self.jumptimer-=1
            if constants.gravitycoils > 0 :
                self.yspeed=-8
            else :
                self.yspeed=-6
        if self.walktimer == 15 and self.xspeed > 0 :
            self.walkvalue=-1
            self.image=pygame.image.load("data/images/player_walk1.png")
        elif self.walktimer == 0 and self.xspeed > 0 :
            self.walkvalue=1
            self.image=pygame.image.load("data/images/player_walk2.png")
        elif self.xspeed == 0 and self.jumptimer == 0 and self.rect.y >= 600 :
            self.image=pygame.image.load("data/images/player_idle.png")
        if self.xspeed > 0 :
            self.walktimer+=self.walkvalue
        if self.hp <=0 :
            self.dead=True
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Spike() :
    def __init__(self,x,y) :
        self.image=pygame.image.load("data/images/spike.png")
        self.sound=pygame.mixer.Sound("data/sounds/spike.wav")
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        if constants.player.rect.colliderect(self.rect) :
            self.sound.play()
            damagesound.play()
            constants.player.hp-=2
            constants.player.rect.x-=200
            constants.camera.x-=200
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Bomb() :
    def __init__(self,x,y) :
        self.image=pygame.image.load("data/images/bomb.png")
        self.sound=pygame.mixer.Sound("data/sounds/bomb.wav")
        self.rect=self.image.get_rect(x=x,y=y)
        self.destroyed=False
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            self.sound.play()
            damagesound.play()
            constants.player.hp-=5
            self.destroyed=True
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Rock() :
    def __init__(self,x,y) :
        self.image=pygame.image.load("data/images/rock.png")
        self.sound=pygame.mixer.Sound("data/sounds/rock.wav")
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        if constants.player.rect.colliderect(self.rect) :
            self.sound.play()
            constants.player.rect.x-=200
            constants.camera.x-=200
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Lava() :
    def __init__(self,x,y) :
        self.image=pygame.image.load("data/images/lava.png")
        self.sound=pygame.mixer.Sound("data/sounds/lava.wav")
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        if constants.player.rect.colliderect(self.rect) :
            self.sound.play()
            damagesound.play()
            constants.player.dead=True
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Platform() :
    def __init__(self,x,y) :
        self.occupied=False
        self.image=pygame.image.load("data/images/platform.png")
        self.sound=pygame.mixer.Sound("data/sounds/platform.wav")
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            constants.player.colliding=True
            constants.player.falling=False
            if not self.occupied :
                self.occupied=True
                self.sound.play()
        elif not self.occupied and constants.player.colliding :
            self.occupied=False
        else :
            constants.player.colliding=False
            constants.player.falling=True
            self.occupied=False
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Springboard() :
    def __init__(self,x,y) :
        self.occupied=False
        self.image=pygame.image.load("data/images/springboard.png")
        self.sound=pygame.mixer.Sound("data/sounds/springboard.wav")
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            constants.player.colliding=True
            constants.player.falling=False
            if not self.occupied :
                self.sound.play()
                self.occupied=True
            constants.player.jumptimer=60
        elif not self.occupied and constants.player.colliding :
            self.occupied=False
        else :
            self.occupied=False
            constants.player.falling=True
            constants.player.colliding=False
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class ElectricBarrier() :
    def __init__(self,x,y) :
        self.image=pygame.image.load("data/images/electricbarrier.png")
        self.sound=pygame.mixer.Sound("data/sounds/electricbarrier.wav")
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            self.sound.play()
            damagesound.play()
            constants.player.hp-=5
            constants.player.rect.x+=400
            constants.camera.x+=400
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Teleporter() :
    def __init__(self,x,y,destpos) :
        self.image=pygame.image.load("data/images/teleporter.png")
        self.sound=pygame.mixer.Sound("data/sounds/teleporter.wav")
        self.rect=self.image.get_rect(x=x,y=y)
        self.destpos=destpos
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            self.sound.play()
            constants.player.rect.x=self.destpos
            constants.camera.x=constants.player.rect.x-500
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Powerup() :
    def __init__(self,x,y,amount) :
        self.image=pygame.image.load("data/images/powerup.png")
        self.sound=pygame.mixer.Sound("data/sounds/powerup.wav")
        self.destroyed=False
        self.rect=self.image.get_rect(x=x,y=y)
        self.amount=amount
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            self.sound.play()
            constants.player.hp+=self.amount
            self.destroyed=True
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Flag() :
    def __init__(self,x,y) :
        self.image=pygame.image.load("data/images/flag.png")
        self.sound=pygame.mixer.Sound("data/sounds/flag.wav")
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            self.sound.play()
            constants.gamewon=True
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])
class Coin() :
    def __init__(self,x,y,amount) :
        self.amount=amount
        self.sound=pygame.mixer.Sound("data/sounds/coin.wav")
        self.image=pygame.image.load("data/images/coin.png")
        self.rect=self.image.get_rect(x=x,y=y)
        self.destroyed=False
    def update(self) :
        if self.rect.colliderect(constants.player.rect) :
            self.sound.play()
            constants.coins+=self.amount
            self.destroyed=True
    def draw(self,screen,camera) :
        screen.blit(self.image,[self.rect.x-camera.x,self.rect.y-camera.y])