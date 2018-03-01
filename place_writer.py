from FiveElements import *

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
                    move(tryblock,firstpos)
                    move(55-tryblock,55-firstpos)
                    if chessinblock!= None:
                        print('-'*12,chessinblock)
                        move(firstpos,tryblock)
                        move(55-firstpos,55-tryblock)
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
