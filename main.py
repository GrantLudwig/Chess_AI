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

#trying something out here
pieceList = [] # list of all pieces, for purposes of display...i think?
posBoard = [['ee' for x in range(8)] for y in range(8)] 
# 2d list representing the board, each location is one square
# For example, a black pawn would be 'bp', empty is 'ee'

# generalized class for game pieces
class gamePiece():

    def __init__(self, pieceImg, pieceType, initPos, color):
        self.Piece = pieceImg # pygame image of the piece
        self.Pos = initPos # position of the piece, type = (float,float)
        self.Color = color # single char, 'b' or 'w'
        self.Type = pieceType # single char, what piece type it is
        self.First = True # for pawns, if this is their first move or not
        # 'r' = rook, 'n' = knight, 'b' = bishop
        # 'q' = queen, 'k' = king, 'p' = pawn
        # add more attributes as needed

    def movePiece(self, targetPos):
        #if validMove(targetPos):  # need to iron out required variables/rethink how position is stored
            self.Pos = targetPos

    def getPos(self):
        return self.Pos


# DUE TO HOW POSITIONS ARE CURRENTLY STORED, THIS FUNCTION WILL NOT WORK
# need to rework position storage before implementing this
def validMove(piece, targetPos, currentPos):
    curY,curX = currentPos
    tarY,tarX = targetPos
    allyColor = piece.Color
    enemyColor = ''
    if allyColor == 'b':
        enemyColor =  'w'
    else:
        enemyColor = 'b'
    if piece.Type == 'p': #pawn
        if piece.First: #first move
            if tarY - curY <= 2: #within range
                if posBoard[tarY][tarX] == 'ee' and posBoard[curY + 1][curX] == 'ee': #empty space
                    return True
                elif posBoard[tarY][tarX][0] == enemyColor:
                    return True
        elif tarY - curY <= 1: #within range
                if posBoard[tarY][tarX] == 'ee': #empty space
                    return True
                elif posBoard[tarY][tarX][0] == enemyColor:
                    return True
    elif pieceType == 'r': #rooks
        if tarX == curX:
            for y in range(curY + 1,tarY):
                if posBoard[y][curX] != 'ee':
                    if posBoard[y][curX][0] == enemyColor:
                        return True
                    else:
                        return False
        elif tarY == curY:
            for x in range(curX + 1,tarX):
                if posBoard[curY][x] != 'ee':
                    if posBoard[curY][x][0] == enemyColor:
                        return True
                    else:
                        return False
    elif pieceType == 'n': #knights
        if (abs(curY - tarY) == 3 and abs(curX - tarX) == 1) or (abs(curY - tarY) == 1 and abs(curX - tarX) == 3):
            if posBoard[tarY][tarX][0] == enemyColor:
                return True
    elif pieceType == 'b': #bishops
        return False #placeholder
    elif pieceType == 'k': #kings
        return False #placeholder
    elif pieceType == 'q': #queens
        return False #placeholder

    return False


