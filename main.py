#main.py v1.0
#Grant Ludwig

# import the pygame module, so you can use it
import pygame
 
# define a main function
def main():
     
    # initialize the pygame module
	pygame.init()
    # load and set the logo
	logo = pygame.image.load("pawnW.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("basic testing")

	screen_width = 800
	screen_height = 512
     
	screen = pygame.display.set_mode((screen_width,screen_height))

    # load image (it is in same directory)
	whitePawn = pygame.image.load("pawnW.png")
	blackPawn = pygame.image.load("pawnB.png")
	board = pygame.image.load("board.png")

	screen.fill((255,255,255))
	screen.blit(board, (0,0))

    
    # and blit it on screen
	screen.blit(whitePawn, (9, 9))
	screen.blit(blackPawn, (73, 9))
	screen.blit(blackPawn, (9, 73))
    
    # update the screen to make the changes visible (fullscreen update)
	pygame.display.flip()

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
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
	main()