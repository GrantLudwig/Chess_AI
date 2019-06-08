#main.py v1.0
#Grant Ludwig and Mitch Downey

# import the pygame module, so you can use it
import pygame
import time

boardSquareSize = 64
pieceSize = 45
board = {}
screen_width = 1088
screen_height = 512
playClockTime = 90
screen = pygame.display.set_mode((screen_width,screen_height))
startTime = time.time()
chessBoard = pygame.image.load("assets/board.png")
moveClickList = []
pieceClicked = None
nothing = None #for doing nothing

#trying something out here
pieceDict = {} # dict of pieces
                #key: (row,col) board
                #value: gamePiece
# 2d list representing the board, each location is one square
# For example, a black pawn would be 'bp', empty is 'ee'

# generalized class for game pieces
class gamePiece():

    def __init__(self, pieceImg, pieceType, boardPos, color):
        self.Piece = pieceImg # pygame image of the piece
        self.Pos = boardPos # position of the piece on board, (row,col)
        self.Color = color # single char, 'b' or 'w'
        self.Type = pieceType   # single char, what piece type it is
                                # 'r' = rook, 'n' = knight, 'b' = bishop
                                # 'q' = queen, 'k' = king, 'p' = pawn
        self.First = True # for pawns, if this is their first move or not
        # add more attributes as needed

    def movePiece(self, targetPos):
        self.Pos = targetPos
        self.First = False

    def getPos(self):
        #r, c = self.Pos
        return getBoard(self.Pos)

