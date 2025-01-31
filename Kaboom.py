from random import randint

def initBoard(sizex,sizey):
    res  = []
    for i in range(sizey):
        res.append([0]*sizex)
    return res

def isOneRange(a,b):
    if a==b or a==b-1 or a==b+1:
        return True

def isNeighbor(x1,y1,x2,y2):
    if(isOneRange(x1,x2) and isOneRange(y1,y2)):
        return True
    return False

def spawnBombs(board, sizex, sizey, px, py, n):
    for i in range(n):
        x = randint(0,sizex-1)
        y = randint(0,sizey-1)
        while board[y][x] == -1 or isNeighbor(x,y,px,py):
            x = randint(0,sizex-1)
            y = randint(0,sizey-1)
        board[y][x] = -1
        for i in range(-1,2):
            for j in range(-1,2):
                if y+i >= 0 and y+i < sizey and x+j >= 0 and x+j < sizex:
                    if board[y+i][x+j] != -1:
                        board[y+i][x+j] += 1

def getBoards(sizex, sizey, px, py,n):
    board = initBoard(sizex,sizey)
    marq = initBoard(sizex,sizey)
    spawnBombs(board, sizex, sizey, px, py,n)
    return board,marq

###########################################################################################################
###########################                DISPLAYING THINGS                   ############################
###########################################################################################################



def printBoard(board,m,px,py,nbFlags):
    print('   ',end='')
    for i in range(len(board[0])):
        print("---",end='')
    print()
    for i in range(len(board)):
        if i == py:
            print('--|',end='')
        else:
            print('  |',end='')
        for j in range(len(board[0])):
            if(m[i][j] == -1):
                if(board[i][j] >= 0):
                    print(' '+str(board[i][j])+" ",end='')
                else:
                    print(str(board[i][j])+" ",end='')
            elif(m[i][j] == 1):
                print(' F ',end='')
            else:
                print('   ',end='')
        print('|')
    print('   ',end='')
    for i in range(len(board[0])):
        print("---",end='')
    print()
    print('   ',end='')
    for i in range(px):
        print('   ',end='')
    print(' |')
    print('Flags left : '+str(nbFlags))


###########################################################################################################
##########################                   ACTIONS HANDLING                   ###########################
###########################################################################################################

def moveUp(py):
    if(py>0):
        return py-1
    return py

def moveDown(py,size):
    if(py < size-1):
        return py+1
    return py

def moveLeft(px):
    if(px>0):
        return px-1
    return px

def moveRight(px,size):
    if(px<size-1):
        return px+1
    return px

def placeFlag(m,px,py,nbFlags):
    if m[py][px] == 0 and nbFlags>0:
        m[py][px] = 1
        nbFlags-=1
    elif m[py][px] == 1:
        nbFlags+=1
        m[py][px] = 0
    return nbFlags

def getMove(board,m,px,py,nbFlags):
    c = input()
    if c == 'w':
        py = moveUp(py)
    elif c == 's':
        py = moveDown(py,len(board))
    elif c =='a':
        px = moveLeft(px)
    elif c == 'd':
        px = moveRight(px,len(board[0]))
    elif c == 'k':
        propagate(board,m,px,py,len(board[0]),len(board))
    elif c == 'l':
        nbFlags = placeFlag(m,px,py,nbFlags)
    elif c == 'q':
        print("See you later :)")
        quit()
    else:
        print('Invalid')
    return px,py,nbFlags

###########################################################################################################
##########################                   GAME    PROCESS                    ###########################
###########################################################################################################

def propagate(board,m,px,py,sizex,sizey):
    """
    -1: visible
     0: invisible
     1: drapeau
    """
    m[py][px] = -1
    if board[py][px] == -1:
        print("You lost..")
        quit()
    else:
        if(board[py][px]==0):
            for i in range(-1,2):
                for j in range(-1,2):
                    if(i == 0 and j ==0):
                        continue
                    if(px+i>=0 and px+i < sizex and py+j>=0 and py+j<sizey):
                        if board[py+j][px+i]==0 and m[py+j][px+i]==0:
                            m[py+j][px+i] = -1
                            propagate(board,m,px+i,py+j,sizex,sizey)
                        m[py+j][px+i] = -1

def isFullM(m):
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == 0:
                return False
    return True

def Play():
    sizex = 10
    sizey = 8
    nbFlags = sizex*sizey // 3
    px,py = sizex//2,sizey//2
    board, m = getBoards(sizex,sizey,px,py,nbFlags)
    propagate(board,m,px,py,sizex,sizey)
    won = False
    while not won:
        printBoard(board,m,px,py,nbFlags)
        px,py,nbFlags = getMove(board,m,px,py,nbFlags)
        won = isFullM(m);
    if won:
        printBoard(board,m,px,py,nbFlags)
        print("Congrats !! You won !")


Play()
