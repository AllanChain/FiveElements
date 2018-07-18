#*_* coding:utf-8 *_*
import pygame,time,math,poly,chessdrawer
import loader,putin
from pygame.locals import*
from os import _exit

pygame.init()
DISPLAYSURF=pygame.display.set_mode((1024,650),0,32)
pygame.display.set_caption('Fighting...')
loader.init('color')
style=loader.stra_to_color(loader.read_db())['default']
turn='神'
FPS=5
fpsClock=pygame.time.Clock()
NAME=''
firstchess= None
firstpos=0
attribute={'金':1,
         '水':4,
         '木':2,
         '火':5,
         '土':3,
         '王':11}
class Block:
    def __init__(self,chessboard,i):
        self.chessboard,self.i=chessboard,i
        self.g,self.num=self.chessboard.board.get_group(i)
        self.n=self.g.n
    @property
    def chess(self):
        return self.chessboard._posdict[self.i]
    @chess.setter
    def chess(self,ch):
        self.chessboard._posdict[self.i]=ch
    @property
    def topleft(self):
        return self.chessboard.board.get_pos_by_num(self.i)
class ChessBoard:
    def __init__(self,DIS):
        global background,hlight_pic
        self._posdict={n:None for n in range(56)}
        self.DIS=DIS
        self.all_chess=[]
        files_image_background = 'backimage.jpg'
        files_sound_boomsound ='Boomsound.mp3'
        background=pygame.image.load(files_image_background) .convert_alpha()
        #boomsound = pygame.mixer.Sound(files_sound_boomsound)
        
        #Initializing the high light surfaces
        hlight_pic=dict()
        hlight_color=(0,200,200,100)
        for n in (6,8):
            t_poly=poly.poly(n=n,topleft=(0,0),size=40)
            highlight=pygame.surface.Surface(t_poly.rect.iwh).convert_alpha()
            highlight.fill((0,0,0,0))
            pygame.draw.polygon(highlight,hlight_color,t_poly.points,0)
            hlight_pic[n]=highlight
        #Setting up blocks
        XMAR=2
        YMAR=40
        size=40
        GAP=size
        base1=poly.poly(n=8,size=size,topleft=(XMAR,YMAR))
        base2=poly.poly(n=6,size=size,topleft=(9.2*size+XMAR+GAP,YMAR+0.35*size))
        base3=poly.poly(n=8,size=size,topleft=(XMAR+14.2*size+XMAR+2*GAP,YMAR))
        self.board=poly.ComboGroup((poly.PolyGroup(base_poly=base1,EVEN=4,ODD=3,line=5),\
                              poly.PolyGroup(base_poly=base2,EVEN=7,ODD=6,line=3),\
                              poly.PolyGroup(base_poly=base3,EVEN=4,ODD=3,line=5)))
        self.board.set_special_neibors({14:(18,19),
                                        15:(19,20,21),
                                        16:(21,22,23),
                                        17:(3,24)})
        chess_pics={}
        chessurf=pygame.image.load('Eight.png')
        chess_pics[8]=pygame.transform.scale(chessurf,base1.rect.iwh)
        chessurf=pygame.image.load('Six.png')
        chess_pics[6]=pygame.transform.scale(chessurf,base2.rect.iwh)
        for p in self.board:
            background.blit(chess_pics[p.n],p.topleft)

    def __getitem__(self,n):
        return Block(self,n)
    def draw(self):
        self.DIS.blit(background,(0,0))
        for chess in self.all_chess:
            self.DIS.blit(chess.actpic,chess.block.topleft)
        #pygame.display.update()

chess_board=ChessBoard(DISPLAYSURF)
class Chess:
    '''Include every chess.'''
    def __init__(self,name,position):
        '''This function needs 2 arguments: name,position .'''
        self.name=name
        self.whose=name[-1:]
        self.alive=True
        self.position=position
        self.pics=getpic(name)
        self.actpic=self.pics[chess_board[position].n]
        #self.attribute
        chess_board[position].chess=self
        self.block=chess_board[position]
        chess_board.all_chess.append(self)
        #xypos=posdic[position]
        #DISPLAYSURF.blit(self.actpic,posdic[position].coords)
    def __str__(self):
        return self.name

class Vecter2:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.dis=math.sqrt(x*x+y*y)
    def normalize(self):
        self.x=self.x/self.dis
        self.y=self.y/self.dis

def getpic(name):
    whose=name[-1:]
    myname=name[:-1]
    sty=style[myname]
    #print(sty)
    return{8:chessdrawer.generate(myname,whose,8,sty),\
           6:chessdrawer.generate(myname,whose,6,sty)}