#returns a list of the moves the piece can make
# still need range check
def moveList(piece):
    list = []
    currRow, currCol = piece.Pos
    allyColor = piece.Color
    enemyColor = None
    if allyColor == 'b':
        enemyColor =  'w'
    else:
        enemyColor = 'b'
    #pawn
    #need bounds checking
    if piece.Type == 'p': 
        if piece.First: #first move
            if allyColor == 'b':
                if (currRow + 1, currCol) in pieceDict:
                    nothing = None
                else:
                    list.append((currRow + 1, currCol))
                if (currRow + 2, currCol) in pieceDict:
                    nothing = None
                else:
                    list.append((currRow + 2, currCol))
            else:
                if (currRow - 1, currCol) in pieceDict:
                    nothing = None
                else:
                    list.append((currRow - 1, currCol))
                if (currRow - 2, currCol) in pieceDict:
                    nothing = None
                else:
                    list.append((currRow - 2, currCol))
        else:
            if allyColor == 'b':
                if currRow + 1 >= 0 and currRow + 1 < 8:
                    if (currRow + 1, currCol) in pieceDict:
                        nothing = None
                    else:
                        list.append((currRow + 1, currCol))
            else:
                if currRow - 1 >= 0 and currRow - 1 < 8:
                    if (currRow - 1, currCol) in pieceDict:
                        nothing = None
                    else:
                        list.append((currRow - 1, currCol))
        #attack
        if allyColor == 'b':
            #right
            if currCol + 1 >= 0 and currCol + 1 < 8 and currRow + 1 >= 0 and currRow + 1 < 8:
                if (currRow + 1, currCol + 1) in pieceDict:
                    if pieceDict[(currRow + 1, currCol + 1)].Color != allyColor:
                        list.append((currRow + 1, currCol + 1))
            #left
            if currCol - 1 >= 0 and currCol - 1 < 8 and currRow + 1 >= 0 and currRow + 1 < 8:
                if (currRow + 1, currCol - 1) in pieceDict:
                    if pieceDict[(currRow + 1, currCol - 1)].Color != allyColor:
                        list.append((currRow + 1, currCol - 1))
        else:
            #right
            if currCol - 1 >= 0 and currCol - 1 < 8 and currRow + 1 >= 0 and currRow + 1 < 8:
                if (currRow - 1, currCol + 1) in pieceDict:
                    if pieceDict[(currRow - 1, currCol + 1)].Color != allyColor:
                        list.append((currRow - 1, currCol + 1))
            #left
            if currCol - 1 >= 0 and currCol - 1 < 8 and currRow - 1 >= 0 and currRow - 1 < 8:
                if (currRow - 1, currCol - 1) in pieceDict:
                    if pieceDict[(currRow - 1, currCol - 1)].Color != allyColor:
                        list.append((currRow - 1, currCol - 1))
        return list
    #rook
    elif piece.Type == 'r':
        #right
        for col in range(currCol + 1, 8):
            if (currRow, col) in pieceDict:
                if pieceDict[(currRow, col)].Color == allyColor:
                    break
                else:
                    list.append((currRow, col))
                    break
            else:
                list.append((currRow, col))
        #left
        for col in range(currCol - 1, -1, -1):
            if (currRow, col) in pieceDict:
                if pieceDict[(currRow, col)].Color == allyColor:
                    break
                elif pieceDict[(currRow, col)].Color != allyColor:
                    list.append((currRow, col))
                    break
            else:
                list.append((currRow, col))
        #up
        for row in range(currRow - 1, -1, -1):
            if (row, currCol) in pieceDict:
                if pieceDict[(row, currCol)].Color == allyColor:
                    break
                elif pieceDict[(row, currCol)].Color != allyColor:
                    list.append((row, currCol))
                    break
            else:
                list.append((row, currCol))
        #down
        for row in range(currRow + 1, 8):
            if (row, currCol) in pieceDict:
                if pieceDict[(row, currCol)].Color == allyColor:
                    break
                elif pieceDict[(row, currCol)].Color != allyColor:
                    list.append((row, currCol))
                    break
            else:
                list.append((row, currCol))
        return list
    #knights
    elif piece.Type == 'n':
        #down 2, left 1
        row = currRow + 2
        col = currCol - 1
        knightCheck(row, col, list, allyColor)
        #down 2, right 1
        row = currRow + 2
        col = currCol + 1
        knightCheck(row, col, list, allyColor)
        #down 1, left 2
        row = currRow + 1
        col = currCol - 2
        knightCheck(row, col, list, allyColor)
        #down 1, right 2
        row = currRow + 1
        col = currCol + 2
        knightCheck(row, col, list, allyColor)
        #up 1, left 2
        row = currRow - 1
        col = currCol - 2
        knightCheck(row, col, list, allyColor)
        #up 1, right 2
        row = currRow - 1
        col = currCol + 2
        knightCheck(row, col, list, allyColor)
        #up 2, left 1
        row = currRow - 2
        col = currCol - 1
        knightCheck(row, col, list, allyColor)
        #up 2, right 1
        row = currRow - 2
        col = currCol + 1
        knightCheck(row, col, list, allyColor)
        return list
    #bishops
    elif piece.Type == 'b': 
        #up left
        #zip combines the 2 ranges, needed to increment at the same rate
        for row, col in zip(range(currRow - 1, -1, -1), range(currCol - 1, -1, -1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        #up right
        for row, col in zip(range(currRow - 1, -1, -1), range(currCol + 1, 8, 1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        #down left
        for row, col in zip(range(currRow + 1, 8, 1), range(currCol - 1, -1, -1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        #down right
        for row, col in zip(range(currRow + 1, 8, 1), range(currCol + 1, 8, 1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        return list
    #kings
    elif piece.Type == 'k': 
        #down
        row = currRow + 1
        kingCheck(row, currCol, list, allyColor)
        #up
        row = currRow - 1
        kingCheck(row, currCol, list, allyColor)
        #left
        col = currCol - 1
        kingCheck(currRow, col, list, allyColor)
        #right
        col = currCol + 1
        kingCheck(currRow, col, list, allyColor)
        #down left
        row = currRow + 1
        col = currCol - 1
        kingCheck(row, col, list, allyColor)
        #down right
        row = currRow + 1
        col = currCol + 1
        kingCheck(row, col, list, allyColor)
        #up left
        row = currRow - 1
        col = currCol - 1
        kingCheck(row, col, list, allyColor)
        #up right
        row = currRow - 1
        col = currCol + 1
        kingCheck(row, col, list, allyColor)
        return list 
    #queens
    else:
        #rook like check
        #right
        for col in range(currCol + 1, 8):
            if (currRow, col) in pieceDict:
                if pieceDict[(currRow, col)].Color == allyColor:
                    break
                else:
                    list.append((currRow, col))
                    break
            else:
                list.append((currRow, col))
        #left
        for col in range(currCol - 1, -1, -1):
            if (currRow, col) in pieceDict:
                if pieceDict[(currRow, col)].Color == allyColor:
                    break
                elif pieceDict[(currRow, col)].Color != allyColor:
                    list.append((currRow, col))
                    break
            else:
                list.append((currRow, col))
        #up
        for row in range(currRow - 1, -1, -1):
            if (row, currCol) in pieceDict:
                if pieceDict[(row, currCol)].Color == allyColor:
                    break
                elif pieceDict[(row, currCol)].Color != allyColor:
                    list.append((row, currCol))
                    break
            else:
                list.append((row, currCol))
        #down
        for row in range(currRow + 1, 8):
            if (row, currCol) in pieceDict:
                if pieceDict[(row, currCol)].Color == allyColor:
                    break
                elif pieceDict[(row, currCol)].Color != allyColor:
                    list.append((row, currCol))
                    break
            else:
                list.append((row, currCol))
        #bishop like check
        #up left
        #zip combines the 2 ranges, needed to increment at the same rate
        for row, col in zip(range(currRow - 1, -1, -1), range(currCol - 1, -1, -1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        #up right
        for row, col in zip(range(currRow - 1, -1, -1), range(currCol + 1, 8, 1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        #down left
        for row, col in zip(range(currRow + 1, 8, 1), range(currCol - 1, -1, -1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        #down right
        for row, col in zip(range(currRow + 1, 8, 1), range(currCol + 1, 8, 1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                if (row,col) in pieceDict:
                    if pieceDict[(row, col)].Color == allyColor:
                        break
                    else:
                        list.append((row, col))
                        break
                else:
                    list.append((row, col))
            else:
                break
        return list 

#generalized knight checking
def knightCheck(row, col, list, allyColor):
    if col >= 0 and col < 8 and row >= 0 and row < 8:
        if (row,col) in pieceDict:
            if pieceDict[(row, col)].Color != allyColor:
                list.append((row, col))
        else:
            list.append((row, col))

#generalized king checking
def kingCheck(row, col, list, allyColor):
    if col >= 0 and col < 8 and row >= 0 and row < 8:
        if (row,col) in pieceDict:
            if pieceDict[(row, col)].Color != allyColor:
                list.append((row, col))
        else:
            list.append((row, col))

#def getBoard(row, col):
#   return board[(row,col)]

def getBoard(bPos):
    return board[bPos]
 
# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("assets/pawnW.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Chess")

    # load image (it is in same directory)
    whitePawn = pygame.image.load("assets/pawnW.png")
    blackPawn = pygame.image.load("assets/pawnB.png")
    whiteRook = pygame.image.load("assets/rookW.png")
    blackRook = pygame.image.load("assets/rookB.png")
    whiteKnight = pygame.image.load("assets/knightW.png")
    blackKnight = pygame.image.load("assets/knightB.png")
    whiteBishop = pygame.image.load("assets/bishopW.png")
    blackBishop = pygame.image.load("assets/bishopB.png")
    whiteQueen = pygame.image.load("assets/queenW.png")
    blackQueen = pygame.image.load("assets/queenB.png")
    whiteKing = pygame.image.load("assets/kingW.png")
    blackKing = pygame.image.load("assets/kingB.png")

    screen.fill((255,255,255))
    screen.blit(chessBoard, (288,0))

    # thinking of making a list for game pieces?
    # maybe just loop through em

    #builds the pieceDict
    for pawnI in range(8):
        pieceDict[(6,pawnI)] = gamePiece(whitePawn, 'p', (6,pawnI), 'w')
        pieceDict[(1,pawnI)] = gamePiece(blackPawn, 'p', (1,pawnI), 'b')
    #Rooks
    pieceDict[(7,0)] = gamePiece(whiteRook, 'r', (7,0), 'w')
    pieceDict[(7,7)] = gamePiece(whiteRook, 'r', (7,7), 'w')
    pieceDict[(0,0)] = gamePiece(blackRook, 'r', (0,0), 'b')
    pieceDict[(0,7)] = gamePiece(blackRook, 'r', (0,7), 'b')
    #Knights
    pieceDict[(7,1)] = gamePiece(whiteKnight, 'n', (7,1), 'w')
    pieceDict[(7,6)] = gamePiece(whiteKnight, 'n', (7,6), 'w')
    pieceDict[(0,1)] = gamePiece(blackKnight, 'n', (0,1), 'b')
    pieceDict[(0,6)] = gamePiece(blackKnight, 'n', (0,6), 'b')
    #Bishops
    pieceDict[(7,2)] = gamePiece(whiteBishop, 'b', (7,2), 'w')
    pieceDict[(7,5)] = gamePiece(whiteBishop, 'b', (7,5), 'w')
    pieceDict[(0,2)] = gamePiece(blackBishop, 'b', (0,2), 'b')
    pieceDict[(0,5)] = gamePiece(blackBishop, 'b', (0,5), 'b')
    #Queens
    pieceDict[(7,3)] = gamePiece(whiteQueen, 'q', (7,3), 'w')
    pieceDict[(0,3)] = gamePiece(blackQueen, 'q', (0,3), 'b')
    #Kings
    pieceDict[(7,4)] = gamePiece(whiteKing, 'k', (7,4), 'w')
    pieceDict[(0,4)] = gamePiece(blackKing, 'k', (0,4), 'b')

    # all pieces displayed by this
    for _, piece in pieceDict.items():
        screen.blit(piece.Piece, piece.getPos())

    #Text
    message_display('Game Time:', (5,0))
    message_display('Play Timer:', (5,70))
    message_display('Captured by AI', (805,0))
    message_display('Captured by User', (805,256))
    
    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()
    #pygame.display.update() need to figure out difference

    #clock = pygame.time.Clock()
    
    # define a variable to control the main loop
    running = True
    
    # main loop
    while running:
        message_display(calcClock(startTime, time.time()), (5,35))
        message_display(calcTimer(startTime,time.time()), (5,105))
        pygame.display.update()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # detection for clicking on a piece
                for _, piece in pieceDict.items():
                    if piece.Color == 'w':
                        pieceRect = piece.Piece.get_rect()
                        xp, yp = piece.getPos()
                        pieceRect.x = xp
                        pieceRect.y = yp
                        if pieceRect.collidepoint(x, y):
                            pieceClicked = piece
                            removePastHighlight()
                            highlightPiece(pieceRect)
                            highlightMoves(piece, pieceRect)
                            pygame.display.update()
                #move detection
                if pieceClicked != None:
                    for move, boardPos in moveClickList:
                        if move.collidepoint(x, y):
                            del pieceDict[pieceClicked.Pos]
                            pieceClicked.movePiece(boardPos)
                            pieceDict[boardPos] = pieceClicked
                            removePastHighlight()
                            pieceClicked = None
                            pygame.display.update()
                            break
            # only do something if the event is of type QUIT
            elif event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

def highlightPiece(pieceRect):
    high = pygame.Surface(pieceRect.size)
    high.set_alpha(100)
    high.fill((230, 255, 41)) 
    screen.blit(high, (pieceRect.x,pieceRect.y))

def removePastHighlight():
    del moveClickList[0:-1]
    screen.blit(chessBoard, (288,0))
    for _, piece in pieceDict.items():
        #print(piece.Pos)
        screen.blit(piece.Piece, piece.getPos())

def highlightMoves(piece, pieceRect):
    list = moveList(piece)
    for place in list:
        high = pygame.Surface(pieceRect.size)
        high.set_alpha(100)
        high.fill((230, 255, 41)) 
        thing = screen.blit(high, getBoard(place))
        moveClickList.append((thing, place))

def calcClock(timeStart, currentTime):
    secs = int(currentTime - timeStart)
    hours = int(secs/3600)
    secs = secs - 3600 * hours
    mins = int(secs/60)
    secs = secs - 60 * mins
    clock = '%s:%s:%s' % (str(hours).zfill(2), str(mins).zfill(2), str(secs).zfill(2))
    return str(clock)

def calcTimer(timeStart, currentTime):
    secs = int(currentTime - timeStart)
    secs = playClockTime - secs
    mins = int(secs/60)
    secs = secs - 60 * mins
    clock = '%s:%s' % (str(mins).zfill(2), str(secs).zfill(2))
    return str(clock)

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text, pos):
    mediumText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, mediumText)
    TextRect = (pos[0],pos[1])
    width, height = mediumText.size(text)
    pygame.draw.rect(screen, (255,255,255), (pos[0], pos[1], width+2, height))
    screen.blit(TextSurf, TextRect)

def buildBoardSpaces():
    padding = int((boardSquareSize-pieceSize)/2)
    for col in range(0, 8):
        colSpace = boardSquareSize * col + padding + 288
        for row in range(0, 8):
            rowSpace = boardSquareSize * row + padding
            board[(row,col)] = (colSpace, rowSpace)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    buildBoardSpaces()
    main()