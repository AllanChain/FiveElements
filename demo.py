from  poly.tile import *
import pygame
from pygame.locals import *
import time
pygame.init()
DIS=pygame.display.set_mode((500,500))
def main():
     base1=poly(n=6,r=40,topleft=(50,50))
     base2=poly(n=8,r=40,topleft=(250,50))
     pg=ComboGroup((PolyGroup(base_poly=base1,EVEN=4,ODD=4,line=3),\
                    PolyGroup(base_poly=base2,EVEN=4,ODD=3,line=4)))
     for g in pg.groups:
          for p in g:
               pygame.draw.polygon(DIS,(255,255,255),p.points,2)
          pygame.draw.rect(DIS,(255,255,255),g.rect,2)
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
