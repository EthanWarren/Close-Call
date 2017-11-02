import pygame
pygame.init()
class Camera() :
    def __init__(self,x,y) :
        self.x=x
        self.y=y
        self.xspeed=0
        self.yspeed=0
    def update(self) :
        self.x+=self.xspeed
        self.y+=self.yspeed
class Button() :
    def __init__(self,x,y,image,onclick,sound=None) :
        self.image=image
        self.rect=self.image.get_rect(x=x,y=y)
        self.onclick=onclick
        self.sound=sound
    def update(self,event) :
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()) :
            if self.sound != None :
                self.sound.play()
            self.onclick()
    def draw(self,screen,camera) :
        screen.blit(self.image,self.rect)
class Text() :
    def __init__(self,text,textcolor,backgroundcolor,x,y) :
        self.text=text
        self.font=pygame.font.SysFont(None,32)
        self.image=self.font.render(text,True,textcolor,backgroundcolor)
        self.rect=self.image.get_rect(x=x,y=y)
    def update(self) :
        pass
    def draw(self,screen,camera) :
        screen.blit(self.image,self.rect)