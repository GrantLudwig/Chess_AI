#main.py v8.0
#Grant Ludwig and Mitch Downey

# import the pygame module, so you can use it
import pygame
import time
from copy import deepcopy
import sys
from random import random

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
aiDepth = None # how many moves ahead the user wants the ai to look
userTurn = True
nothing = None #for doing nothing
aiCapture = [] #list of pieces captured by ai
userCapture = [] #list of pieces captured by user
moveDict = [] #list of checked moves to speed up ai
wChecked = False
bChecked = False
running = True
bCheckedPieces = []
wCheckedPieces = []
wKing = None
bKing = None

pieceDict = {} # dict of pieces
                #key: (row,col) board
                #value: gamePiece

# generalized class for game pieces
class gamePiece():

    def __init__(self, pieceImg, pieceType, boardPos, color, value):
        self.Piece = pygame.image.tostring(pieceImg,"RGBA") # pygame image of the piece, stored as a string buffer
        self.Pos = boardPos # position of the piece on board, (row,col)
        self.Color = color # single char, 'b' or 'w'
        self.Type = pieceType   # single char, what piece type it is
                                # 'r' = rook, 'n' = knight, 'b' = bishop
                                # 'q' = queen, 'k' = king, 'p' = pawn
        self.First = True # for pawns, if this is their first move or not
        self.Value = value # the value of a piece
        # add more attributes as needed

    def getPiece(self): #return the actual image, retreived from the string buffer
        return pygame.image.frombuffer(self.Piece, (45,45), "RGBA")

    def changePiece(self, img):
        self.Piece = pygame.image.tostring(img,"RGBA")

    def movePiece(self, targetPos):
        self.Pos = targetPos
        self.First = False

    def getPos(self):
        return getBoard(self.Pos)

#returns a list of the moves the piece can make
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
    if piece.Type == 'p': 
        done = False
        if piece.First: #first move
            if allyColor == 'b':
                if (currRow + 1, currCol) in pieceDict:
                    done = True
                else:
                    list.append((currRow + 1, currCol))
                if (currRow + 2, currCol) in pieceDict:
                    nothing = None
                elif not done:
                    list.append((currRow + 2, currCol))
            else:
                if (currRow - 1, currCol) in pieceDict:
                    done = True
                else:
                    list.append((currRow - 1, currCol))
                if (currRow - 2, currCol) in pieceDict and not done:
                    nothing = None
                elif not done:
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
            if currCol + 1 >= 0 and currCol + 1 < 8 and currRow - 1 >= 0 and currRow - 1 < 8:
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

def getBoard(bPos):
    return board[bPos]
 
