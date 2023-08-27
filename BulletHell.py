import pygame
import math
import random
import os
os.environ["SDL_VIDEO_CENTERED"] = "1" # Centers game window
def main():

    # init game
    pygame.init()
    clock= pygame.time.Clock()
    timer = pygame.time.get_ticks()
    score_font= pygame.font.Font(None, 30)
    gameover_font = pygame.font.Font(None, 100)
    score = 0

    # timer to create enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 3000)
    
    # timer to shoot bullet
    SHOOT = pygame.USEREVENT + 2
    pygame.time.set_timer(SHOOT, 100)
    
    # timer to shoot projectile
    ADDBULLET = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDBULLET, 25)
    

    # game variables
    width = 1600
    height = 800
    gamestate = "PLAY"
    timer = 0
    
    # Player #
    player_size = 25
    player_speed = 5
    x = width/2
    y = height/4
    bullet_color = (255,255,255)
    bullet_speed = 10
    bullet_size = 6
    player_bullet_list = [] # stores [bullet_x, bullet_y, bullet_angleFromGround]

    # Static #
    spawner_size = 20
    spawner_color = (255,0,124)
    x_S = width/2
    y_S = height/2
    spawner_bullet_color = (255,192,203)
    spawner_bullet_speed = 3
    spawner_bullet_size = 6
    spawner_bullet_list = [] # stores [bullet_x, bullet_y, bullet_angleFromGround]
    
    # Enemy #    
    enemy_size = 25
    enemy_color = (255,0,124)
    enemy_list = []
    enemy_speed = 3
    shooting = False
    timer = pygame.time.get_ticks()
    
    # display
    screen = pygame.display.set_mode( (width, height) )

    O = 0
    ran_Spiral = random.randint(1,10)
    ran_Distance = random.randint(1,10)
    RAN = 0
    # RAN = random.randint(0,2)
    PERIOD = 5
    def process_game_events():
        nonlocal O,x, y, gamestate, enemy_size, enemy_list,ran_Spiral,ran_Distance,PERIOD,RAN
        # PROCESS GAME EVENTS #
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
            if event.type == pygame.MOUSEBUTTONDOWN :
                shooting = True
                
            else:
                shooting = False
                
            if event.type == ADDENEMY and gamestate == "PLAY":
                PERIOD -= 1
                grid_x = width/enemy_size-1
                grid_y = height/enemy_size-1
                enemy_loc = [[random.randint(0,grid_x),0],[random.randint(0,grid_x),grid_y],[0,random.randint(0,grid_y)],[grid_x,random.randint(0,grid_y)]]
                ran = random.randint(0,3)
                enemy_list.append([enemy_loc[ran][0]*enemy_size+enemy_size/2, enemy_loc[ran][1]*enemy_size+enemy_size/2])

            if event.type == ADDBULLET and gamestate == "PLAY":
                if RAN == 0:
                    spawner_bullet_list.append([x_S,y_S,ran_Spiral+(O*ran_Distance)])
                elif RAN == 1:
                    spawner_bullet_list.append([x_S,y_S,(ran_Spiral+(math.cos(O)*ran_Spiral))*3])
                elif RAN == 2:
                    angle = (math.atan2((math.cos(O*180)+math.pi)/180, (math.sin(O*180)+math.pi)/180))
                    spawner_bullet_list.append([x_S,y_S,angle*2])
                
                O += 1
                if O == 361:
                    O = 0

    def get_inputs():
        nonlocal x,y,player_speed,player_bullet_list,timer
        
        # PLAYER IIPUT #
        pygame.event.get()
        pressed = pygame.key.get_pressed()
        # held-down keys
        if pressed[pygame.K_w]:
            y -= player_speed
        if pressed[pygame.K_a]:
            x -= player_speed
        if pressed[pygame.K_s]:
            y += player_speed
        if pressed[pygame.K_d]:
            x += player_speed
        now = pygame.time.get_ticks()
        # PLAYER SHOOT #
        if pygame.mouse.get_pressed()[0] and now - timer >= 100:
            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos() #Get mouse pos
            rel_x, rel_y = mouse_pos_x - x, mouse_pos_y - y # relative pos
            angle = (math.atan2(rel_y, rel_x)) - (random.randint(-1,1)/10) #angle    # totally not copied from a website
            # add bullet
            player_bullet_list.append( [x, y, angle] )
            timer = now
            
    def process_player_related():
        nonlocal x, y, width, height, bullet_speed
        
        # screen boundary
        if x < player_size/2:
            x = player_size/2
        if x > width-player_size/2:
            x = width-player_size/2
        if y < player_size/2:
            y = player_size/2
        if y > height-player_size/2:
            y = height-player_size/2

        # bullet coords
        for bullet in player_bullet_list:
            x_spd = bullet_speed * math.cos(bullet[2])
            y_spd = bullet_speed * math.sin(bullet[2])
            bullet[0] += x_spd
            bullet[1] += y_spd
            if bullet[0]<-10 or bullet[0]>width or bullet[1]< -10 or bullet[1]>height:
                player_bullet_list.remove(bullet)
                
    def process_enemy_related():
        nonlocal enemy_list, enemy_speed
        # Enemies #
        for enemy in enemy_list:
            min_dist = 1000
            delta_x = x - enemy[0]
            delta_y = y - enemy[1]

            if abs(delta_x) <= min_dist and abs(delta_y) <= min_dist:
                enemy_move_x = abs(delta_x) > abs(delta_y)
                if abs(delta_x) > enemy_speed and abs(delta_x) > enemy_speed:
                   enemy_move_x = random.random() < 0.5
                if enemy_move_x:
                   enemy[0] += min(delta_x, enemy_speed) if delta_x > 0 else max(delta_x, -enemy_speed)
                else:
                   enemy[1] += min(delta_y, enemy_speed) if delta_y > 0 else max(delta_y, -enemy_speed)
                   
        # Spawner #
        # bullet coords
        for bullet in spawner_bullet_list:
            x_spd = spawner_bullet_speed * math.cos(bullet[2])
            y_spd = spawner_bullet_speed * math.sin(bullet[2])
            bullet[0] += x_spd
            bullet[1] += y_spd
            if bullet[0]<-10 or bullet[0]>width or bullet[1]< -10 or bullet[1]>height:
                spawner_bullet_list.remove(bullet)
                
                
    def process_collisions():
        nonlocal enemy_list, x, y, gamestate, score,spawner_bullet_list
        for bullet in spawner_bullet_list:
            if ((x-bullet[0])**2+(y-bullet[1])**2)**0.5 < player_size - 10:
                gamestate = "GAMEOVER"
        for enemy in enemy_list:
            if ((x-enemy[0])**2+(y-enemy[1])**2)**0.5 < player_size:
                gamestate = "GAMEOVER"
                
            for bullet in player_bullet_list:
                if ((enemy[0]-bullet[0])**2+(enemy[1]-bullet[1])**2)**0.5 < (enemy_size+bullet_size)/2:
                    enemy_list.remove(enemy)
                    player_bullet_list.remove(bullet)
                    score += 1
                    break   

    def display():
        # draw screen
        screen.fill((0,0,0))
        # draw player
        pygame.draw.ellipse( screen, (0,188,255), pygame.Rect(x-player_size/2, y-player_size/2, player_size, player_size))

