from FiveElements import chess_board,get_input,Chess,Vecter2
from FiveElements import DISPLAYSURF,hlight_pic
from math import copysign
import pygame
from pygame.locals import *
from random import random
import loader#,putin
from os import _exit

loader.init('place')
stra_dict=loader.read_db()
firstchess= None
firstpos=0
fpsClock=pygame.time.Clock()
attribute={'金':1,
         '水':4,
         '木':2,
         '火':5,
         '土':3,
         '王':11}
print(stra_dict)
MOVING=[]
NAME=''

def setchess():
    global NAME
    NAME=get_input(items=[i for i in stra_dict.keys()])
##    name=input('Please enter the name of map to edit:')
    poses=stra_dict.get(NAME,loader.default_place['默认'])
    atris=list(attribute.keys())[:-1]
    for i in range (5):
        for j in (0,1):
            #print(sdict[i])
            Chess(atris[i]+'神',poses[i][j])
            Chess(atris[i]+'仙',55-poses[i][j])
    Chess('王神',poses[5][0])
    Chess('王仙',55-poses[5][0])
def move (tryblock,firstpos,swap=False,speed=30):
    '''To move a chess to another place and make the animation.

This function needs 3 arguments: tryblock,firstpos,boomit(a boolean)'''

    
    tempObj=chess_board[firstpos].chess
    if swap:
        tempObj2=chess_board[tryblock].chess
        if chess_board[firstpos].n!=chess_board[tryblock].n:
            tempObj2.actpic=tempObj2.pics[chess_board[firstpos].n]
    if chess_board[firstpos].n!=chess_board[tryblock].n:
        tempObj.actpic=tempObj.pics[chess_board[tryblock].n]
    if chess_board[tryblock].chess!= None:
        chess_board[tryblock].chess.alive=False
        chess_board[tryblock].chess= None
    chess_board[firstpos].chess=None
    def animate(firstpos,tryblock,tempObj):
        oldx,oldy=chess_board[firstpos].topleft
        newx,newy=chess_board[tryblock].topleft
        movevecter=Vecter2((newx-oldx),(newy-oldy))
        movevecter.normalize()
        while True:
            oldx+=copysign(min(abs(speed*movevecter.x),abs(newx-oldx)),movevecter.x)
            oldy+=copysign(min(abs(speed*movevecter.y),abs(newy-oldy)),movevecter.y)
            DISPLAYSURF.blit(tempObj.actpic,(oldx,oldy))
            #time.sleep(0.05
            if oldx==newx and oldy==newy:
                break
            yield None
        chess_board[tryblock].chess=tempObj
    MOVING.append(animate(firstpos,tryblock,tempObj))
    if swap:
        MOVING.append(animate(tryblock,firstpos,tempObj2))
        #posdic[firstpos].chess=tempObj2
    return

def save_stra():
    filt=lambda c:c.whose=='神' and c.block!=None
    chesses=list(filter(filt,chess_board.all_chess))
    chesses=list(map(lambda c:(c.block.i,c),chesses))
    
##    filt=lambda b:b[1].chess!=None and b[1].chess.whose=='神'
##    chesses=list(filter(filt,posdic.items()))
##    chesses=list(map(lambda x:(x[0],x[1].chess),chesses))
    poses={k:[] for k,v in attribute.items()}
    print(poses)
    if len(chesses)!=11:
        return
    for k,v in chesses:
        poses[v.name[0]].append(k)
        print(k,v)
    poses['王'].append(0)
    poses=list(map(tuple,poses.values()))
    #name=input('Please input your map name:')
    stra_dict[NAME]=poses
    print(NAME,poses,stra_dict)
    loader.write_db(stra_dict,mode='w')
    for i in chess_board:
        i.chess=None
    setchess()
def hflag_animate(_blockinfo):
    #print('pre',_blockinfo)
    yield None
    #print('then',_blockinfo)
    DISPLAYSURF.blit(hlight_pic[_blockinfo.n],_blockinfo.topleft)
    
def move_animate():
    global FPS
    #DISPLAYSURF.blit(background,(0,0))
    chess_board.draw()
    if MOVING!=[]:
        removes=[]
        FPS=30
        for i in MOVING[:]:
            try:
                next(i)
            except StopIteration:
                MOVING.remove(i)
                #removes.append(i)
##        for i in removes:
##            MOVING.remove(i)
        pygame.display.update()
##        if random()>0.7:
##            print(removes)
    FPS=10
def main():
    #setchess()
    #DISPLAYSURF.blit(background,(0,0))#画图
    chess_board.draw()
    cpos=0
    event=pygame.event.Event(MOUSEMOTION,{'pos':pygame.mouse.get_pos()})
    pygame.event.post(event)
    global firstchess
    while True:
        move_animate()
        mou=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEMOTION:
                blockinfo = None
                print(event.pos)
                p = chess_board.board.collide(event.pos)
                if p is not None:
                    cpos = chess_board.board.coord_to_num(p)
                    blockinfo = chess_board[cpos]
                    #print(blockinfo)
                    hflag = True
                else:
                    hflag=False
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    return
                if len(MOVING)<=1:
                    print(MOVING)
                    if event.key==K_s:
                        save_stra()
                    if event.key==K_d:
                        for i in posdic.values():
                            i.chess=None
                        setchess()
            elif event.type==MOUSEBUTTONDOWN and blockinfo!=None\
                 and event.button==1:
                cango=False
                tryblock=cpos
                print(cpos)
                chessinblock=chess_board[tryblock].chess
                if firstchess != None and chessinblock != firstchess:#对称改变双方
                   #and blockinfo.chess==None:
                    swap=False
                    if firstpos+tryblock!=55:
                        if chessinblock!= None :
                            print('-'*12,chessinblock)
                            swap=True
                        move(tryblock,firstpos,swap)
                        move(55-tryblock,55-firstpos,swap)
                    else:
                        move(tryblock,firstpos,True)
                    firstchess=None
                    
                elif firstchess==None and blockinfo.chess!=None:
                    firstchess=blockinfo.chess
                    firstpos=cpos
                    print ('firstchess set')
##        DISPLAYSURF.blit(background,(0,0))#画图
##        drawchess()
        if hflag:
            MOVING.append(hflag_animate(blockinfo))
##            DISPLAYSURF.blit(hlightdict[blockinfo.type],blockinfo.coords)
        pygame.display.update()
        fpsClock.tick(FPS)
if __name__=='__main__':
    #chess_board=ChessBoard(DISPLAYSURF)
    setchess()
    print(chess_board.all_chess)
    main()