# define a main function
def main():
    aiDepth = int(sys.argv[1]) * 2
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("assets/pawnW.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Chess")

    # load image
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

    #builds the pieceDict
    for pawnI in range(8):
        pieceDict[(6,pawnI)] = gamePiece(whitePawn, 'p', (6,pawnI), 'w', 10)
        pieceDict[(1,pawnI)] = gamePiece(blackPawn, 'p', (1,pawnI), 'b', -10)
    #Rooks
    pieceDict[(7,0)] = gamePiece(whiteRook, 'r', (7,0), 'w', 50)
    pieceDict[(7,7)] = gamePiece(whiteRook, 'r', (7,7), 'w', 50)
    pieceDict[(0,0)] = gamePiece(blackRook, 'r', (0,0), 'b', -50)
    pieceDict[(0,7)] = gamePiece(blackRook, 'r', (0,7), 'b', -50)
    #Knights
    pieceDict[(7,1)] = gamePiece(whiteKnight, 'n', (7,1), 'w', 30)
    pieceDict[(7,6)] = gamePiece(whiteKnight, 'n', (7,6), 'w', 30)
    pieceDict[(0,1)] = gamePiece(blackKnight, 'n', (0,1), 'b', -30)
    pieceDict[(0,6)] = gamePiece(blackKnight, 'n', (0,6), 'b', -30)
    #Bishops
    pieceDict[(7,2)] = gamePiece(whiteBishop, 'b', (7,2), 'w', 30)
    pieceDict[(7,5)] = gamePiece(whiteBishop, 'b', (7,5), 'w', 30)
    pieceDict[(0,2)] = gamePiece(blackBishop, 'b', (0,2), 'b', -30)
    pieceDict[(0,5)] = gamePiece(blackBishop, 'b', (0,5), 'b', -30)
    #Queens
    pieceDict[(7,3)] = gamePiece(whiteQueen, 'q', (7,3), 'w', 90)
    pieceDict[(0,3)] = gamePiece(blackQueen, 'q', (0,3), 'b', -90)
    #Kings
    pieceDict[(7,4)] = gamePiece(whiteKing, 'k', (7,4), 'w', 9000)
    pieceDict[(0,4)] = gamePiece(blackKing, 'k', (0,4), 'b', -9000)

    # all pieces displayed by this
    displayPieces()

    #Text
    message_display('Game Time:', (5,0))
    message_display('Captured by AI', (805,0))
    message_display('Captured by User', (805,256))
    
    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()
    
    # define a variable to control the main loop
    pygame.display.update()
    useless = 0
    global running
    global userTurn
    global pieceClicked

    # main loop
    global moveDict

    while running:
        message_display(calcClock(startTime, time.time()), (5,35))
        pygame.display.update()
        #AI
        if not userTurn:
            kingChecked()
            useless, targetMove, targetPiece = deepBlue(aiDepth, pieceDict, -100000, 100000, False)
            aiPiece = pieceDict[targetPiece]
            del pieceDict[aiPiece.Pos]
            aiPiece.movePiece(targetMove)
            if targetMove in pieceDict:
                aiCapture.append(pieceDict[targetMove].getPiece())
                updateCapture(False)
            pieceDict[targetMove] = aiPiece
            removePastHighlight()
            pawnCheck(whiteQueen)
            pygame.display.update()
            kingChecked()
            userTurn = True
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if userTurn:
                kingChecked()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # detection for clicking on a piece
                    for _, piece in pieceDict.items():
                        if piece.Color == 'w':
                            pieceRect = piece.getPiece().get_rect()
                            xp, yp = piece.getPos()
                            pieceRect.x = xp
                            pieceRect.y = yp
                            if pieceRect.collidepoint(x, y):
                                removePastHighlight()
                                highlightPiece(pieceRect)
                                done = highlightMoves(piece, pieceRect)
                                if done:
                                    endGame(True)
                                pieceClicked = piece
                                pygame.display.update()
                                break
                    #move detection
                    if pieceClicked != None:
                        for move, boardPos in moveClickList:
                            if move.collidepoint(x, y):
                                del pieceDict[pieceClicked.Pos]
                                pieceClicked.movePiece(boardPos)
                                #attack check
                                if boardPos in pieceDict:
                                    userCapture.append(pieceDict[boardPos].getPiece())
                                    updateCapture(True)
                                pieceDict[boardPos] = pieceClicked
                                removePastHighlight()
                                pieceClicked = None
                                pawnCheck(whiteQueen)
                                pygame.display.update()
                                kingChecked()
                                userTurn = False
                                break
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

