# from gamebuino_meta import waitForUpdate, display, color, buttons
from random import randint

###########################################################################################################
#######################                   Global    Variables                   #########################
###########################################################################################################

# SCREEN_WIDTH  = 80
# SCREEN_HEIGHT = 64
# NBCOL = 10
# NBLI = 8
# MODE_START    = 0
# MODE_READY    = 1
# MODE_PLAY     = 2
# MODE_LOST     = 3
# GRIS = color.DARKGRAY
# GRISCLAIR = color.GRAY
# VERT = color.GREEN
# BLEU =  color.BLUE
# ORANGE = color.ORANGE
# VIOLET = color.PURPLE
# ROUGE = color.RED
# MARRON = color.BROWN
# NOIR = color.BLACK

# game = {
#     'mode': MODE_MENU,
#     'nbBomb': 0,
#     'time': 0,
#     'size': 10,
#     'board' : None,
#     'm' : None,
#     'px' :  3,
#     'py' :  3,
# }


###########################################################################################################
#######################                   Initializing    Board                   #########################
###########################################################################################################



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

# def displayBoard(board, m, sizex, sizey):
#     display.setColor(GRISCLAIR)
#     display.fillRect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
#     display.setColor(Gris)
#     tcasex,tcasey = SCREEN_WIDTH/sizex, SCREEN_HEIGHT/sizey
#     y = 0
#     for i in range(sizey):
#         x =0
#         for j in range(sizex):
#             display.drawRect(x,y,SCREEN_WIDTH,SCREEN_HEIGHT)
#             x += tcasex
#         y += tcasey



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
    if m[py][px] != -1:
        m[py][px] = 1
    else:
        print('Place already discovered')

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
        propagate(board,m,px,py,len(board[0]),len(board))
    elif c == 'l':
        placeFlag(m,px,py)
    else:
        print('Invalid')
    return px,py

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
        print("You lost")
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

###########################################################################################################
###############################                   GAME                   ##################################
###########################################################################################################


def Play():
    sizex = 10
    sizey = 10
    px,py = sizex//2,sizey//2
    board, m = getBoards(sizex,sizey,px,py,10)
    propagate(board,m,px,py,sizex,sizey)
    while True:
        printBoard(board,m,px,py)
        px,py = getMove(board,m,px,py)

# board = getBoard(6,2,1)
# printBoard(board,2,1)

Play()