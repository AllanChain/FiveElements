#*_* coding:utf-8 *_*
import pygame,time,math,poly,chessdrawer
import loader
from pygame.locals import*

pygame.init()
posdic={}
hlightdict={}
hlight_color=(0,200,200,100)
DISPLAYSURF=pygame.display.set_mode((1024,650),0,32)
pygame.display.set_caption('Fighting...')
files_image_background = 'backimage.jpg'
files_image_highlight ='blockhlight.png'
files_sound_boomsound ='Boomsound.mp3'
background = pygame.image.load(files_image_background) .convert_alpha()

highlight=pygame.surface.Surface((96,96)).convert_alpha()
highlight.fill((0,0,0,0))
EightObj=poly.poly(n=8,center=(48,48),size=40)
pygame.draw.polygon(highlight,hlight_color,EightObj.points,0)
hlightdict['Eight']=highlight
SixObj=poly.poly(n=6,size=40)
highlight=pygame.surface.Surface(SixObj.rect).convert_alpha()
highlight.fill((0,0,0,0))
pygame.draw.polygon(highlight,hlight_color,SixObj.points,0)
hlightdict['Six']=highlight
#boomsound = pygame.mixer.Sound(files_sound_boomsound)
FPS=5
fpsClock=pygame.time.Clock()
loader.init('color')
style=loader.stra_to_color(loader.read_db())['default']
turn='神'
#hlightflag=False
firstchess= None
firstpos=0
attribute={'金':1,
         '水':4,
         '木':2,
         '火':5,
         '土':3,
         '王':11}#['Medal','Wood','Earth','Water','Fire']

class Chess:
    '''Include every chess.'''
    def __init__(self,name,position):
        '''This function needs 2 arguments: name,position .'''
        self.name=name
        self.whose=name[-1:]
        self.alive=True
        self.position=position
        self.eight_pic,self.six_pic=getpic(name)
        self.actpic=self.eight_pic if posdic[position].type=='Eight'\
                     else self.six_pic
        #self.attribute
        posdic[position].chess=self
        #xypos=posdic[position]
        DISPLAYSURF.blit(self.actpic,posdic[position].coords)
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


class Block:
    def __init__(self):
        self.coords=()
        self.cangos=[]
        self.chess=None
        self.shape=None
        self.type=''
def getpic(name):
    whose=name[-1:]
    myname=name[:-1]
    
    sty=style[myname]
    #print(sty)
    return(chessdrawer.generate(myname,whose,8,sty),\
           chessdrawer.generate(myname,whose,6,sty))
def setchess():
    loader.init('place')
    sdict=loader.read_db()
    poses=sdict[list(sdict.keys())[0]]
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
    tempObj=posdic[firstpos].chess
    if posdic[firstpos].type!=posdic[tryblock].type:
        tempObj.actpic=tempObj.six_pic if posdic[tryblock].type=='Six'\
                        else tempObj.eight_pic
    if posdic[tryblock].chess!= None:
        posdic[tryblock].chess.alive=False
        posdic[tryblock].chess= None
    posdic[firstpos].chess=None
    oldx,oldy=posdic[firstpos].coords
    newx,newy=posdic[tryblock].coords
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
        DISPLAYSURF.blit(background,(0,0))
        DISPLAYSURF.blit(tempObj.actpic,(oldx,oldy))
        time.sleep(0.05)
        drawchess()
        pygame.display.update()
        if oldx==newx and oldy==newy:
            flag=False
    posdic[tryblock].chess=tempObj
    return
def Win(whose):
    print(whose,'Wins!')
def start():
    global block,posdic,DISPLAYSURF#,attribute,show
    XMAR=2
    YMAR=40
    size=40
    GAP=size
    for i in range(56):
        posdic[i]=Block()
    x=XMAR+size*1.2
    y=YMAR+size*1.2
    for i in range(0,15,7):
        for j in range(4):
            posdic[i+j].type='Eight'
            posdic[i+j+38].type='Eight'
            posdic[i+j].shape=poly.poly(n=8,center=(x,y+j*size*3.4),size=size)
            posdic[i+j+38].shape=poly.poly(n=8,center=(x+14.2*size+XMAR+2*GAP,y+j*size*3.4),size=size)
            
        x+=size*3.4
    x=XMAR+size*2.9
    y=YMAR+size*2.9
    for i in range(0,8,7):
        for j in range(4,7):
            
            posdic[i+j].type='Eight'
            posdic[i+j+38].type='Eight'
            posdic[i+j].shape=poly.poly(n=8,center=(x,y+(j-4)*size*3.4),size=size)
            posdic[i+j+38].shape=poly.poly(n=8,center=(x+14.2*size+XMAR+2*GAP,y+(j-4)*size*3.4),size=size)
            #print(posdic[i+j].shape)
        x+=size*3.4
    for i in range(18,25):
        posdic[i].type='Six'
        posdic[i+13].type='Six'
        posdic[i].shape=poly.poly(n=6,center=(10.2*size+XMAR+GAP,YMAR+0.35*size+0.85*size+1.7*size*(i-18)),size=size)
        posdic[i+13].shape=poly.poly(n=6,center=(13.2*size+XMAR+GAP,YMAR+0.35*size+0.85*size+1.7*size*(i-18)),size=size)
    for i in range(25,31):
        posdic[i].type='Six'
        posdic[i].shape=poly.poly(n=6,center=(11.7*size+XMAR+GAP,YMAR+0.35*size+1.7*size+1.7*size*(i-25)),size=size)
    def bond(step,list1,flag=True):
        for start,end in list1:
            for i in ((start,end,step),(end,start,-step)):
                for j in range(*i):
                    posdic[j].cangos.append(j+i[2])
                    if flag:
                        posdic[55-j].cangos.append(55-j-i[2])
        return
    def singlebond(list1):
        for a,*s in list1:
            for b in s:
                posdic[a].cangos.append(b)
                posdic[b].cangos.append(a)
                posdic[55-a].cangos.append(55-b)
                posdic[55-b].cangos.append(55-a)
    bond(3,[(1,7),(2,14),(3,15),(10,16)])
    bond(4,[(7,15),(0,16),(1,17),(2,10)])
    bond(1,[(18,24),(25,30),(31,37)],False)
    for i in range(19,25):
        bond(6,[(i,i+12)],False)
        bond(7,[(i-1,i+13)],False)
    singlebond([(14,18,19),(15,19,20,21),(16,21,22,23),(17,23,24)])
##    for k,v in cango_dict.cango_dict.items():
##        posdic[k].cangos=v
    for i in range(56):
        
        posdic[i].coords=posdic[i].shape.leftop
        chessurf=pygame.image.load(posdic[i].type+'.png')
        if posdic[i].type=='Eight':
            chessurf=pygame.transform.scale(chessurf,(int(size*2.4),int(size*2.4)))
        else:
            
            chessurf=pygame.transform.scale(chessurf,(size*2,int(size*1.7)))
        background.blit(chessurf,posdic[i].shape.leftop)
        

    
    
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
                if firstchess != None and firstchess.whose==turn:
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

if __name__=='__main__':
    start()
    main()
