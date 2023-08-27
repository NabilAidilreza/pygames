import pygame
import math
import random

def main():

    # init game
    pygame.init()
    clock= pygame.time.Clock()
    score_font= pygame.font.Font(None, 30)
    gameover_font = pygame.font.Font(None, 100)
    score = 0

    # timer to create enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 150)

    # game variables
    width = 700
    height = 700
    gamestate = "PLAY"
    timer = 0

    player_size = 30
    player_speed = 4
    x = width/3
    y = height/2
    bullet_color = (255,255,255)
    bullet_speed = 10
    bullet_size = 6
    player_bullet_list = [] # stores [bullet_x, bullet_y, bullet_angleFromGround]

    enemy_size = 25
    enemy_color = (220,20,60)
    enemy_list = []
    enemy_speed = 5
    enemy_bullet_list = []
    enemy_bullet_spd = 10
    UP = False

    # display
    screen = pygame.display.set_mode( (width, height) )


    def get_inputs_pro():
        nonlocal x, y, player_speed, gamestate, bullet_speed, enemy_size, enemy_list,UP 

        # one time events
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                gamestate = "END"
            # keydown
            if event.type == pygame.KEYDOWN:
                #pause/play
                if event.key == pygame.K_ESCAPE:
                    if gamestate == "PAUSE":
                        gamestate = "PLAY"
                    elif gamestate == "PLAY":
                        gamestate = "PAUSE"
                if event.key == pygame.K_SPACE:
                    if UP == False:
                        UP = True
                    elif UP == True:
                        UP = False
            if event.type == ADDENEMY and gamestate == "PLAY":
                grid_x = width/enemy_size-1
                grid_y = height/enemy_size-1
                enemy_loc = [grid_x,random.randint(0,grid_y)]
                enemy_x_dir = -1
                enemy_list.append([enemy_loc[0]*enemy_size+enemy_size/2, enemy_loc[1]*enemy_size+enemy_size/2, enemy_x_dir])

    def get_inputs():
        nonlocal x,y,player_speed,player_bullet_list,UP

##        pygame.event.get()
##        pressed = pygame.key.get_pressed()
##        # held-down keys
##        if pressed[pygame.K_w]:
##            y -= player_speed
####        if pressed[pygame.K_a]:
####            x -= player_speed
##        if pressed[pygame.K_s]:
##            y += player_speed
####        if pressed[pygame.K_d]:
####            x += player_speed

            
    def process_player_related():
        nonlocal x, y, width, height, bullet_speed,player_speed
        
        # screen boundary
        if x < player_size/2:
            x = player_size/2
        if x > width-player_size/2:
            x = width-player_size/2
        if y < player_size/2:
            y = player_size/2
        if y > height-player_size/2:
            y = height-player_size/2

        if UP == True:
            y -= player_speed
        else:
            y += player_speed
    def process_enemy_related():
        nonlocal enemy_list, enemy_bullet_list, enemy_speed
    
        for enemy in enemy_list:
            enemy[0] += enemy_speed * enemy[2]


    def process_collisions():
        nonlocal enemy_list, x, y, gamestate, score
        
        for enemy in enemy_list:
            if ((x-enemy[0])**2+(y-enemy[1])**2)**0.5 < player_size:
                gamestate = "GAMEOVER"
                
    def display():
        # draw screen
        screen.fill((255,255,255))

        # draw player
        pygame.draw.ellipse( screen, (0,0,255), pygame.Rect(x-player_size/2, y-player_size/2, player_size, player_size))

        # draw enemy
        for enemy in enemy_list:
            pygame.draw.ellipse( screen, enemy_color, pygame.Rect(enemy[0]-enemy_size/2,enemy[1]-enemy_size/2,enemy_size,enemy_size) )

        # update
        pygame.display.flip()
        clock.tick(60)

    while gamestate != "END":
        get_inputs_pro()
        if gamestate == "PLAY":
            get_inputs()
            process_player_related()
            process_enemy_related()
            process_collisions()
        elif gamestate == "GAMEOVER":
            screen.blit( gameover_font.render("GAMEOVER", True,(0,0,0)), (150,height/2) )
            if sum(pygame.mouse.get_pressed()):
                main()
            pygame.display.flip()
            clock.tick(2)
        display()

    pygame.quit()

main()
