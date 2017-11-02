import pygame
import os
import collections
import glob
import constants
import levelloader
import gui
pygame.init()
class Scene() :
    def __init__(self) :
        self.next=self
    def switchscene(self,scene) :
        self.next=scene
    def handle_event(self,event) :
        pass
    def update(self) :
        pass
    def draw(self,screen,camera) :
        pass
class mainmenu(Scene) :
    def __init__(self) :
        pygame.mixer.music.load("data/music/mainmenu.wav")
        pygame.mixer.music.play(-1)
        Scene.__init__(self)
        self.levels={}
        for level in glob.glob("data/levels/*.lvl") :
            dotfile=level.replace("/",".")
            dotlen=len(dotfile.split("."))
            self.levels[os.path.abspath(level)]=gui.Text(dotfile.split(".")[dotlen-2],(255,255,255),(0,0,255),500,500)
        self.levels=collections.OrderedDict(sorted(self.levels.items()))
        self.pos=0
        self.instructbutton=gui.Button(100,300,pygame.image.load("data/images/instructbutton.png"),self.instructclick,sound=pygame.mixer.Sound("data/sounds/click_instruct.wav"))
        self.upbutton=gui.Button(500,400,pygame.image.load("data/images/upbutton.png"),self.upclick,sound=pygame.mixer.Sound("data/sounds/scroll.wav"))
        self.downbutton=gui.Button(500,600,pygame.image.load("data/images/downbutton.png"),self.downclick,sound=pygame.mixer.Sound("data/sounds/scroll.wav"))
        self.shopbutton=gui.Button(400,500,pygame.image.load("data/images/shopbutton.png"),self.shopclick,sound=pygame.mixer.Sound("data/sounds/click_shop.wav"))
        self.playbutton=gui.Button(600,500,pygame.image.load("data/images/playbutton.png"),self.playclick,sound=pygame.mixer.Sound("data/sounds/click_play.wav"))
    def shopclick(self) :
        self.switchscene(shop())
    def instructclick(self) :
        os.system("open data/instructions.html")
    def upclick(self) :
        if self.pos > 0 :
            self.pos-=1
    def downclick(self) :
        if self.pos < len(self.levels.keys())-1 :
            self.pos+=1
    def playclick(self) :
        self.switchscene(game(levelloader.loadlevel(self.levels.keys()[self.pos])))
    def handle_event(self,event) :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i :
            self.instructbutton.sound.play()
            self.instructclick()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s :
            self.shopbutton.sound.play()
            self.shopclick()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
            self.upbutton.sound.play()
            self.upclick()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN :
            self.downbutton.sound.play()
            self.downclick()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
            self.playbutton.sound.play()
            self.playclick()
        self.playbutton.update(event)
        self.upbutton.update(event)
        self.downbutton.update(event)
        self.instructbutton.update(event)
        self.shopbutton.update(event)
    def update(self) :
        self.levels[self.levels.keys()[self.pos]].update()
    def draw(self,screen,camera) :
        screen.fill((255,255,255))
        screen.blit(pygame.image.load("data/images/player_idle.png"),[200,100])
        self.playbutton.draw(screen,camera)
        self.shopbutton.draw(screen,camera)
        self.instructbutton.draw(screen,camera)
        self.upbutton.draw(screen,camera)
        self.downbutton.draw(screen,camera)
        self.levels[self.levels.keys()[self.pos]].draw(screen,camera)
class shop(Scene) :
    def __init__(self) :
        Scene.__init__(self)
        pygame.mixer.music.load("data/music/shop.wav")
        pygame.mixer.music.play(-1)
        self.purchasesound=pygame.mixer.Sound("data/sounds/purchase.wav")
        self.notenoughsound=pygame.mixer.Sound("data/sounds/notenough.wav")
        self.homebutton=gui.Button(100,300,pygame.image.load("data/images/homebutton.png"),self.homeclick,sound=pygame.mixer.Sound("data/sounds/click_home.wav"))
        self.hpbutton=gui.Button(300,100,pygame.image.load("data/images/powerup.png"),self.hpclick)
        self.hptext=gui.Text("Full Health : 1",(255,0,0),(0,0,255),300,200)
        self.gravbutton=gui.Button(500,100,pygame.image.load("data/images/gravitycoil.png"),self.gravclick)
        self.gravtext=gui.Text("Gravity Coil : 5",(0,0,255),(0,0,0),500,200)
    def hpclick(self) :
        if constants.coins >=1 :
            self.purchasesound.play()
            constants.coins-=1
            constants.player.hp=constants.player.maxhp
        else :
            self.notenoughsound.play()
    def gravclick(self) :
        if constants.coins >= 5 :
            self.purchasesound.play()
            constants.gravitycoils+=1
            constants.coins-=5
        else :
            self.notenoughsound.play()
    def homeclick(self) :
        self.switchscene(mainmenu())
    def handle_event(self,event) :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b :
            self.homebutton.sound.play()
            self.homeclick()
        self.homebutton.update(event)
        self.hpbutton.update(event)
        self.gravbutton.update(event)
    def update(self) :
        self.hptext.update()
        self.gravtext.update()
    def draw(self,screen,camera) :
        screen.fill((255,255,255))
        self.homebutton.draw(screen,camera)
        cointext=gui.Text(str(constants.coins),(160,130,0),(0,0,255),500,300)
        cointext.draw(screen,camera)
        self.hpbutton.draw(screen,camera)
        self.gravbutton.draw(screen,camera)
        self.gravtext.draw(screen,camera)
        self.hptext.draw(screen,camera)
