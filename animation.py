class Animator:
    def move_chess (tryblock,firstpos,swap=False,speed=30):
        tempObj=chess_board[firstpos].chess
        if swap:
            tempObj2=chess_board[tryblock].chess
            if chess_board[firstpos].n!=chess_board[tryblock].n:
                tempObj2.actpic=tempObj2.pics[chess_board[firstpos].n]
        if chess_board[firstpos].n!=chess_board[tryblock].n:
            tempObj.actpic=tempObj.pics[chess_board[tryblock].n]
        #Should this be removed?
        if chess_board[tryblock].chess!= None:
            chess_board[tryblock].chess.alive=False
            chess_board[tryblock].chess= None
        chess_board[firstpos].chess=None
        MOVING.append(self.animate(firstpos,tryblock,tempObj))
        if swap:
            MOVING.append(self.animate(tryblock,firstpos,tempObj2))
        return

    def animate(firstpos,tryblock,tempObj):
        oldx,oldy=chess_board[firstpos].topleft
        newx,newy=chess_board[tryblock].topleft
        movevecter=Vecter2((newx-oldx),(newy-oldy))
        movevecter.normalize()
        while True:
            oldx+=copysign(min(abs(speed*movevecter.x),abs(newx-oldx)),movevecter.x)
            oldy+=copysign(min(abs(speed*movevecter.y),abs(newy-oldy)),movevecter.y)
            DISPLAYSURF.blit(tempObj.actpic,(oldx,oldy))
            if oldx==newx and oldy==newy:
                break
            yield None
        chess_board[tryblock].chess=tempObj
        return

    def hflag_animate(blockinfo):
        yield None
        DISPLAYSURF.blit(hlight_pic[blockinfo.n],blockinfo.topleft)
        
    def process():
        chess_board.draw()
        if MOVING==[]:
            time.sleep(0.2)
            return
        for i in MOVING[:]:
            try:
                next(i)
            except StopIteration:
                MOVING.remove(i)
        pygame.display.update()
