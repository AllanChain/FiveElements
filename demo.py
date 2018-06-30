from  poly.tile import *
import pygame
from pygame.locals import *
import time
pygame.init()
DIS=pygame.display.set_mode((500,500))
def main():
     base=poly(n=6,r=40,topleft=(50,50))
     pg=PolyGroup(base_poly=base,EVEN=4,ODD=4,line=4)
     for p in pg:
          pygame.draw.polygon(DIS,(255,255,255),p.points,2)
     pygame.draw.rect(DIS,(255,255,255),pg.rect,2)
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
