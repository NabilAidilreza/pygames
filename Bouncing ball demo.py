import pygame
import os
import math
import random
os.environ["SDL_VIDEO_CENTERED"] = "1" # Centers game window

def main():

    # init game
    pygame.init()
    clock = pygame.time.Clock()

    # variables
    gs = "PLAY"
    width = 800
    height = 700

    color = (0,255,255)

    size = 10
    angle = 45*(math.pi/180)
    speed = 15
    num_of_ball = 100
    ballloclist = [] #[width/2, height/2] # x, y, color
    ballvellist = [] #[speed*math.cos(angle), speed*math.sin(angle)] #Vx, Vy
    for i in range(num_of_ball):
        color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        ballloclist.append([random.randint(size,width-size), random.randint(size,height-size), color])
        ballvellist.append([speed*math.cos(angle), speed*math.sin(angle)])

    # display
    screen = pygame.display.set_mode( (width, height) )

    def get_inputs():
        nonlocal gs
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                gs = "END"
                
    def process_game_objects():
        for i in range(len(ballloclist)):
            ballloclist[i][0] += ballvellist[i][0]
            ballloclist[i][1] += ballvellist[i][1]

            if ballloclist[i][0] < size//2 or ballloclist[i][0] > width-size//2:
                ballvellist[i][0] *= -1
            if ballloclist[i][1] < size//2 or ballloclist[i][1] > height-size//2:
                ballvellist[i][1] *= -1

    def display():
        # draw screen
        screen.fill((0,0,0))

        # draw ball
        for ballloc in ballloclist:
            pygame.draw.ellipse(screen,ballloc[2], pygame.Rect(ballloc[0]-size//2,ballloc[1]-size//2,size,size))

        # update
        pygame.display.flip()
        clock.tick(60)

    while gs != "END":
        get_inputs()
        process_game_objects()
        display()
    pygame.quit()

main()
