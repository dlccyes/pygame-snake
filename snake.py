import pygame
import random
import sys
import time

def main():
    global screenWidth,screenHeight,game_speed,gridSize,delay,\
    x_food,y_food,x_player,y_player,bodies,tail_length,isGame,isEaten,\
    isEaten_slowpill,generate_slowpill,colordict,next_level_unlocked,\
    generate_food, l_obs_x,l_obs_y,l_obs_w,l_obs_h,dict_level
    pygame.init()

    screenWidth = 1080
    screenHeight = 600


    #initial variable
    game_speed = 5
    gridSize = 40
    delay = 140
    x_food = 0 #food's x pos
    y_food = 0 #food's y pos
    x_player = 1*gridSize #snake's head's x pos
    y_player = 1*gridSize #snake's head's y pos
    bodies = list()
    tail_length = 1
    isGame = True
    isEaten = True
    isEaten_slowpill = True
    generate_slowpill = False
    generate_food = True
    next_level_unlocked = False
    l_obs_x,l_obs_y,l_obs_w,l_obs_h = [],[],[],[]
    dict_level={'level1':True,'level2':False}

    colordict = {'yellow':(255,255,0),'blue':(54,135,255),'black':(0,0,0),\
    'white':(255,255,255),'pink':(255,131,239),'red':(255,0,0)}

    snake_game()

def button(unpressed_color, pressed_color,
    text, text_color, x_pos, y_pos, width, height, action = None):
    global screen, colordict

    mouse_pos = pygame.mouse.get_pos()
    if (x_pos < mouse_pos[0] < x_pos + width 
        and y_pos < mouse_pos[1] < y_pos + height):
        pygame.draw.rect(screen, colordict[pressed_color], (x_pos,y_pos,width,height))
        if pygame.mouse.get_pressed()[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, colordict[unpressed_color], (x_pos,y_pos,width,height))

    font = pygame.font.SysFont('Calibri', 25, bold=True)
    button_text = font.render(text, True, colordict[text_color])
    button_text_rect = button_text.get_rect()
    button_text_rect.center = (x_pos+width/2 , y_pos+height/2)
    screen.blit(button_text, button_text_rect)
    pygame.display.flip()

def quit_game():
    sys.exit() 
    pygame.quit()

def pause():
    global isGame,colordict,screen,mouse_pos
    while isGame:
        # pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False
        mouse_pos = pygame.mouse.get_pos()
        x_pos,y_pos,width,height=screenWidth/2-120/2,screenHeight/2-60/2,120,60

        if (x_pos < mouse_pos[0] < x_pos + width 
            and y_pos < mouse_pos[1] < y_pos + height):
            pygame.draw.rect(screen, colordict['pink'], (x_pos,y_pos,width,height))
            if pygame.mouse.get_pressed()[0] == 1:
                break
        else:
            pygame.draw.rect(screen, colordict['red'], (x_pos,y_pos,width,height))

        font = pygame.font.SysFont('Calibri', 25, bold=True)
        button_text = font.render('resume', True, colordict['white'])
        button_text_rect = button_text.get_rect()
        button_text_rect.center = (x_pos+width/2 , y_pos+height/2)
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()


def how_snake_die():
    global tail_length, screen, delay, isGame, colordict
    time.sleep(2)
    screen.fill(colordict['black'])

    font = pygame.font.SysFont('Calibri', 30)
    score_text = font.render("Congrats you got " + str(tail_length - 1) 
        + " points!",4,colordict['red'])
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (screenWidth/2 , screenHeight/2)
    screen.blit(score_text,score_text_rect)
    pygame.display.flip()
    time.sleep(2) # time.delay
    screen.fill(colordict['black'])
    
    while isGame:
        # pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False
        button('red','pink','quit','white',380,screenHeight/2-60/2,120,60,quit_game)
        button('red','pink','restart','white',580,screenHeight/2-60/2,120,60,main)
        pygame.display.update()


def obstacle(x,y,w,h,index):
    global screen, colordict, x_player, y_player, x_food, y_food,\
    l_obs_x,l_obs_y,l_obs_w,l_obs_h
 
    #die if snake touches obstacles
    if (x*gridSize < (x_player*2+gridSize)/2 < (x+w)*gridSize 
        and y*gridSize < (y_player*2+gridSize)/2 < (y+h)*gridSize):
        how_snake_die()
    # obs_x,obs_y,obs_w,obs_h = x,y,w,h
    if len(l_obs_x) <= index:
        l_obs_x.append(x)
    else:
        l_obs_x[index] = x
    if len(l_obs_y) <= index:
        l_obs_y.append(y)
    else:
        l_obs_y[index] = y
    if len(l_obs_w) <= index:
        l_obs_w.append(w)
    else:
        l_obs_w[index] = w
    if len(l_obs_h) <= index:
        l_obs_h.append(h)
    else:
        l_obs_h[index] = h

