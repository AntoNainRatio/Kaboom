from random import *

###########################################################################################################
#######################                   Initializing    Board                   #########################
###########################################################################################################



def initBoard(n):
    res  = []
    for i in range(n):
        res.append([0]*n)
    return res

def isOneRange(a,b):
    if a==b or a==b-1 or a==b+1:
        return True

def isNeighbor(x1,y1,x2,y2):
    if(isOneRange(x1,x2) and isOneRange(y1,y2)):
        return True
    return False

def spawnBombs(board, n, px, py):
    for i in range(n):
        x = randint(0,n-1)
        y = randint(0,n-1)
        while board[y][x] == -1 or isNeighbor(x,y,px,py):
            x = randint(0,n-1)
            y = randint(0,n-1)
        board[y][x] = -1
        for i in range(-1,2):
            for j in range(-1,2):
                if y+i >= 0 and y+i < n and x+j >= 0 and x+j < n:   
                    if board[y+i][x+j] != -1:
                        board[y+i][x+j] += 1

def getBoards(n, px, py):
    board = initBoard(n)
    marq = []
    for i in range(n):
        marq.append([0]*n)
    spawnBombs(board, n, px, py)
    return board,marq

###########################################################################################################
###########################                DISPLAYING THINGS                   ############################
###########################################################################################################



def printBoard(board,m,px,py):
    print('   ',end='')
    for i in range(len(board)):
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
    for i in range(len(board)):
        print("---",end='')
    print()
    print('   ',end='')
    for i in range(px):
        print('   ',end='')
    print(' |')


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

def placeFlag(m,px,py):
    m[py][px] = 1

def getMove(board,m,px,py):
    c = input('move ?')
    if c == 'w':
        py = moveUp(py)
    elif c == 's':
        py = moveDown(py,len(board))
    elif c =='a':
        px = moveLeft(px)
    elif c == 'd':
        px = moveRight(px,len(board))
    elif c == 'k':
        print('discover Value')
    elif c == 'l':
        placeFlag(m,px,py)
    else:
        print('Invalid')
    return px,py

###########################################################################################################
##########################                   GAME    PROCESS                    ###########################
###########################################################################################################

def propagate(board,m,px,py,size):
    """
    -1: visible
     0: invisible
     1: drapeau
    """
    m[py][px] = -1
    for i in range(-1,2):
        for j in range(-1,2):
            if(i == 0 and j ==0):
                continue
            if(px+i>=0 and px+i < size and py+j>=0 and py+j<size):
                if board[py+j][px+i]==0 and m[py+j][px+i]==0: 
                    m[py+j][px+i] = -1
                    propagate(board,m,px+i,py+j,size)
                m[py+j][px+i] = -1
            

###########################################################################################################
###############################                   GAME                   ##################################
###########################################################################################################


def Play():
    size = 9
    px,py = size//2,size//2
    board, m = getBoards(size,px,py)
    propagate(board,m,px,py,size)
    printBoard(board,m,px,py)
    while True:
        px,py = getMove(board,m,px,py)
        printBoard(board,m,px,py)

# board = getBoard(6,2,1)
# printBoard(board,2,1)
        
Play()

