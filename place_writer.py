from FiveElements import *

def main():
    def main():
    global turn
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
                    cango= tryblock in posdic[firstpos].cangos
                    boomit=False
                    if blockinfo.chess!= None:
                        if blockinfo.chess.whose!=turn and cango:
                            cango=eatable(firstchess,blockinfo.chess,tryblock)
                            print(cango)
                            if cango:
                                boomit=True
                        elif blockinfo.chess.whose==turn:
                            firstchess=blockinfo.chess
                            firstpos=cpos
                            print ('firstchess set')
                            cango=None
                    if cango:
                        move(tryblock,firstpos,boomit)
                        turn='仙' if turn=='神' else '神'
                        firstchess=None
                    elif cango!=None:
                        firstchess=None
                        firstpos=0
                elif firstchess==None and blockinfo.chess!=None and blockinfo.chess.whose==turn:
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
