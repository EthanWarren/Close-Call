import pygame
import os
import gui
import sprites
pygame.init()
gamewon=False
player=sprites.Player(500,600)
camera=gui.Camera(0,0)
coins=0
gravitycoils=0
def reset() :
    global gamewon
    global gravitycoils
    global player
    global camera
    if player.dead :
        player.hp=player.maxhp
        if gravitycoils > 0 :
            gravitycoils-=1
        player.dead=False
    player.rect.x=500
    player.rect.y=600
    player.xspeed=0
    player.yspeed=0
    player.walkvalue=0
    player.walktimer=15
    camera=gui.Camera(0,0)
    gamewon=False