def generate_food_pos():
    global x_food, y_food, bodies, screenWidth, screenHeight, gridSize,\
    l_obs_x,l_obs_y,l_obs_w,l_obs_h
    x_food = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize #grid num * grid size
    y_food = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize

    for obs_x,obs_y,obs_w,obs_h in zip(l_obs_x,l_obs_y,l_obs_w,l_obs_h):
        while ((x_food, y_food) in bodies
            or obs_x*gridSize < (x_food*2+gridSize)/2 < (obs_x+obs_w)*gridSize
            and obs_y*gridSize < (y_food*2+gridSize)/2 < (obs_y+obs_h)*gridSize):
            print('fucku')
            x_food = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize
            y_food = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize
    return x_food, y_food

#same as a food except speed set back to default when eaten
def generate_slowpill_pos():
    global x_slowpill, y_slowpill, bodies, screenWidth, screenHeight, gridSize,\
    l_obs_x,l_obs_y,l_obs_w,l_obs_h
    x_slowpill = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize #grid num * grid size
    y_slowpill = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize

    for obs_x,obs_y,obs_w,obs_h in zip(l_obs_x,l_obs_y,l_obs_w,l_obs_h):
        while ((x_slowpill, y_slowpill) in bodies
            or obs_x*gridSize < (x_slowpill*2+gridSize)/2 < (obs_x+obs_w)*gridSize 
             and obs_y*gridSize < (y_slowpill*2+gridSize)/2 < (obs_y+obs_h)*gridSize):
            x_slowpill = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize
            y_slowpill = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize
    return x_slowpill, y_slowpill

def level_1():
    global tail_length, next_level_unlocked, x_player, y_player,obstacle,screenHeight,\
    screenWidth,gridSize,level_2,delay,level_common

    if tail_length == 5: #score = 10
        next_level_unlocked = True

    level_common(level_1,level_2)

def level_2():
    """level 2 of the game"""
    global next_level_unlocked, obstacle, dict_level, gridSize, generate_food,screenHeight,\
    screenWidth,gridSize,tail_length,x_player,y_player,delay,level_3,level_common

    if tail_length == 5: #score = 10
        next_level_unlocked = True
    else:
        next_level_unlocked = False

    obstacle(10,7,4,4,8)

    level_common(level_2,level_3)


def level_common(level,next_level):
    global next_level_unlocked, obstacle, dict_level, gridSize, generate_food,screenHeight,\
    screenWidth,gridSize,tail_length,x_player,y_player,delay,level_1,level_2,level_3

    if level != level_1:
        dict_level['level%s'%str(int(list(str(level))[list(str(level)).index('_')+1])-1)] = False
        dict_level['level%s'%str(list(str(level))[list(str(level)).index('_')+1])] = True

    #parameters
    obstacle(0,0,screenWidth/gridSize,1,0) #top bar
    obstacle(0,screenHeight/gridSize-1,screenWidth/gridSize,1,1) #bottom bar
    obstacle(0,0,1,(screenHeight/gridSize-1)/2,2) #left top bar
    obstacle(0,(screenHeight/gridSize-1)/2+1,1,(screenHeight/gridSize-1)/2,3) #left bottom bar
    obstacle(screenWidth/gridSize-1,0,1,(screenHeight/gridSize-1)/2,4) #right top bar
    obstacle(screenWidth/gridSize-1,(screenHeight/gridSize-1)/2+1,1,(screenHeight/gridSize-1)/2,5) #right bottom bar

    if next_level_unlocked == False:
        generate_food = True
        obstacle(screenWidth/gridSize-1,(screenHeight/gridSize-1)/2,1,1,6) #right middle block
        if level == level_1:
            obstacle(0,(screenHeight/gridSize-1)/2,1,1,7) #left middle block

    elif next_level_unlocked == True:
        obstacle(0,0,0,0,6) #open a "hole" on the right parameter
        if x_player+gridSize/2 >= screenWidth-gridSize and (screenHeight-gridSize)/2 < y_player+gridSize/2 < (screenHeight-gridSize)/2+gridSize:

            tail_length = 1
            #snake goes into the hole then appears on the left
            x_player,y_player = 1*gridSize,(screenHeight-gridSize)/2
            if level == level_1:
                obstacle(0,0,0,0,7) #open a "hole" on the left parameter

            delay = 140
            next_level()

