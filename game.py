import pygame
import sys
import lib
pygame.init()
screen=pygame.display.set_mode((1000,1000))
clock=pygame.time.Clock()
currentscene=lib.scenes.mainmenu()
while True :
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.KEYDOWN and event.key == pygame.K_q :
            pygame.quit()
            sys.exit()
        currentscene.handle_event(event)
    currentscene.update()
    currentscene.draw(screen,lib.constants.camera)
    currentscene=currentscene.next
    pygame.display.update()
    clock.tick(60)