#Chess Ai
#returns best value, move position, piece position
#uses minimax algorithm with alpha-beta pruning
def deepBlue(depth, gameBoard, alpha, beta, maxWhite):
    global moveDict
    global wChecked
    global bChecked
    list = []
    if depth < 1:
        totalValue = 0
        for _, piece in gameBoard.items():
            totalValue = totalValue + piece.Value
        return totalValue, (-1,-1), (-1,-1)
    if maxWhite: #white pieces
        bestValue = -99999
        bestMove = None
        bestPiece = None
        for _, piece in gameBoard.items():
            if piece.Color == 'w':
                list.append(piece)
        for piece in list:
            moves = None
            if wChecked:
                moves, done = checkedMoves(piece)
                if done:
                    return -1000000, (-1,-1), (-1,-1)
            else:
                moves = moveList(piece)
            for move in moves:
                oldPos = deepcopy(piece.Pos)
                mimicBoard = deepcopy(gameBoard)
                del mimicBoard[oldPos]
                piece.movePiece(move)
                mimicBoard[move] = piece
                kingChecked()
                if (oldPos, move, depth,alpha,bestValue) not in moveDict: #pruning moves that have already been checked to improve efficiency
                    potentialBestValue, _, _ = deepBlue(depth - 1, mimicBoard, alpha, beta, not maxWhite)
                    moveDict.append((oldPos, move, depth,alpha,bestValue))
                    if bestValue < potentialBestValue:
                        moveDict.remove((oldPos, move, depth, alpha,bestValue))
                        bestValue = potentialBestValue
                del mimicBoard[move]
                piece.movePiece(oldPos)
                mimicBoard[oldPos] = piece
                kingChecked()
                if alpha < bestValue:
                    alpha = bestValue
                if beta <= alpha:
                    return bestValue, None, None
        if bestValue == 99999:
            bestValue = 0
        return bestValue, None, None
    else: #black pieces
        bestMove = None
        bestPiece = None
        bestValue = 99999
        changeIt = False
        for _, piece in gameBoard.items():
            if piece.Color == 'b':
                list.append(piece)
        for piece in list:
            moves = None
            if bChecked:
                moves, done = checkedMoves(piece)
                if done:
                    return 1000000, (-1,-1), (-1,-1)
            else:
                moves = moveList(piece)
            for move in moves:
                oldPos = deepcopy(piece.Pos)
                mimicBoard = deepcopy(gameBoard)
                del mimicBoard[oldPos]
                piece.movePiece(move)
                mimicBoard[move] = piece
                kingChecked()
                if (oldPos, move, depth, beta,bestValue) not in moveDict: #pruning moves that have already been checked to improve efficiency
                    potentialBestValue, _, _ = deepBlue(depth - 1, mimicBoard, alpha, beta, not maxWhite)
                    moveDict.append((oldPos, move, depth, beta,bestValue))
                    if bestValue > potentialBestValue:
                        moveDict.remove((oldPos, move, depth, beta,bestValue))
                        changeIt = True
                del mimicBoard[move]
                piece.movePiece(oldPos)
                mimicBoard[oldPos] = piece
                kingChecked()
                if changeIt:
                    bestValue = potentialBestValue
                    bestMove = move
                    bestPiece = piece.Pos
                if beta > bestValue:
                    beta = bestValue
                if beta <= alpha:
                    return bestValue, bestMove, bestPiece
                changeIt = False
            if bestPiece == None and len(moves) > 0:
                bestMove = moves[0]
                bestPiece = piece.Pos
        if bestValue == -99999:
            bestValue = 0
        return bestValue, bestMove, bestPiece


def displayPieces():
    for _, piece in pieceDict.items():
        screen.blit(piece.getPiece(), piece.getPos())

def updateCapture(user): #move a captured piece to its appropriate location to the right of the game board
    if not user:
        #update AI
        for i in range(0,len(aiCapture)):
            if i < 5:
                screen.blit(aiCapture[i], (805 + i * 50, 35))
            elif i < 10:
                screen.blit(aiCapture[i], (805 + (i - 5) * 50, 85))
            elif i < 15:
                screen.blit(aiCapture[i], (805 + (i - 10) * 50, 135))
    else:
        #update user
        for i in range(0,len(userCapture)):
            if i < 5:
                screen.blit(userCapture[i], (805 + i * 50, 291))
            elif i < 10:
                screen.blit(userCapture[i], (805 + (i - 5) * 50, 341))
            elif i < 15:
                screen.blit(userCapture[i], (805 + (i - 10) * 50, 391))


def highlightPiece(pieceRect):
    high = pygame.Surface(pieceRect.size)
    high.set_alpha(100)
    high.fill((230, 255, 41)) 
    screen.blit(high, (pieceRect.x,pieceRect.y))

def removePastHighlight():
    moveClickList.clear()
    screen.blit(chessBoard, (288,0))
    displayPieces()