##        # draw enemy
        for enemy in enemy_list:
            pygame.draw.ellipse( screen, enemy_color, pygame.Rect(enemy[0]-enemy_size/2,enemy[1]-enemy_size/2,enemy_size,enemy_size) )
        
        # draw spawner
        pygame.draw.ellipse( screen, (255,0,124), pygame.Rect(x_S-spawner_size/2, y_S-spawner_size/2, spawner_size, spawner_size))

        # draw player bullets
        for bullet in player_bullet_list:
            pygame.draw.ellipse( screen, bullet_color, pygame.Rect(bullet[0]-bullet_size/2, bullet[1]-bullet_size/2, bullet_size,bullet_size))

        # draw spawner bullets
        for bullet in spawner_bullet_list:
            pygame.draw.ellipse( screen, spawner_bullet_color, pygame.Rect(bullet[0]-spawner_bullet_size/2, bullet[1]-spawner_bullet_size/2, spawner_bullet_size,spawner_bullet_size))
            
        # display score
        screen.blit( score_font.render("SCORE: "+str(round(score,2)), True,(255,255,255)), (0,0) )

        # update
        pygame.display.flip()
        clock.tick(60)

    while gamestate != "END":
        process_game_events()
        if gamestate == "PLAY":
            if PERIOD == 0:
                ran_Spiral = random.randint(1,10)
                ran_Distance = random.randint(1,10)
                PERIOD = 5
                #RAN = random.randint(0,2)
            get_inputs()
            process_player_related()
            process_enemy_related()
            process_collisions()
            score += 1/10
        elif gamestate == "GAMEOVER":
            screen.blit( gameover_font.render("GAMEOVER", True,(255,255,255)), (200,height/2-25) )
            screen.blit( gameover_font.render("Score: " + str(round(score,2)), True,(255,255,255)), (250,height/2+100) )
            if sum(pygame.mouse.get_pressed()):
                main()
            pygame.display.flip()
            clock.tick(2)
        display()

    pygame.quit()

main()