def level_3():
    """level 3 of the game"""
    pass


#Game Loop
def snake_game():
    global generate_slowpill,x_slowpill,y_slowpill,isEaten_slowpill, game_speed,\
    x_food, y_food, x_player, y_player, gridSize, screenWidth, screenHeight, bodies,\
    delay, tail_length, screen, isGame, isEaten, colordict, next_level_unlocked,\
    generate_food, next_level_unlocked,l_obs_x,l_obs_y,l_obs_w,l_obs_h,level_1,level_2
    
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    velocity = gridSize
    up = False
    down = False
    right = False 
    left = False

    score_now = 0 #for determining the generate slowpill threshold

    while isGame :
        #Game's delay 
        pygame.time.delay(delay)

        #start_time updates as long as snake doensn't leave (i.e. move)
        if x_player == 1*gridSize and y_player == 1*gridSize:
            start_time = pygame.time.get_ticks()
        game_time = pygame.time.get_ticks() - start_time #in-game time

        if up != False or down != False or right != False or left != False :
            #die if snake's head touches its body
            for body in bodies :
                if x_player == body[0] and y_player == body[1] :
                    how_snake_die()
                    
       #to let the game close 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False

        bodies.append((x_player, y_player))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pause()
        if keys[pygame.K_UP] and down != True :
            up = True
            down = left = right = False
        if keys[pygame.K_DOWN] and up != True :
            down = True
            up = left = right = False
        if keys[pygame.K_LEFT] and right != True :
            left = True
            up = right = down = False
        if keys[pygame.K_RIGHT] and left != True :
            right = True
            up = left = down = False

        if up :
            y_player -= velocity
        elif down :
            y_player += velocity
        elif left :
            x_player -= velocity
        elif right :
            x_player += velocity

        #when touches boundary
        # if (x_player < 0 or x_player > screenWidth - gridSize 
        #         or y_player < 0 or y_player > screenHeight - gridSize):
        #     how_snake_die()


        if dict_level['level1'] == True:
            level_1()

        if dict_level['level2'] == True:
            level_2()

        if next_level_unlocked == True:
            generate_slowpill = False
            generate_food = False
        elif next_level_unlocked == False:
            if isEaten:
                x_food, y_food = generate_food_pos()
                isEaten = False
                delay -= game_speed

            if isEaten_slowpill == True and delay < 120 - score_now:
                x_slowpill, y_slowpill = generate_slowpill_pos()
                isEaten_slowpill = False
                generate_slowpill = True
            elif isEaten_slowpill == True and delay >= 100:
                generate_slowpill = False
                
            if generate_food == True and (x_player, y_player) == (x_food, y_food):
                isEaten = True
                tail_length += 1

            if generate_slowpill == True and (x_player, y_player) == (x_slowpill, y_slowpill):
                isEaten_slowpill = True
                delay += game_speed*5 #set speed back to the start
                score_now = tail_length


        while (len(bodies) > tail_length):
            del (bodies[0])
              
        screen.fill((0, 0, 0))


        #draw obstacle
        for obs_x,obs_y,obs_w,obs_h in zip(l_obs_x,l_obs_y,l_obs_w,l_obs_h):
            pygame.draw.rect(screen,colordict['blue'],(obs_x*gridSize,obs_y*gridSize,obs_w*gridSize,obs_h*gridSize))
        
        #draw food
        if generate_food == True:
            pygame.draw.rect(screen,colordict['yellow'], (x_food, y_food, gridSize, gridSize))

        #draw slowpill
        if generate_slowpill == True:
            pygame.draw.rect(screen,colordict['red'],(x_slowpill,y_slowpill,gridSize,gridSize))

        #draw the body
        for body in bodies :
            pygame.draw.rect(screen, colordict['white'], (body[0], body[1], gridSize, gridSize))

        font = pygame.font.SysFont("None", 30)
        textScore = font.render("Score: {}".format(tail_length - 1), True, (100, 100, 100))
        screen.blit(textScore, (10, 10))
        
        font = pygame.font.SysFont('Calibri', 30)
        time_text = font.render('time: %ss'%str(game_time//1000), True, (255, 0, 0))
        screen.blit(time_text, (100,100))
        # pygame.display.flip()

        #update the screen
        pygame.display.update()

if __name__ == '__main__':
    main()