def highlightMoves(piece, pieceRect):
    global wChecked
    global bChecked
    list = []
    if wChecked:
        list, done = checkedMoves(piece)
        if done:
            return True
    else:
        list = moveList(piece)
    for place in list:
        high = pygame.Surface(pieceRect.size)
        high.set_alpha(100)
        high.fill((230, 255, 41)) 
        thing = screen.blit(high, getBoard(place))
        moveClickList.append((thing, place))

def pawnCheck(queenImage):
    for _, piece in pieceDict.items():
        if piece.Type == 'p':
            if piece.Color == 'w':
                row, _ = piece.Pos
                if row == 0:
                    piece.Type = 'q'
                    piece.changePiece(queenImage)
                    piece.Value = 90
                    pieceDict[piece.Pos] = piece
            else:
                row, _ = piece.Pos
                if row == 7:
                    piece.Type = 'q'
                    piece.changePiece(queenImage)
                    piece.Value = -90
                    pieceDict[piece.Pos] = piece

def kingChecked(): #determining if a king has been checked
    global wChecked
    global bChecked
    global bCheckedPieces
    global wCheckedPieces
    global wKing
    global bKing
    wKing = None
    bKing = None
    whitePieceList = []
    blackPieceList = []
    changedW = False
    changedB = False
    for _, piece in pieceDict.items():
        if piece.Color == 'b': #white checked
            if piece.Type == 'k':
                bKing = piece.Pos
            blackPieceList.append(piece)
        else: #black checked
            if piece.Type == 'k':
                wKing = piece.Pos
            whitePieceList.append(piece)
    if wKing == None:
        endGame(True)
    elif bKing == None:
        endGame(False)
    for singlePiece in blackPieceList:
        moves = moveList(singlePiece)
        for move in moves:
            if move == wKing:
                wChecked = True
                wCheckedPieces.append(singlePiece.Pos)
                changedW = True
    if not changedW:
        wChecked = False
        wCheckedPieces.clear()
    for singlePiece in whitePieceList:
        moves = moveList(singlePiece)
        for move in moves:
            if move == wKing:
                bChecked = True
                bCheckedPieces.append(singlePiece.Pos)
                changedB = True
    if not changedB:
        bChecked = False
        bCheckedPieces.clear()

