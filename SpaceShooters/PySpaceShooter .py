import pygame
import math
import os
import random
os.environ["SDL_VIDEO_CENTERED"] = "1" # Centers game window
##SPACESHIP GAME
# Version 10
# Start Screen
# Game Over Screen
# Instructions Screen
# Paused Screen
# BackGround Change to Black

#Instructions:
# W/A/S/D to move
#"Space" to shoot
# P to pause
# ESC to exit game
# Your Mission: Survive

def main():
    #Initialise pygame
    pygame.init()
    clock = pygame.time.Clock() #FPS
    timer = pygame.time.get_ticks() # Spawner Time
    timerB = pygame.time.get_ticks() # Boss Time
    cooldown = pygame.time.get_ticks() #Attack Time
    #Display
    Dis_x = 900
    Dis_y = 900
    DISPLAY=(Dis_x,Dis_y) #Window Size
    screen = pygame.display.set_mode(DISPLAY)
    screen.fill((10, 10, 10)) # Window Color
    font = pygame.font.Font(None,30)
    pygame.display.set_caption('SpaceShooters')
    #Display objects blitted into memory
    pygame.display.flip()
    ## PlayerAnims
    PlayUp = pygame.transform.smoothscale(pygame.image.load('Player.png'),(80,80))
    PlayDown = pygame.transform.rotate(PlayUp,180)
    PlayLeft = pygame.transform.rotate(PlayUp,90)
    PlayRight = pygame.transform.rotate(PlayUp,-90)
    PlayUpRight = pygame.transform.rotate(PlayUp,-45)
    PlayUpLeft = pygame.transform.rotate(PlayUp,45)
    PlayDownRight = pygame.transform.rotate(PlayUp,-135)
    PlayDownLeft = pygame.transform.rotate(PlayUp,135)
    PlayerAnim = PlayUp
    ##BulletAnims
    BulletU = pygame.transform.smoothscale(pygame.image.load('PlayerBullet.png'),(10,15))
    BulletS = pygame.transform.rotate(BulletU,90)
    BulletUpLeft = pygame.transform.rotate(BulletU,45)
    BulletUpRight = pygame.transform.rotate(BulletU,-45)
    BulletDownLeft = pygame.transform.rotate(BulletU,-135)
    BulletDownRight = pygame.transform.rotate(BulletU,135)
    ##EnemyBulletAnims
    EBU = pygame.transform.smoothscale(pygame.image.load('RedLaser.png'),(25,30))
    EBS = pygame.transform.rotate(EBU,90)
    ##EnemyAnims
    EnemyRight = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load('Enemy.png'),(80,80)),90)
    EnemyLeft = pygame.transform.rotate(EnemyRight,180)
    EnemyUp = pygame.transform.rotate(EnemyRight,90)
    EnemyDown = pygame.transform.rotate(EnemyRight,-90)
    EnemyUpRight = pygame.transform.rotate(EnemyRight,45)
    EnemyUpLeft = pygame.transform.rotate(EnemyRight,135)
    EnemyDownRight = pygame.transform.rotate(EnemyRight,-45)
    EnemyDownLeft = pygame.transform.rotate(EnemyRight,-135)
    EnemyAnim = EnemyRight
    BossAnim = pygame.transform.smoothscale(pygame.image.load('Boss.png'),(120,120))
    ## Start Screen Variable ##
    Title = pygame.image.load('Space-Shooters.png')
    Play = pygame.image.load('Play.png')
    Quit = pygame.image.load('Quit.png')
    GM = pygame.image.load('Game-Over.png')
    RS = pygame.image.load('Click-To-Restart.png')
    Paused = pygame.image.load('PAUSED.png')
    Ins = pygame.image.load('Instructions.png')
    INSTRUC = pygame.image.load('Instruc.png')
    start = False
    ind = True
    ### GameObjects ###
    player = Player(50,10) # Player Instance
    enemies = [] # Enemy List          
    # Game Variables
    xloc = 300 #Player X position
    yloc = 300 #Player Y position
    GAMESTATE = 0
    playerHP = 50 # HealthBar Variable
    bullets = [] # Player Bullet List
    EnemBullets = [] # Enemy Bullet List
    state = 'Up' #Animation stages for up,down,left,right
    substate = 'Neutral' #Animation stages for diagonal anims
    bbcords = [[37,-5],[80,37],[37,80],[-5,37],[80,80],[0,80],[0,0],[80,0]] #Bullet Direction Points
    score = 0 #Score
    time = 0 #Time
    count = 0 

    def start_screen():
        nonlocal start
        while start == False:
            screen.fill((10, 10, 10))
            screen.blit(Title,(100,200))
            screen.blit(Play,(350,400))
            screen.blit(Ins,(180,500))
            screen.blit(Quit,(350,600))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    #Play
                    if 350 <= pos[0] <= 600 and 400 <= pos[1] <= 499:
                        start = True
                    if 350 <= pos[0] <= 600 and 500 <= pos[1] <= 550:
                        instruc()
                    #Quit
                    if 350 <= pos[0] <= 500 and 600 <= pos[1] <= 699:
                        pygame.display.quit()
    def instruc():
        nonlocal ind
        ind = True
        while ind == True:
            screen.blit(INSTRUC,(0,0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ind = False
        start_screen()
                    
    def get_input():
        nonlocal xloc, yloc, GAMESTATE,PlayerAnim,bbcords,state,substate,bullets
        bullet_x = xloc #X axis of bullet
        bullet_y = yloc #Y axis of bullet
        ### Handle Player Movement and Bullet Directions ###
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                GAMESTATE = 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xloc-=10
                    state = 'Left'
                if event.key == pygame.K_RIGHT:
                    xloc+=10
                    state = 'Right'
                if event.key == pygame.K_UP:
                    yloc-=10
                    state = 'Up'
                if event.key == pygame.K_DOWN:
                    yloc+=10
                    state = 'Down'
                if event.key == pygame.K_ESCAPE:
                    GAMESTATE = 2
                if event.key == pygame.K_SPACE:
                    ### Bullet Shoot Points ###
                    if state == 'Up' and substate == 'Neutral':
                        bullet_x = xloc + bbcords[0][0]
                        bullet_y = yloc + bbcords[0][1]
                        bullets += [[bullet_x,bullet_y,'UP']]
                    elif state == 'Down' and substate == 'Neutral':
                        bullet_x = xloc + bbcords[2][0]
                        bullet_y = yloc + bbcords[2][1]
                        bullets += [[bullet_x,bullet_y,'DOWN']]
                    elif state == 'Right' and substate == 'Neutral':
                        bullet_x = xloc + bbcords[1][0]
                        bullet_y = yloc + bbcords[1][1]
                        bullets += [[bullet_x,bullet_y,'RIGHT']]
                    elif state == 'Left' and substate == 'Neutral':
                        bullet_x = xloc + bbcords[3][0]
                        bullet_y = yloc + bbcords[3][1]
                        bullets += [[bullet_x,bullet_y,'LEFT']]
                    if substate == 'RightUp':
                        bullet_x = xloc + bbcords[7][0]
                        bullet_y = yloc + bbcords[7][1]
                        bullets += [[bullet_x,bullet_y,'RIGHTUP']]
                    elif substate == 'LeftUp':
                        bullet_x = xloc + bbcords[6][0]
                        bullet_y = yloc + bbcords[6][1]
                        bullets += [[bullet_x,bullet_y,'LEFTUP']]
                    elif substate == 'RightDown':
                        bullet_x = xloc + bbcords[4][0]
                        bullet_y = yloc + bbcords[4][1]
                        bullets += [[bullet_x,bullet_y,'RIGHTDOWN']]
                    elif substate == 'LeftDown':
                        bullet_x = xloc + bbcords[5][0]
                        bullet_y = yloc + bbcords[5][1]
                        bullets += [[bullet_x,bullet_y,'LEFTDOWN']]
                #Toggle between pause and play
                if event.key == pygame.K_p:
                    if GAMESTATE == 0:
                        GAMESTATE = 1
                    elif GAMESTATE == 1:
                        GAMESTATE = 0
                        
        ### PlayerMovementAnimations
        pygame.event.get()
        pressed = pygame.key.get_pressed() 
        if pressed[pygame.K_LEFT]:
            xloc-=5
            state = 'Left'
            substate = 'Neutral'
            PlayerAnim = PlayLeft
        if pressed[pygame.K_RIGHT]:
            xloc+=5
            state = 'Right'
            substate = 'Neutral'
            PlayerAnim = PlayRight
        if pressed[pygame.K_UP]:
            yloc-=5
            state = 'Up'
            substate = 'Neutral'
            PlayerAnim = PlayUp
        if pressed[pygame.K_DOWN]:
            yloc+=5
            state = 'Down'
            substate = 'Neutral'
            PlayerAnim = PlayDown
        if pressed[pygame.K_UP] and pressed[pygame.K_RIGHT]:
            state = 'Up'
            substate = 'RightUp'
            PlayerAnim = PlayUpRight
        if pressed[pygame.K_UP] and pressed[pygame.K_LEFT]:
            state = 'Up'
            substate = 'LeftUp'
            PlayerAnim = PlayUpLeft
        if pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT]:
            state = 'Down'
            substate = 'RightDown'
            PlayerAnim = PlayDownRight
        if pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT]:
            state = 'Down'
            substate = 'LeftDown'
            PlayerAnim = PlayDownLeft
        if pressed[pygame.K_ESCAPE]:
            GAMESTATE = 2

    def process_game_objects():
        nonlocal xloc, yloc, GAMESTATE,player,state,enemies,bullets,timer,timerB,EnemBullets,cooldown,playerHP,score,time,Dis_x,Dis_y,count
        ### Loops for player bullet travel in diff directions ###
        for i in range(len(bullets)):
            if bullets[i][2] == 'UP' and bullets[i][1] > -20:
                bullets[i][1] += (-20)
            if bullets[i][2] == 'DOWN' and bullets[i][1] < Dis_y:
                bullets[i][1] += (20)
            if bullets[i][2] == 'LEFT' and bullets[i][0] > -20:
                bullets[i][0] += (-20)
            if bullets[i][2] == 'RIGHT' and bullets[i][0] < Dis_x:
                bullets[i][0] += (20)
            if bullets[i][2] == 'LEFTUP' and bullets[i][0] > -20 and bullets[i][1] > -20:
                bullets[i][0] += (-20)
                bullets[i][1] += (-20)
            if bullets[i][2] == 'RIGHTUP' and bullets[i][1] < Dis_y and bullets[i][1] > -20:
                bullets[i][0] += (20)
                bullets[i][1] += (-20)
            if bullets[i][2] == 'LEFTDOWN' and bullets[i][0] > -20 and bullets[i][1] < Dis_y:
                bullets[i][0] += (-20)
                bullets[i][1] += (20)
            if bullets[i][2] == 'RIGHTDOWN' and bullets[i][1] < Dis_y and bullets[i][0] < Dis_x:
                bullets[i][0] += (20)
                bullets[i][1] += (20)
            ### Bullet Collision Check ###
            for ins in enemies:
                if ins.get_x()<bullets[i][0]<ins.get_x()+120 and ins.get_y()<bullets[i][1]<ins.get_y()+100 and ins.get_dmg() == 0:
                    ins.take_dmg(player.get_dmg())
                    bullets[i][0] += 1000
                    bullets[i][1] += 1000
                    if ins.get_hp() <= 0:
                        score += 1000
                        count += 1
                elif ins.get_x()<bullets[i][0]<ins.get_x()+80 and ins.get_y()<bullets[i][1]<ins.get_y()+60:
                    ins.take_dmg(player.get_dmg())
                    bullets[i][0] += 1000
                    bullets[i][1] += 1000
                    if ins.get_hp() <= 0:
                        score += 10
                        count += 1
                    
        ### Loop for Enemy Bullet Travel in diff directions ###
        for i in range(len(EnemBullets)):
            if EnemBullets[i][2] == 'UP' and EnemBullets[i][1] > -40 and EnemBullets[i][1] < Dis_y+200:
                EnemBullets[i][1] += (-20)
            elif EnemBullets[i][2] == 'DOWN' and EnemBullets[i][1] < Dis_y+200 and EnemBullets[i][1] > -40:
                EnemBullets[i][1] += (20)
            elif EnemBullets[i][2] == 'LEFT' and EnemBullets[i][0] > -40 and EnemBullets[i][0] < Dis_x+200:
                EnemBullets[i][0] += (-20)
            elif EnemBullets[i][2] == 'RIGHT' and EnemBullets[i][0] < Dis_x+200 and EnemBullets[i][0] > -40:
                EnemBullets[i][0] += (20)
            ### Player Collision Check ###
            if xloc<EnemBullets[i][0]<xloc+80 and yloc<EnemBullets[i][1]<yloc+60 and  xloc  < DISPLAY[0] and xloc > -10 and yloc < DISPLAY[1] and yloc > -10:
                    player.take_dmg(5) # Player object take damage
                    playerHP -= 5 # HealthBar Update Display
                    EnemBullets[i][0] += 1000

                

        ### Player Hover Effect ###
        if state == 'Up' and substate == 'Neutral':
            yloc -= 1
        elif state == 'Down' and substate == 'Neutral':
            yloc += 1
        elif state == 'Right' and substate == 'Neutral':
            xloc += 1
        elif state == 'Left' and substate == 'Neutral':
            xloc -= 1
        if substate == 'RightUp':
            xloc += 0.5
            yloc -= 0.5
        elif substate == 'LeftUp':
            xloc -= 0.5
            yloc -= 0.5
        elif substate == 'RightDown':
            xloc += 0.5
            yloc += 0.5
        elif substate == 'LeftDown':
            xloc -= 0.5
            yloc += 0.5
        #If out of screen, make Enemies within screen
        for ins in enemies:
            if ins.get_x() > DISPLAY[0]:
                ins.set_x(0)
            elif ins.get_x() < -10:
                ins.set_x(Dis_x)
            if ins.get_y() > DISPLAY[1]:
                ins.set_y(0)
            elif ins.get_y() < -10:
                ins.set_y(Dis_y)

        ### Process Enemy Spawner ###
        now = pygame.time.get_ticks()
        # When 3s pass
        if now - timer > 3000:
            timer = now
            ran = random.randint(0,7) ### Random spawn point e.g up,down,left,right
            if ran == 0: #UP
                enemy = Enemy(30,5,random.randint(10, Dis_y-30),10,'UP')
            elif ran == 1: #DOWN
                enemy = Enemy(30,5,random.randint(10, Dis_y-30),Dis_y-30,'DOWN')
            elif ran == 2: #Right
                enemy = Enemy(30,5,10,random.randint(10, Dis_x-30),'RIGHT')
            elif ran == 3: #Left
                enemy = Enemy(30,5,Dis_x-30,random.randint(10, Dis_x-30),'LEFT')
            elif ran == 4: #UpRight
                enemy = Enemy(30,5,Dis_x-30,Dis_y-30,'UPRIGHT')
            elif ran == 5: #UpLeft
                enemy = Enemy(30,5,10,10,'UPLEFT')
            elif ran == 6: #DownRight
                enemy = Enemy(30,5,10,Dis_y-30,'DOWNRIGHT')
            elif ran == 7: #DownLeft
                enemy = Enemy(30,5,Dis_x-30,Dis_y-30,'DOWNLEFT')
            enemies.append(enemy)
            
        ### Bonus Point Boss Spawner ###
        nowB = pygame.time.get_ticks()
        # When 60s pass
        if nowB - timerB > 60000:
            timerB = nowB
            enemies.append(Enemy(150,0,random.randint(30, Dis_x-50),Dis_y-40,'BOSS'))
            enemies.append(Enemy(30,5,random.randint(30, Dis_x-50),Dis_y-30,'DOWN'))
            enemies.append(Enemy(30,5,random.randint(30, Dis_x-50),Dis_y-30,'DOWN'))
            enemies.append(Enemy(30,5,random.randint(30, Dis_x-50),Dis_y-30,'DOWN'))
            
        ### Process Enemy Shooting ###
        for ins in enemies:
            h = pygame.time.get_ticks()
            if h - ins.get_last() >= ins.get_cooldown() and ins.get_status() == True: # If cooldown and not dead
                ins.set_last(h)
                if ins.get_state() == 'UP':
                    EnemBullets += ins.shoot('UP')
                elif ins.get_state() == 'DOWN':
                    EnemBullets += ins.shoot('DOWN')
                elif ins.get_state() == 'RIGHT':
                    EnemBullets += ins.shoot('RIGHT')
                elif ins.get_state() == 'LEFT':
                    EnemBullets += ins.shoot('LEFT')
                elif ins.get_state() == 'UPRIGHT':
                    EnemBullets += ins.shoot('UP')
                elif ins.get_state() == 'UPLEFT':
                    EnemBullets += ins.shoot('UP')
                elif ins.get_state() == 'DOWNRIGHT':
                    EnemBullets += ins.shoot('DOWN')
                elif ins.get_state() == 'DOWNLEFT':
                    EnemBullets += ins.shoot('DOWN')
                
        ### Process Enemy Movement ###
        for ins in enemies:
            if ins.get_status() == True: # Not Dead
                if ins.get_state() == 'UP':
                    ins.up()
                elif ins.get_state() == 'DOWN':
                    ins.down()
                elif ins.get_state() == 'RIGHT':
                    ins.right()
                elif ins.get_state() == 'LEFT':
                    ins.left()
                elif ins.get_state() == 'UPRIGHT':
                    ins.UpRight()
                elif ins.get_state() == 'UPLEFT':
                    ins.UpLeft()
                elif ins.get_state() == 'DOWNRIGHT':
                    ins.DownRight()
                elif ins.get_state() == 'DOWNLEFT':
                    ins.DownLeft()
                elif ins.get_state() == 'BOSS':
                    ins.downB()

        ### Process Time ###
        time += 1
        
        #If out of screen, make Player within screen
        if xloc  > DISPLAY[0]:  #Xloc
            xloc = 0  
        elif xloc < -10:
            xloc = Dis_x
        if yloc > DISPLAY[1]:   #Yloc
            yloc = 0
        elif yloc < -10:
            yloc = Dis_y


    def display():
        nonlocal PlayerAnim,EnemyAnim,state,enemies,score,bullets,EnemBullets,GAMESTATE,time,Dis_x,Dis_y,count,GM,RS,Paused
        #Display / Output
        screen.fill((10, 10, 10))
        # Draw the bullets
        for i in range(len(bullets)):
            if bullets[i][2] == 'UP' or bullets[i][2] == 'DOWN':
                screen.blit(BulletU, (bullets[i][0],bullets[i][1]))
            elif bullets[i][2] == 'RIGHT' or bullets[i][2] == 'LEFT':
                screen.blit(BulletS, (bullets[i][0],bullets[i][1]))
            elif bullets[i][2] == 'RIGHTUP':
                screen.blit(BulletUpRight, (bullets[i][0],bullets[i][1]))
            elif bullets[i][2] == 'LEFTUP':
                screen.blit(BulletUpLeft, (bullets[i][0],bullets[i][1]))
            elif bullets[i][2] == 'RIGHTDOWN':
                screen.blit(BulletDownLeft, (bullets[i][0],bullets[i][1]))
            elif bullets[i][2] == 'LEFTDOWN':
                screen.blit(BulletDownRight, (bullets[i][0],bullets[i][1]))
        # Draw Enemy Bullets
        for m in range(len(EnemBullets)):
            if EnemBullets[m][2] == 'UP' or EnemBullets[m][2] == 'DOWN':
                screen.blit(EBU, (EnemBullets[m][0],EnemBullets[m][1]))
            elif EnemBullets[m][2] == 'RIGHT' or EnemBullets[m][2] == 'LEFT':
                screen.blit(EBS, (EnemBullets[m][0],EnemBullets[m][1]))
        ##Draw enemies
        for ins in enemies:
            if ins.get_hp() > 0:
                if ins.get_state() == 'UP':
                    EnemyAnim = EnemyUp
                elif ins.get_state() == 'DOWN':
                    EnemyAnim = EnemyDown
                elif ins.get_state() == 'RIGHT':
                    EnemyAnim = EnemyRight
                elif ins.get_state() == 'LEFT':
                    EnemyAnim = EnemyLeft
                elif ins.get_state() == 'UPRIGHT':
                    EnemyAnim = EnemyUpRight
                elif ins.get_state() == 'UPLEFT':
                    EnemyAnim = EnemyUpLeft
                elif ins.get_state() == 'DOWNRIGHT':
                    EnemyAnim = EnemyDownRight
                elif ins.get_state() == 'DOWNLEFT':
                    EnemyAnim = EnemyDownLeft
                elif ins.get_state() == 'BOSS':
                    EnemyAnim = BossAnim
                screen.blit(EnemyAnim, (ins.get_x(),ins.get_y()))
            else:
                ins.set_x(2000) #'Disappear'
                ins.set_y(1000)
                ins.set_status(False) #Dead
        ### Draw Player
        if player.get_hp() > 0:
            screen.blit(PlayerAnim, (xloc,yloc))
            #Time
            screen.blit(font.render("Time Survived: " + str(int(time/60)), True, (255,255,255)), (700,4))
            #Score
            screen.blit(font.render("Score: " + str(int(score)), True, (255,255,255)), (350,4))
            #Count shots
            screen.blit(font.render("Enemies Killed: " + str(int(count)), True, (255,255,255)), (500,4))
            # Health Bar
            screen.blit(font.render("Health", True, (255,0,0)), (10,5))
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(80,10,playerHP*3,10)) 
        else:
            GAMESTATE = 1
            screen.blit(font.render("Time Survived: " + str(int(time/60)), True, (255,255,255)), (550,4))
            screen.blit(font.render("Enemies Killed: " + str(int(count)), True, (255,255,255)), (350,4))
            screen.blit(font.render("Score: " + str(int(score)), True, (255,255,255)), (200,4))
            screen.blit(GM,(180,300))
            screen.blit(RS,(80,500))
            if sum(pygame.mouse.get_pressed()):
                main()
        # Display the paused text
        if GAMESTATE==1 and player.get_hp() > 0:
            screen.blit(Paused,(280,400))
            
        #display: flip the page to display it
        pygame.display.flip()

        ### FPS ###
        clock.tick(90)
    #Game Loop
    start_screen()
    while GAMESTATE != 2:
        get_input()
        if GAMESTATE == 0:         #if game is running (0), and not paused
            process_game_objects() #do the game processing
        display()                  #output


    #Out of game loop. Close display
    pygame.display.quit()


    