def get_input(items):
    global NAME
    mylister=putin.Lister(items,DISPLAYSURF,pos=(0,0),max_list=4)
    while True:
        DISPLAYSURF.blit(background,(0,0))
        mylister.update()
        pygame.display.update()
        for event in pygame.event.get():
            item=mylister.react(event)
            if event.type==QUIT:
                pygame.quit()
                _exit(0)
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    _exit(0)
            if item!=None:
                NAME=item
                return NAME
            time.sleep(0.2)


def setchess():
    loader.init('place')
    sdict=loader.read_db()
    get_input(items=[i for i in sdict.keys()])
    #poses=sdict[list(sdict.keys())[0]]
    poses=sdict[NAME]
    atris=list(attribute.keys())[:-1]
    for i in range (5):
        for j in (0,1):
            #print(sdict[i])
            Chess(atris[i]+'神',poses[i][j])
            Chess(atris[i]+'仙',55-poses[i][j])
    Chess('王神',poses[5][0])
    Chess('王仙',55-poses[5][0])


def move (tryblock,firstpos,boomit=False,speed=30):
    '''To move a chess to another place and make the animation.

This function needs 3 arguments: tryblock,firstpos,boomit(a boolean)'''

    flag=True
    tempObj=chess_board[firstpos].chess
    if chess_board[firstpos].n!=chess_board[tryblock].n:
        tempObj.actpic=tempObj.pics[chess_board[tryblock].n]
    if chess_board[tryblock].chess!= None:
        chess_board[tryblock].chess.alive=False
        chess_board[tryblock].chess= None
    chess_board[firstpos].chess=None
    oldx,oldy=chess_board[firstpos].topleft
    newx,newy=chess_board[tryblock].topleft
    movevecter=Vecter2((newx-oldx),(newy-oldy))
    movevecter.normalize()
    while flag:
        if movevecter.x<0:
            oldx+=max(speed*movevecter.x,(newx-oldx))
        else:
            oldx+=min(speed*movevecter.x,(newx-oldx))
        if movevecter.y<0:
            oldy+=max(speed*movevecter.y,(newy-oldy))
        else:
            oldy+=min(speed*movevecter.y,(newy-oldy))
        chess_board.draw()
        DISPLAYSURF.blit(background,(0,0))
        DISPLAYSURF.blit(tempObj.actpic,(oldx,oldy))
        time.sleep(0.05)
        
        pygame.display.update()
        if oldx==newx and oldy==newy:
            flag=False
    chess_board[tryblock].chess=tempObj
    return


def Win(whose):
    print(whose,'Wins!')


def drawchess():
    for i in posdic.values():
        if i.chess !=None:
            DISPLAYSURF.blit(i.chess.actpic,i.coords)

def eatable(chessA,chessB,chesspos):
    '''To check if ChessA can eat ChessB.If so, return True,

This function needs 3 arguments: ChessA ,ChessB ,ChessBpos.'''
    if chessA.whose!=chessB.whose:
        print (chessA.whose,chessB.whose)
        difindex=attribute.get(chessA.name[:-1])-attribute.get(chessB.name[:-1])
        print(difindex)
        if difindex in(-1,4):
            return True
        if 0<=chesspos<=17:area='神'
        elif 38<=chesspos<=55:area='仙'
        else:area='战'
        if difindex in (-2,3,0) and area=='战':
            return True
        if attribute.get(chessB.name[:-1])==11:
            Win(chessA.whose)
            return True
        if turn!=area and area!='战' and difindex not in(1,-4):
            return True
        if turn==area and difindex in (-2,3,0):
            return True
    return False



def main():
    global turn
    setchess()
    hlightflag=None
    cpos=0
    event=pygame.event.Event(MOUSEMOTION,{'pos':pygame.mouse.get_pos()})
    pygame.event.post(event)
    global firstchess
    while True:

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    return
            elif event.type == MOUSEMOTION:
                blockinfo = None
                p = chess_board.board.collide(event.pos)
                if p is not None:
                    cpos = chess_board.board.coord_to_num(p)
                    blockinfo = chess_board[cpos]
                    hflag = True
                    ##          if blockinfo.chess!= None and blockinfo.chess.whose!= turn:
                    ##              hflag=False
                else:
                    hflag = False
            elif event.type==MOUSEBUTTONDOWN and blockinfo!=None\
                 and event.button==1:
                cango=False
                print(firstchess)
                if firstchess != None and firstchess.whose==turn:
                   #and blockinfo.chess==None:
                    tryblock=cpos
                    cango= tryblock in chess_board.board.get_neibors_by_num(firstpos)
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
                        print('Here!')
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
        #DISPLAYSURF.blit(background,(0,0))#画图
        #drawchess()
        chess_board.draw()
        if hflag:
            DISPLAYSURF.blit(hlight_pic[blockinfo.n],blockinfo.topleft)
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__=='__main__':
    main()
