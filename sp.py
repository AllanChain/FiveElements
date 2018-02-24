def move(firstb,tryb):
        firstblock=posdic[firstb]
        tryblock=posdic[tryb]
        if firstblock.type==tryblock.type=='Eight':
                j=tryblock.index-firstblock.index
                dic={4:3,
                3:1,
                -4:6,
                -3:4}
                model=Eight((0,0),size)
                point=model.points[dic[j]]
                surfsize=[]
                for i in (0,1)
                        if point[i]>1.2*size:
                                startpo[i]=0
                                surfsize[i]=2*point[i]
                        else:
                                startpo[i]=2.4*size-point[i]*2
                                surfsize[i]=4.8*size-point[i]*2
                surf=pygame.surface.Surface(tuple(surfsize))
                surf.blit(firstchess.chess.actpic,tuple(startpo))
                degree=5 if j<0 else -5
                for deg in range(28):
                        surf1=pygame.transform.rotate(surf,deg*degree)
                        rect1=surf1.get_rect()
                        rect1.center=firstblock.shape.points[dic[j]]
                        DISPLAYSURF.blit(surf1,rect1)
                        pygame.display.update()
                surf=pygame.surface.Surface((2.4*size,2.4*size))
                surf.blit(firstchess.chess.actpic,(0,0))
                for deg in range(28):
                        surf1=pygame.transform.rotate(surf,-deg*degree)
                        rect1=surf1.get_rect()
                        rect1.center=firstblock.shape.center
                        DISPLAYSURF.blit(surf1,rect1)
                        pygame.display.update()
        elif firstblock.type==tryblock.type=='Six':
                flag=True
                if tryblock.chess!= None:
                        posdic[tryb].chess.alive=False
                        posdic[tryb].chess= None
                        posdic[firstb].chess=None
                #if boomit:
                #boomsound.play()
                #time.sleep(0.5)
                #boomsound.stop()
                oldx,oldy=firstblock.coords
                newx,newy=tryblock.coords
                movevecter=pygame.math.Vecter2((newx-oldx),(newy-oldy))
                movevecter.normalize_ip()

                print(oldx,oldy)
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
                        DISPLAYSURF.blit(firstpos.actpic,(oldx,oldy))
                        time.sleep(0.05)
                        drawchess()
                        pygame.display.update()
                        if oldx==newx and oldy==newy:
                            flag=False
                        print(oldx,oldy)
                posdic[tryb].chess=firstblock
                
        else:
                oldx,oldy=firstblock.coords
                newx,newy=tryblock.coords
                movec=pygame.math.Vecter2((newx-oldx),(newy-oldy))
                dis=movec.length()
                movec.normalize_ip()
                spinspeed=100/dis
                degree=0
                speedup=0
                a=(oldx,oldy)
                for i in range(int(dis/2)):
                        
                        a+=movec
                        degree+=speedup
                        surf1=pygame.transform.rotate(firstblock.chess,actpic,degree)
                        speedup+=spinspeed
                        DISPLAYSURF.blit(surf1,(a.x,a.y))
                #posdic[firstb].chess.actpic=posdic[firstb].chess.pics[1-...]
                degree-=2*(degree%360)
                for i in range(int(dis/2)):
                        a+=movec
                        degree-=speedup
                        speedup-=spinspeed
                        surf1=pygame.transform.rotate(firstblock.chess,actpic,degree)
                        DISPLAYSURF.blit(surf1,(a.x,a.y))
                DISPLAYSURF.blit(firstblock.chess,actpic,(newx,newy))
