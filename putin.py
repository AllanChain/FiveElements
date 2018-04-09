import pygame,time,loader
from pygame.locals import *
pygame.init()
class Lister:
    def __init__(self,items,DIS,max_list=3,pos=(0,0),
                 COLOR=(0,0,0),BGCOLOR=(0,200,200),HCOLOR=(200,200,0),
                 height=50,width=200):
##        self.items=items
##        self.DIS=display
##        self.pos=pos
##        self.max_list=max_list
##        
##        self.height=50
##        self.width=200
        self.__dict__.update(locals())
        del self.__dict__['self']
        self.SURF=pygame.surface.Surface((self.width,self.height*max_list))
        self.BGSURF=pygame.surface.Surface((self.width,self.height*max_list))
        self.BGSURF.fill(BGCOLOR)
        #FontObj=pygame.font.Font('STXINWEI.ttf',20)
        myfonts=['stliti','stkaiti','华文新魏','arial']
        sys_fonts=pygame.font.get_fonts()
        for font in myfonts:
            if font in sys_fonts:
                break
        else:
            print("Can't get system's appropriate font.")
        FontObj=pygame.font.SysFont(font,20)
        self.TEXTS=list(map(lambda txt:FontObj.render(txt,True,COLOR),items))
        self.focus=self.head=0
        self.update()
        return
    def scroll(self,down):
        self.focus+=down
        self.head+=down
        if self.focus<0 or self.focus>=len(self.items):
            self.focus-=down
        if self.head<0 or self.head>len(self.items)-self.max_list:
            self.head-=down
        self.update()
    def update(self):
        self.SURF.blit(self.BGSURF,(0,0))
        pygame.draw.rect(self.SURF,self.HCOLOR,
                         (0,(self.focus-self.head)*self.height,
                          self.width,self.height))
        for i in range(self.head,self.head+self.max_list):
            rect=self.TEXTS[i].get_rect()
            rect.center=(self.width//2,self.height*(i-self.head+0.5))
            self.SURF.blit(self.TEXTS[i],rect)
        self.DIS.blit(self.SURF,self.pos)
        pygame.display.update()
        return
    def click(self,x,y):
        if 0<x<self.width and 0<y<self.max_list*self.height:
            return self.items[self.head+y//self.height]
    def enter(self):
        return self.items[self.focus]
    def react(self,event):
        if event.type==MOUSEBUTTONDOWN:
            if event.button in (4,5):
                self.scroll(event.button*2-9)
            elif event.button==1:
                item=self.click(event.pos[0]-self.pos[0],
                                    event.pos[1]-self.pos[1])
                self.callback(item)
        if event.type==KEYDOWN:
            if event.key in(273,274):
                self.scroll(event.key*2-547)
            elif event.key==K_RETURN:
                item=self.enter()
                self.callback(item)
def main():
    DIS=pygame.display.set_mode((500,500))
    DIS.fill((255,255,255))
    loader.init('place')
    stra_dict=loader.read_db()
    items=[i for i in stra_dict.keys()]
    #items=['诛仙','默认','Default','龙蛇','蛇皮']
    mylister=Lister(items,DIS,pos=(50,50),max_list=2)
    mylister.callback=print
    while True:
        for event in pygame.event.get():
            mylister.react(event)
            if event.type==QUIT:
                pygame.quit()
                return
            time.sleep(0.2)
if __name__=="__main__":
    main()
