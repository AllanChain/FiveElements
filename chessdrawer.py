# -*- coding: utf-8 -*-
import pygame,os,poly
import loader
#import stylesheet

loader.init('color')
style=loader.stra_to_color(loader.read_db())['default']
print(style)
_style={
    u'金神':(((200,200,100),(255,255,0)),5),
    u'金仙':(((200,200,100),(255,255,0)),5),
    u'水神':(((0,255,255),(0,0,180)),5),
    u'水仙':(((0,255,255),(0,0,180)),5),
    u'木神':(((50,255,175),(0,200,0)),5),
    u'木仙':(((50,255,175),(0,200,0)),5),
    u'火神':(((255,175,50),(200,0,0)),5),
    u'火仙':(((255,175,50),(200,0,0)),5),
    u'土神':(((200,175,150),(210,147,84)),5),
    u'土仙':(((200,175,150),(210,147,84)),5),
    u'王仙':(((255,50,100),(0,200,0)),5),
    u'王神':(((255,50,100),(0,200,0)),5),
    }

def generate(name,whose,n,color,shadow_width=5):
    start_color,central_color=color
    font_size=80 if n==8 else 72
    ShapeObj=poly.poly(n=n,leftop=(0,0),size=39)
    center=(ShapeObj.rect[0]//2,ShapeObj.rect[1]//2)
    #print(ShapeObj.rect)
    surf=pygame .surface.Surface(ShapeObj.rect).convert_alpha()
    surf.fill((0,0,0,0))
    surf1=pygame .surface.Surface(ShapeObj.rect).convert_alpha()
    surf1.fill((0,0,0,0))
    r0=central_color[0]
    g0=central_color[1]
    b0=central_color[2]
    r=(start_color[0]-r0)/40
    g=(start_color[1]-g0)/40
    b=(start_color[2]-b0)/40
    FontObj=pygame.font.Font('STXINWEI.ttf',font_size)
    Whosurf=FontObj.render(whose,True,(180,180,180)).convert_alpha()
    rect=Whosurf.get_rect()
    rect.center=center
    surf.blit(Whosurf,rect)
    for i in range(40,0,-1):
        factor=0.9 #影响渐变效果
        color=(r0+r*i*factor,g0+g*i*factor,b0+b*i*factor,220)
        ShapeObj=poly.poly(n=n,center=center,size=i)
        pygame.draw.polygon(surf1,color,ShapeObj.points,0)
    surf.set_alpha(100)
    surf.blit(surf1,(0,0))
    FontObj=pygame.font.Font('STXINWEI.ttf',50)
    Namesurf=FontObj.render(name,True,(180,180,180,100)).convert_alpha()
    Namesurf.set_alpha(8)
    rect=Namesurf.get_rect()
    rect.center=center
    surf.blit(Namesurf,rect)
    return surf
if __name__=='__main__':
    from pygame.locals import *
    pygame.init()
    DISPLAYSURF=pygame.display.set_mode((300,400),0,32)#.convert_alpha()
    fpsClock=pygame.time.Clock()
    DISPLAYSURF.fill((255,255,255))
    n=0
    for name,sty in style.items():
        ##print(name,name[0],name[-1])
        ##print(style)
        surf=generate(name[0],'神',8,*sty)
        DISPLAYSURF.blit(surf,((n%3)*100,(n//3)*100))
        n+=1
    pygame.display.update()
    while True:
        
        for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    os._exit(0)
        fpsClock.tick(20)
