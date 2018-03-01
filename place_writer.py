from FiveElements import *
from math import copysign

def move (tryblock,firstpos,swap=False,speed=30):
    '''To move a chess to another place and make the animation.

This function needs 3 arguments: tryblock,firstpos,boomit(a boolean)'''

    
    tempObj=posdic[firstpos].chess
    if swap:
        tempObj2=posdic[tryblock].chess
        if posdic[firstpos].type!=posdic[tryblock].type:
            tempObj2.actpic=tempObj2.six_pic if posdic[firstpos].type=='Six'\
                        else tempObj2.eight_pic
    if posdic[firstpos].type!=posdic[tryblock].type:
        tempObj.actpic=tempObj.six_pic if posdic[tryblock].type=='Six'\
                        else tempObj.eight_pic
    if posdic[tryblock].chess!= None:
        posdic[tryblock].chess.alive=False
        posdic[tryblock].chess= None
    posdic[firstpos].chess=None
    def animate(firstpos,tryblock,tempObj):
        flag=True
        oldx,oldy=posdic[firstpos].coords
        newx,newy=posdic[tryblock].coords
        movevecter=Vecter2((newx-oldx),(newy-oldy))
        movevecter.normalize()
        while flag:
            oldx+=copysign(min(abs(speed*movevecter.x),abs(newx-oldx)),movevecter.x)
            oldy+=copysign(min(abs(speed*movevecter.y),abs(newy-oldy)),movevecter.y)
            DISPLAYSURF.blit(background,(0,0))
            DISPLAYSURF.blit(tempObj.actpic,(oldx,oldy))
            time.sleep(0.05)
            drawchess()
            pygame.display.update()
            if oldx==newx and oldy==newy:
                flag=False
        posdic[tryblock].chess=tempObj
    animate(firstpos,tryblock,tempObj)
    if swap:
        animate(tryblock,firstpos,tempObj2)
        #posdic[firstpos].chess=tempObj2
    return
def main():
    setchess()
    hlightflag=None
    cpos=0
    global firstchess
    while True:
        mou=pygame.mouse.get_pos()
        blockinfo=None
        for j in posdic.keys():
            if posdic[j].shape.collide(mou):
                blockinfo=posdic[j]
                hflag=True
##                if blockinfo.chess!= None and blockinfo.chess.whose!= turn:
##                    hflag=False
                cpos=j
                break
        else:
            hflag=False
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    return
            elif event.type==MOUSEBUTTONDOWN and blockinfo!=None\
                 and event.button==1:
                cango=False
                if firstchess != None:#对称改变双方
                   #and blockinfo.chess==None:
                    tryblock=cpos
                    print(cpos)
                    chessinblock=posdic[tryblock].chess
                    swap=False
                    if chessinblock!= None:
                        print('-'*12,chessinblock)
                        swap=True
                    move(tryblock,firstpos,swap)
                    move(55-tryblock,55-firstpos,swap)
                    
                    firstchess=None
                    
                elif firstchess==None and blockinfo.chess!=None:
                    firstchess=blockinfo.chess
                    firstpos=cpos
                    print ('firstchess set')
        DISPLAYSURF.blit(background,(0,0))#画图
        drawchess()
        if hflag:
            DISPLAYSURF.blit(hlightdict[blockinfo.type],blockinfo.coords)
        pygame.display.update()
        fpsClock.tick(FPS)
start()
main()