# return move list, return true if game dead
def checkedMoves(piece): #evaluates which moves can be done in a Checked state
    global wChecked
    global bChecked
    global wKing
    global bKing
    pieceList = []
    list = [] #list of moves king can do
    if piece.Type == 'k':
        currRow, currCol = piece.Pos
        allyColor = piece.Color
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
        #now prune moves
        if piece.Color == 'w' and wChecked:
            for _, otherPiece in pieceDict.items():
                if otherPiece.Color == 'b':
                    pieceList.append(otherPiece)
            for singlePiece in pieceList:
                moves = []
                if singlePiece.Type == 'p':
                    currRow, currCol = singlePiece.Pos
                    allyColor = singlePiece.Color
                    #right
                    if currCol + 1 >= 0 and currCol + 1 < 8 and currRow + 1 >= 0 and currRow + 1 < 8:
                        if (currRow + 1, currCol + 1) in pieceDict:
                            if pieceDict[(currRow + 1, currCol + 1)].Color != allyColor:
                                moves.append((currRow + 1, currCol + 1))
                    #left
                    if currCol - 1 >= 0 and currCol - 1 < 8 and currRow + 1 >= 0 and currRow + 1 < 8:
                        if (currRow + 1, currCol - 1) in pieceDict:
                            if pieceDict[(currRow + 1, currCol - 1)].Color != allyColor:
                                moves.append((currRow + 1, currCol - 1))
                else:
                    moves = moveList(singlePiece)
                for move in moves:
                    if move in list:
                        list.remove(move)
        elif piece.Color == 'b' and bChecked:
            for _, otherPiece in pieceDict.items():
                if otherPiece.Color == 'w':
                    pieceList.append(otherPiece)
            for singlePiece in pieceList:
                moves = []
                if singlePiece.Type == 'p':
                    currRow, currCol = singlePiece.Pos
                    allyColor = singlePiece.Color
                    #right
                    if currCol + 1 >= 0 and currCol + 1 < 8 and currRow - 1 >= 0 and currRow - 1 < 8:
                        if (currRow - 1, currCol + 1) in pieceDict:
                            if pieceDict[(currRow - 1, currCol + 1)].Color != allyColor:
                                moves.append((currRow - 1, currCol + 1))
                    #left
                    if currCol - 1 >= 0 and currCol - 1 < 8 and currRow - 1 >= 0 and currRow - 1 < 8:
                        if (currRow - 1, currCol - 1) in pieceDict:
                            if pieceDict[(currRow - 1, currCol - 1)].Color != allyColor:
                                moves.append((currRow - 1, currCol - 1))
                else:
                    moves = moveList(singlePiece)
                for move in moves:
                    if move in list:
                        list.remove(move)
        if len(list) < 1:
            return list, True
        #future checking
        actualList = []
        for move in list:
            oldPos = deepcopy(piece.Pos)
            del pieceDict[oldPos]
            piece.movePiece(move)
            pieceDict[move] = piece
            kingChecked()
            if piece.Color == 'b':
                if not bChecked:
                    actualList.append(move)
            else:
                if not wChecked:
                    actualList.append(move)
            del pieceDict[move]
            piece.movePiece(oldPos)
            pieceDict[oldPos] = piece
        kingChecked()
        return actualList, False
    else: #determines what moves a non-king piece can make in a "checked" state
        list = moveList(piece)
        actualMoves = []
        for move in list:
            if piece.Color == 'b':
                if move in bCheckedPieces or blocked(bCheckedPieces, move, bKing):
                    actualMoves.append(move)
            else:
                if move in wCheckedPieces or blocked(wCheckedPieces, move, wKing):
                    actualMoves.append(move)
        if len(actualMoves) < 1:
            actualMoves, True
        return actualMoves, False

def blocked(checkedPieces, move, kingPos): #determines if a piece can "block" a check
    rKing, cKing = kingPos
    rMove, cMove = move
    for pos in checkedPieces:
        checkedR, checkedC = pos
        #hor
        if checkedR == rKing and rMove == checkedR:
            if checkedC < cKing and cMove < cKing and cMove > checkedC:
                return True
            elif checkedC > cKing and cMove > cKing and cMove < checkedC:
                return True
        #vert
        if checkedC == cKing and cMove == checkedC:
            if checkedR < rKing and rMove < rKing and rMove > checkedR:
                return True
            elif checkedR > rKing and rMove > rKing and rMove < checkedR:
                return True
        diagList = []
        #diag
        #up left
        for row, col in zip(range(rKing - 1, checkedR, -1), range(cKing - 1, checkedC, -1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                diagList.append((row, col))
        #up right
        for row, col in zip(range(rKing - 1, checkedR, -1), range(cKing + 1, checkedC, 1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                diagList.append((row, col))
        #down left
        for row, col in zip(range(rKing + 1, checkedR, 1), range(cKing - 1, checkedC, -1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                diagList.append((row, col))
        #down right
        for row, col in zip(range(rKing + 1, checkedR, 1), range(cKing + 1, checkedC, 1)):
            if col >= 0 and col < 8 and row >= 0 and row < 8:
                diagList.append((row, col))
        if move in diagList:
            return True
    return False

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
    pygame.display.update()


def buildBoardSpaces():
    padding = int((boardSquareSize-pieceSize)/2)
    for col in range(0, 8):
        colSpace = boardSquareSize * col + padding + 288
        for row in range(0, 8):
            rowSpace = boardSquareSize * row + padding
            board[(row,col)] = (colSpace, rowSpace)

def endGame(userLose):
    global running
    if userLose:
        message_display('The AI Won', (5,105))
        pygame.display.update()
        time.sleep(10)
        running = False
    else:
        message_display('You Won', (5,105))
        pygame.display.update()
        time.sleep(10)
        running = False


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    buildBoardSpaces()
    main()