class gameover(Scene) :
    def __init__(self) :
        Scene.__init__(self)
        pygame.mixer.music.load("data/music/gameover.wav")
        pygame.mixer.music.play(-1)
        self.homebutton=gui.Button(200,500,pygame.image.load("data/images/whitehomebutton.png"),self.homeclick,sound=pygame.mixer.Sound("data/sounds/click_home.wav"))
        self.overtext=gui.Text("Game , Over!",(0,0,0),(255,0,0),500,200)
    def handle_event(self,event) :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b :
            self.homebutton.sound.play()
            self.homeclick()
        self.homebutton.update(event)
    def update(self) :
        self.overtext.update()
    def draw(self,screen,camera) :
        screen.fill((0,0,0))
        screen.blit(pygame.image.load("data/images/skull.png"),[500,400])
        self.homebutton.draw(screen,camera)
        self.overtext.draw(screen,camera)
    def homeclick(self) :
        constants.reset()
        self.switchscene(mainmenu())
class won(Scene) :
    def __init__(self) :
        Scene.__init__(self)
        pygame.mixer.music.load("data/music/won.wav")
        pygame.mixer.music.play(-1)
        self.wontext=gui.Text("You , Won!",(0,0,255),(255,0,0),500,500)
        self.cheertimer=15
        self.cheervalue=-1
        self.homebutton=gui.Button(100,500,pygame.image.load("data/images/homebutton.png"),self.homeclick,sound=pygame.mixer.Sound("data/sounds/click_home.wav"))
    def homeclick(self) :
        constants.reset()
        self.switchscene(mainmenu())
    def update(self) :
        self.wontext.update()
    def handle_event(self,event) :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b :
            self.homebutton.sound.play()
            self.homeclick()
        self.homebutton.update(event)
    def draw(self,screen,camera) :
        screen.fill((255,255,255))
        if self.cheertimer == 15 :
            self.cheervalue=-1
            self.playerimage=pygame.image.load("data/images/player_cheer1.png")
        elif self.cheertimer == 0 :
            self.cheervalue=1
            self.playerimage=pygame.image.load("data/images/player_cheer2.png")
        self.cheertimer+=self.cheervalue
        screen.blit(self.playerimage,[500,600])
        self.wontext.draw(screen,camera)
        self.homebutton.draw(screen,camera)
class game(Scene) :
    def __init__(self,objects) :
        Scene.__init__(self)
        pygame.mixer.music.load("data/music/game.wav")
        pygame.mixer.music.play(-1)
        self.objects=objects
        self.homebutton=gui.Button(100,100,pygame.image.load("data/images/homebutton.png"),self.homeclick,sound=pygame.mixer.Sound("data/sounds/click_home.wav"))
        self.jumpsound=pygame.mixer.Sound("data/sounds/jump.wav")
    def homeclick(self) :
        constants.reset()
        self.switchscene(mainmenu())
    def handle_event(self,event) :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b :
            self.homeclick()
            self.homebutton.sound.play()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE :
                constants.player.xspeed,constants.camera.xspeed={5:0,0:5}[constants.player.xspeed],{5:0,0:5}[constants.camera.xspeed]
            if event.key == pygame.K_UP and constants.player.rect.y >= 600 or event.key == pygame.K_UP and constants.player.colliding :
                self.jumpsound.play()
                constants.player.jumptimer=constants.player.maxjump
        self.homebutton.update(event)
    def update(self) :
        if constants.player.dead :
            constants.reset()
            self.switchscene(gameover())
        if constants.gamewon :
            constants.reset()
            self.switchscene(won())
        constants.player.update()
        constants.camera.update()
        for key in self.objects.keys() :
            for object in self.objects[key] :
                object.update()
    def draw(self,screen,camera) :
        screen.fill((0,0,0))
#        pygame.draw.rect(screen,(0,255,0),[0,600+constants.player.rect.height,1000,1000])
#        pygame.draw.rect(screen,(0,0,255),[0,-5,1000,605+constants.player.rect.height])
        constants.player.draw(screen,camera)
        self.homebutton.draw(screen,camera)
        pygame.draw.rect(screen,(255,0,0),[10,10,50*constants.player.hp,10])
        hptext=gui.Text(str(constants.player.hp),(255,0,0),(0,0,0),500,25)
        pygame.draw.rect(screen,(160,130,0),[10,50,20*constants.coins,10])
        cointext=gui.Text(str(constants.coins),(160,130,0),(0,0,255),500,65)
        cointext.update()
        cointext.draw(screen,camera)
        hptext.update()
        hptext.draw(screen,camera)
        screen.blit(pygame.image.load("data/images/gravitycoil.png"),[50,100])
        gravtext=gui.Text(str(constants.gravitycoils),(0,0,255),(255,255,255),50,200)
        gravtext.update()
        gravtext.draw(screen,camera)
        for key in self.objects.keys() :
            for object in self.objects[key] :
                object.draw(screen,camera)
        for bomb in self.objects["bombs"] :
            if bomb.destroyed :
                self.objects["bombs"].remove(bomb)
        for powerup in self.objects["powerups"] :
            if powerup.destroyed :
                self.objects["powerups"].remove(powerup)
        for coin in self.objects["coins"] :
            if coin.destroyed :
                self.objects["coins"].remove(coin)