#main.py v1.0
#Grant Ludwig

# import the pygame module, so you can use it
import pygame

boardSquareSize = 64
pieceSize = 45
board = {}
screen_width = 800
screen_height = 512
screen = pygame.display.set_mode((screen_width,screen_height))

def getBoard(row, col):
    return board[(row,col)]
 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("pawnW.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Chess")

    # load image (it is in same directory)
    whitePawn = pygame.image.load("pawnW.png")
    blackPawn = pygame.image.load("pawnB.png")
    whiteRook = pygame.image.load("rookW.png")
    blackRook = pygame.image.load("rookB.png")
    whiteKnight = pygame.image.load("knightW.png")
    blackKnight = pygame.image.load("knightB.png")
    whiteBishop = pygame.image.load("bishopW.png")
    blackBishop = pygame.image.load("bishopB.png")
    whiteQueen = pygame.image.load("queenW.png")
    blackQueen = pygame.image.load("queenB.png")
    whiteKing = pygame.image.load("kingW.png")
    blackKing = pygame.image.load("kingB.png")
    board = pygame.image.load("board.png")

    screen.fill((255,255,255))
    screen.blit(board, (0,0))

    
    #Pawns
    for pawnI in range(8):
        screen.blit(whitePawn, getBoard(6,pawnI))
        screen.blit(blackPawn, getBoard(1,pawnI))
    #Rooks
    screen.blit(whiteRook, getBoard(7,0))
    screen.blit(whiteRook, getBoard(7,7))
    screen.blit(blackKnight, getBoard(0,0))
    screen.blit(blackKnight, getBoard(0,7))
    #Knights
    screen.blit(whiteKnight, getBoard(7,1))
    screen.blit(whiteKnight, getBoard(7,6))
    screen.blit(blackRook, getBoard(0,1))
    screen.blit(blackRook, getBoard(0,6))
    #Bishops
    screen.blit(whiteBishop, getBoard(7,2))
    screen.blit(whiteBishop, getBoard(7,5))
    screen.blit(blackBishop, getBoard(0,2))
    screen.blit(blackBishop, getBoard(0,5))
    #Queens
    screen.blit(whiteQueen, getBoard(7,3))
    screen.blit(blackQueen, getBoard(0,3))
    #Kings
    screen.blit(whiteKing, getBoard(7,4))
    screen.blit(blackKing, getBoard(0,4))

    #Text
    message_display('Captured by AI', (517,0))
    message_display('Captured by User', (517,256))
    
    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()
    #pygame.display.update() need to figure out difference

    #clock = pygame.time.Clock()
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # check if the smily is still on screen, if not change direction

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text, pos):
    mediumText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, mediumText)
    TextRect = (pos[0],pos[1])
    screen.blit(TextSurf, TextRect)

def buildBoardSpaces():
    padding = int((boardSquareSize-pieceSize)/2)
    for col in range(0, 8):
        colSpace = boardSquareSize * col + padding
        for row in range(0, 8):
            rowSpace = boardSquareSize * row + padding
            board[(row,col)] = (colSpace, rowSpace)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    buildBoardSpaces()
    main()