def getBoard(row, col):
    return board[(row,col)]
 
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

    #Real
    #Pawns
    #for pawnI in range(8):
    #    screen.blit(whitePawn, getBoard(6,pawnI))
    #    screen.blit(blackPawn, getBoard(1,pawnI))
    #Rooks
    #screen.blit(whiteRook, getBoard(7,0))
    #screen.blit(whiteRook, getBoard(7,7))
    #screen.blit(blackKnight, getBoard(0,0))
    #screen.blit(blackKnight, getBoard(0,7))
    #Knights
    #screen.blit(whiteKnight, getBoard(7,1))
    #screen.blit(whiteKnight, getBoard(7,6))
    #screen.blit(blackRook, getBoard(0,1))
    #screen.blit(blackRook, getBoard(0,6))
    #Bishops
    #screen.blit(whiteBishop, getBoard(7,2))
    #screen.blit(whiteBishop, getBoard(7,5))
    #screen.blit(blackBishop, getBoard(0,2))
    #screen.blit(blackBishop, getBoard(0,5))
    #Queens
    #screen.blit(whiteQueen, getBoard(7,3))
    #screen.blit(blackQueen, getBoard(0,3))
    #Kings
    #screen.blit(whiteKing, getBoard(7,4))
    #screen.blit(blackKing, getBoard(0,4))
    #hi

    # generalized piece initialization
    for pawnI in range(8):
        pieceList.append(gamePiece(whitePawn, 'p', getBoard(6,pawnI), 'w'))
        posBoard[6][pawnI] = 'wp'
        pieceList.append(gamePiece(blackPawn, 'p', getBoard(1,pawnI), 'b'))
        posBoard[1][pawnI] = 'bp'
    #Rooks
    pieceList.append(gamePiece(whiteRook, 'r', getBoard(7,0), 'w'))
    pieceList.append(gamePiece(whiteRook, 'r', getBoard(7,7), 'w'))
    posBoard[7][0] = 'wr'
    posBoard[7][7] = 'wr'
    pieceList.append(gamePiece(blackRook, 'r', getBoard(0,0), 'b'))
    pieceList.append(gamePiece(blackRook, 'r', getBoard(0,7), 'b'))
    posBoard[0][0] = 'br'
    posBoard[0][7] = 'br'
    #Knights
    pieceList.append(gamePiece(whiteKnight, 'n', getBoard(7,1), 'w'))
    pieceList.append(gamePiece(whiteKnight, 'n', getBoard(7,6), 'w'))
    posBoard[7][1] = 'wn'
    posBoard[7][6] = 'wn'
    pieceList.append(gamePiece(blackKnight, 'n', getBoard(0,1), 'b'))
    pieceList.append(gamePiece(blackKnight, 'n', getBoard(0,6), 'b'))
    posBoard[0][1] = 'bn'
    posBoard[0][6] = 'bn'
    #Bishops
    pieceList.append(gamePiece(whiteBishop, 'b', getBoard(7,2), 'w'))
    pieceList.append(gamePiece(whiteBishop, 'b', getBoard(7,5), 'w'))
    posBoard[7][2] = 'wb'
    posBoard[7][5] = 'wb'
    pieceList.append(gamePiece(blackBishop, 'b', getBoard(0,2), 'b'))
    pieceList.append(gamePiece(blackBishop, 'b', getBoard(0,5), 'b'))
    posBoard[0][2] = 'bb'
    posBoard[0][5] = 'bb'
    #Queens
    pieceList.append(gamePiece(whiteQueen, 'q', getBoard(7,3), 'w'))
    pieceList.append(gamePiece(blackQueen, 'q', getBoard(0,3), 'b'))
    posBoard[7][3] = 'wq'
    posBoard[0][3] = 'bq'
    #Kings
    pieceList.append(gamePiece(whiteKing, 'k', getBoard(7,4), 'w'))
    pieceList.append(gamePiece(blackKing, 'k', getBoard(0,4), 'b'))
    posBoard[7][4] = 'wk'
    posBoard[0][4] = 'bk'

    # all pieces displayed by this
    for piece in pieceList:
        screen.blit(piece.Piece, piece.getPos())

    ##Fake
    #screen.blit(whitePawn, getBoard(6,0)) #g
    #screen.blit(whitePawn, getBoard(3,1)) #g
    #screen.blit(whitePawn, getBoard(6,2)) #g
    #screen.blit(whitePawn, getBoard(5,3)) #g
    #screen.blit(whitePawn, getBoard(3,4)) #g
    #screen.blit(whitePawn, (805, 35)) #g
    #screen.blit(whitePawn, getBoard(6,6)) #g
    #screen.blit(whitePawn, getBoard(6,7)) #g
    #screen.blit(blackPawn, getBoard(1,0)) #g
    #screen.blit(blackPawn, getBoard(1,1)) #g
    #screen.blit(blackPawn, getBoard(3,2)) #g
    #screen.blit(blackPawn, getBoard(2,3)) #g
    #screen.blit(blackPawn, getBoard(1,4)) #g
    #screen.blit(blackPawn, getBoard(1,5)) #g
    #screen.blit(blackPawn, getBoard(2,6)) #g
    #screen.blit(blackPawn, getBoard(3,7)) #g
    ##Rooks
    #screen.blit(whiteRook, getBoard(7,0)) #g
    #screen.blit(whiteRook, getBoard(7,7)) #g
    #screen.blit(blackKnight, getBoard(0,0)) #g
    #screen.blit(blackKnight, getBoard(0,7)) #g
    ##Knights
    #screen.blit(whiteKnight, (855, 35)) #g
    #screen.blit(whiteKnight, getBoard(7,6)) #g
    #screen.blit(blackRook, (805, 291)) #g
    #screen.blit(blackRook, getBoard(0,6)) #g
    ##Bishops
    #screen.blit(whiteBishop, getBoard(7,2)) #g
    #screen.blit(whiteBishop, getBoard(7,5)) #g
    #screen.blit(blackBishop, getBoard(1,3)) #g
    #screen.blit(blackBishop, getBoard(2,7)) #g
    ##Queens
    #screen.blit(whiteQueen, getBoard(7,3)) #g
    #screen.blit(blackQueen, getBoard(5,2)) #g
    ##Kings
    #screen.blit(whiteKing, getBoard(7,4)) #g
    #screen.blit(blackKing, getBoard(0,4)) #g

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
            # detection for clicking on a piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for piece in pieceList:
                    if piece.Color == 'w':
                        pieceRect = piece.Piece.get_rect()
                        xp, yp = piece.getPos()
                        pieceRect.x = xp
                        pieceRect.y = yp
                        if pieceRect.collidepoint(x, y):
                            removePastHighlight(pieceList)
                            highlightPiece(pieceRect)
                            pygame.display.update()
                #if board.get_rect().collidepoint(x, y):
                #    highlightPiece(board.get_rect())
                #    pygame.display.update()
                #do something here
                    # select what piece you clicked on.
                    # if there's a piece selected, then check if it can move to the
                    # position that you selected.
                    # if yes, move the piece, else do nothing
            # only do something if the event is of type QUIT
            elif event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # check if the smily is still on screen, if not change direction

def highlightPiece(pieceRect):
    high = pygame.Surface(pieceRect.size)
    high.set_alpha(100)
    high.fill((230, 255, 41)) 
    screen.blit(high, (pieceRect.x,pieceRect.y))

def removePastHighlight(pieceList):
    screen.blit(chessBoard, (288,0))
    for piece in pieceList:
        screen.blit(piece.Piece, piece.getPos())

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