##CLASSES
class GameObject(object): #Parent Class
    def __init__(self, hp, dmg):
        self.hp = hp
        self.dmg = dmg
    def get_hp(self):
        return self.hp
    def get_dmg(self):
        return self.dmg
    def take_dmg(self,damage):
        self.hp -= damage

class Player(GameObject): # Player Subclass
    def __init__(self,hp,dmg):
        super().__init__(hp,dmg)

class Enemy(GameObject): # Enemy Subclass
    def __init__(self,hp,dmg,x,y,state):
        super().__init__(hp,dmg)
        self.x = x
        self.y = y
        self.state = state
        self.last = pygame.time.get_ticks()
        self.cooldown = 2000
        self.active = True
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,nx):
        self.x = nx
    def set_y(self,ny):
        self.y = ny
    def get_state(self): # Get Animation Stage
        return self.state
    def get_last(self): #Shoot Cooldown
        return self.last
    def get_cooldown(self): #Shoot Cooldown Duration
        return self.cooldown
    def get_status(self): # Status (Dead or Alive)
        return self.active
    def set_status(self,t):
        self.active = t
    def set_last(self,k):
        self.last = k
    def right(self): #Move Right
        self.x += 3
    def left(self): #Move Left
        self.x -= 3
    def down(self): #Move Down
        self.y += 3
    def up(self): #Move Up
        self.y -= 3
    def UpRight(self): #Move Upright
        self.x += 3
        self.y -= 3
    def UpLeft(self): #Move Upleft
        self.x -= 3
        self.y -= 3
    def DownRight(self): #Move DownRight
        self.x += 3
        self.y += 3
    def DownLeft(self): #Move Downleft
        self.x -= 3
        self.y += 3
    def downB(self): #Boss Movement
        self.y += 1
    def shoot(self,direction): # Set Bullet and Bullet Shoot Point
        if direction == 'UP':
            return [[self.x+34,self.y-5,'UP']]
        elif direction == 'DOWN':
            return [[self.x+34,self.y+80,'DOWN']]
        elif direction == 'RIGHT':
            return [[self.x+80,self.y+34,'RIGHT']]
        elif direction == 'LEFT':
            return [[self.x-5,self.y+34,'LEFT']]


    
if __name__ == "__main__":  #runs the function main() automatically
    main()  

