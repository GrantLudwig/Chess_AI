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

    xpos = 50
    ypos = 50
    xother = 300
    yother = 300
    # how many pixels we move our smily each frame
    step_x = 10
    step_y = 5
    step_xother = 5
    step_yother = 10
    
    # and blit it on screen
    screen.blit(whitePawn, (xpos, ypos))
    screen.blit(blackPawn, (xother, yother))
    
    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()

    clock = pygame.time.Clock()
     
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
        if xpos>screen_width-64 or xpos<0:
            step_x = -step_x
        if ypos>screen_height-64 or ypos<0:
            step_y = -step_y
        if xother>screen_width-64 or xother<0:
            step_xother = -step_xother
        if yother>screen_height-64 or yother<0:
            step_yother = -step_yother
        # update the position of the smily
        xpos += step_x # move it to the right
        ypos += step_y # move it down
        xother += step_xother # move it to the right
        yother += step_yother # move it down
        
        # first erase the screen (just blit the background over anything on screen)
        screen.fill((255,255,255))
        screen.blit(board, (0,0))
        # now blit the smily on screen
        screen.blit(whitePawn, (xpos, ypos))
        screen.blit(blackPawn, (xother, yother))
        # and update the screen (dont forget that!)
        pygame.display.flip()
        
        # this will slow it down to 10 fps, so you can watch it, 
        # otherwise it would run too fast
        clock.tick(60)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()