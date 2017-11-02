import pygame
import sprites
pygame.init()
def loadlevel(filepath) :
    f=open(filepath,"r+")
    lines=f.readlines()
    f.close()
    objstruct={"spikes":[],"bombs":[],"electricbarriers":[],"lava":[],"rocks":[],"powerups":[],"teleporters":[],"flags":[],"platforms":[],"springboards":[],"clouds":[],"coins":[]}
    for line in lines :
        parsed=line.replace(":","|").split("|")
        if parsed[0] == "spike" :
            objstruct["spikes"].append(sprites.Spike(int(parsed[1])*200,600))
        elif parsed[0] == "bomb" :
            objstruct["bombs"].append(sprites.Bomb(int(parsed[1])*200,600))
        elif parsed[0] == "electricbarrier" :
            objstruct["electricbarriers"].append(sprites.ElectricBarrier(int(parsed[1])*200,600))
        elif parsed[0] == "lava" :
            objstruct["lava"].append(sprites.Lava(int(parsed[1])*200,600))
        elif parsed[0] == "platform" :
            objstruct["platforms"].append(sprites.Platform(int(parsed[1])*200,500))
        elif parsed[0] == "springboard" :
            objstruct["springboards"].append(sprites.Springboard(int(parsed[1])*200,600))
        elif parsed[0] == "teleporter" :
            objstruct["teleporters"].append(sprites.Teleporter(int(parsed[1])*200,600,int(parsed[2])*200))
        elif parsed[0] == "powerup" :
            objstruct["powerups"].append(sprites.Powerup(int(parsed[1])*200,600,int(parsed[2])))
        elif parsed[0] == "rock" :
            objstruct["rocks"].append(sprites.Rock(int(parsed[1])*200,600))
        elif parsed[0] == "flag" :
            objstruct["flags"].append(sprites.Flag(int(parsed[1])*200,600))
        elif parsed[0] == "coin" :
            objstruct["coins"].append(sprites.Coin(int(parsed[1])*200,600,int(parsed[2])))
    return objstruct