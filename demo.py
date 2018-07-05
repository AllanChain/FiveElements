import poly
import pygame
from pygame.locals import *
import time
pygame.init()
DIS=pygame.display.set_mode((1024,650))
files_image_background = 'backimage.jpg'
background = pygame.image.load(files_image_background).convert_alpha()
chess_pics={}
def main():
##     base1=poly(n=6,r=40,topleft=(50,50))
##     base3=poly(n=6,r=40,topleft=(50,270))
##     base2=poly(n=8,r=40,topleft=(250,50))
##     pg=ComboGroup((PolyGroup(base_poly=base1,EVEN=3,ODD=2,line=3),\
##                    PolyGroup(base_poly=base3,EVEN=3,ODD=2,line=3),\
##                    PolyGroup(base_poly=base2,EVEN=3,ODD=2,line=3)))
    XMAR=2
    YMAR=40
    size=40
    GAP=size
    base1=poly.poly(n=8,size=size,topleft=(XMAR,YMAR))
    base2=poly.poly(n=6,size=size,topleft=(9.2*size+XMAR+GAP,YMAR+0.35*size))
    base3=poly.poly(n=8,size=size,topleft=(XMAR+14.2*size+XMAR+2*GAP,YMAR))
    pg=poly.ComboGroup((poly.PolyGroup(base_poly=base1,EVEN=4,ODD=3,line=5),\
                        poly.PolyGroup(base_poly=base2,EVEN=7,ODD=6,line=3),\
                        poly.PolyGroup(base_poly=base3,EVEN=4,ODD=3,line=5)))
    pg.set_special_neibors({14:(18,19),
                                15:(19,20,21),
                                16:(21,22,23),
                                17:(3,24)})
    chessurf=pygame.image.load('Eight.png')
    chess_pics[8]=pygame.transform.scale(chessurf,base1.rect.iwh)
    chessurf=pygame.image.load('Six.png')
    chess_pics[6]=pygame.transform.scale(chessurf,base2.rect.iwh)
    for p in pg:
        background.blit(chess_pics[p.n],p.topleft)

    '''for g in pg.groups:
        for p in g:
            pygame.draw.polygon(DIS,(255,255,255),p.points,2)
        pygame.draw.rect(DIS,(255,255,255),g.rect.xywh,2)'''
    DIS.blit(background,(0,0))
    pygame.display.update()
    while True:
        time.sleep(0.2)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return
            if event.type==MOUSEBUTTONDOWN:
                po=pg.collide(event.pos)
                print(po)
main()
