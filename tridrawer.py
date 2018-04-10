import pygame,poly
def drawtri(color,size,alpha=255):
    X=0
    Y=1
    color=color+(alpha,)
    YIN=pygame .surface.Surface((size,size//5)).convert_alpha()
    YIN.fill((255,255,255,0))
    pygame.draw.rect(YIN,color,(0,0,size*2//5,size//5))
    pygame.draw.rect(YIN,color,(size*3//5,0,size*2//5,size//5))
    YANG=pygame .surface.Surface((size,size//5)).convert_alpha()
    YANG.fill(color)
    YI=(YIN,YANG)
    Trigram=[]
    for lower in YI:
        for mid in YI:
            for upper in YI:
                GUA=pygame .surface.Surface((size,size)).convert_alpha()
                GUA.fill((255,255,255,0))
                GUA.blit(lower,(0,size*4//5))
                GUA.blit(mid,(0,size*2//5))
                GUA.blit(upper,(0,0))
                Trigram.append(GUA)
    temp=poly.poly(n=8,topleft=(size,size),size=size*2)
    picsurf=pygame .surface.Surface((size*7,size*7)).convert_alpha()
    picsurf.fill((255,255,255,0))
    for i in range(4):
        Trigram[i]=pygame.transform.rotate(Trigram[i],-(i-4)*45)
        TriRect=Trigram[i].get_rect()
        TriRect.center=((temp.points[4-i][X]+temp.points[3-i][X])//2,(temp.points[4-i][Y]+temp.points[3-i][Y])//2)
        picsurf.blit(Trigram[i],TriRect)
    for i in [4,5,6,7]:
        Trigram[i]=pygame.transform.rotate(Trigram[i],(i+1)*45)
        TriRect=Trigram[i].get_rect()
        TriRect.center=((temp.points[i][X]+temp.points[(i+1)%8][X])//2,(temp.points[i][Y]+temp.points[(i+1)%8][Y])//2)
        picsurf.blit(Trigram[i],TriRect)
    return picsurf
if __name__=='__main__':
    from pygame.locals import *
    pygame.init()
    DIS=pygame.display.set_mode((400,400))
    DIS.blit(drawtri((0,0,255),40),(0,0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                raise EOFError
