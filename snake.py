import pygame
import random
import sys
import time

pygame.init()

screenWidth = 1080
screenHeight = 600


#initial variable
game_speed = 5
gridSize = 40
delay = 140
x_food = 0 #food's x pos
y_food = 0 #food's y pos
x_player = 0 #snake's head's x pos
y_player = 0 #snake's head's y pos
bodies = list()
tail_length = 1
isGame = True
isEaten = True
isEaten_slowpill = True
colordict = {'yellow':(255,255,0),'blue':(54,135,255),'black':(0,0,0),'white':(255,255,255),'pink':(255,131,239),'red':(255,0,0)}


def button(pressed_color, unpressed_color, text, text_color, x_pos, y_pos, width, height, action = None):
    global screen, colordict

    mouse_pos = pygame.mouse.get_pos()
    if x_pos < mouse_pos[0] < x_pos + width and y_pos < mouse_pos[1] < y_pos + height:
        pygame.draw.rect(screen, colordict[unpressed_color], (x_pos,y_pos,width,height))
        if pygame.mouse.get_pressed()[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, colordict[pressed_color], (x_pos,y_pos,width,height))

    font = pygame.font.SysFont('Calibri', 25, bold=True)
    button_text = font.render(text, True, colordict[text_color])
    button_text_rect = button_text.get_rect()
    button_text_rect.center = (x_pos+width/2 , y_pos+height/2)
    screen.blit(button_text, button_text_rect)
    pygame.display.flip()

def quit_game():
    sys.exit() 
    pygame.quit()

def reset():
    """restart the game"""
    global x_food, x_player, y_food, y_player, isEaten, tail_length, bodies, delay
    #initial variable
    pygame.init()
    delay = 140
    x_food = 0 #food's x pos
    y_food = 0 #food's y pos
    x_player = 0 #snake's head's x pos
    y_player = 0 #snake's head's y pos

    bodies = list()
    tail_length = 1
    isEaten = True
    snake_game()

def how_snake_die():
    global tail_length, screen, delay, isGame, colordict
    time.sleep(2)
    screen.fill(colordict['black'])
    font = pygame.font.SysFont('Calibri', 30)
    score_text = font.render("Congrats you got " + str(tail_length - 1) + " points!",4,colordict['red'])
    screen.blit(score_text,(425,350))
    pygame.display.flip()
    time.sleep(2) # time.delay
    screen.fill(colordict['black'])
    
    while isGame:
        # pygame.time.delay(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False
        button('red','pink','quit','white',400,300,120,60,quit_game)
        button('red','pink','restart','white',600,300,120,60,reset)
        pygame.display.update()


def obstacle(x,y,w,h):
    global screen, colordict, x_player, y_player, x_food, y_food, obs_x,obs_y,obs_w,obs_h
    # pygame.draw.rect(screen,colordict['blue'],(x*gridSize,y*gridSize,w*gridSize,h*gridSize))
    if x*gridSize < (x_player*2+gridSize)/2 < (x+w)*gridSize and y*gridSize < (y_player*2+gridSize)/2 < (y+h)*gridSize:
        how_snake_die()
    obs_x,obs_y,obs_w,obs_h = x,y,w,h  

def generate_food():
    global x_food, y_food, bodies, screenWidth, screenHeight, gridSize, obs_x,obs_y,obs_w,obs_h
    x_food = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize #grid num * grid size
    y_food = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize

    while (x_food, y_food) in bodies or obs_x*gridSize < (x_food*2+gridSize)/2 < (obs_x+obs_w)*gridSize and obs_y*gridSize < (y_food*2+gridSize)/2 < (obs_y+obs_h)*gridSize:
        x_food = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize
        y_food = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize
    return x_food, y_food

#same as a food except speed set back to default when eaten
def generate_slowpill():
    global x_slowpill, y_slowpill, bodies, screenWidth, screenHeight, gridSize, obs_x,obs_y,obs_w,obs_h
    x_slowpill = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize #grid num * grid size
    y_slowpill = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize

    while (x_slowpill, y_slowpill) in bodies or obs_x*gridSize < (x_slowpill*2+gridSize)/2 < (obs_x+obs_w)*gridSize and obs_y*gridSize < (y_slowpill*2+gridSize)/2 < (obs_y+obs_h)*gridSize:
        x_slowpill = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize
        y_slowpill = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize
    return x_slowpill, y_slowpill

    
#Game Loop
def snake_game():
    global x_slowpill,y_slowpill,isEaten_slowpill, game_speed, x_food, y_food, x_player, y_player, gridSize, screenWidth, screenHeight, bodies, delay, tail_length, screen, isGame, isEaten, colordict
    
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    velocity = gridSize
    up = False
    down = False
    right = False 
    left = False

    while isGame :
        #Game's delay 
        pygame.time.delay(delay)

        if up != False or down != False or right != False or left != False :
            #if snake's head touches its body
            for body in bodies :
                if x_player == body[0] and y_player == body[1] :
                    how_snake_die()
                    
       #to let the game close 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False

        bodies.append((x_player, y_player))

        keys = pygame.key.get_pressed()

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
        if x_player < 0 or x_player > screenWidth - gridSize or y_player < 0 or y_player > screenHeight - gridSize:
            how_snake_die()

        obstacle(5,4,8,8)
        if isEaten:
            x_food, y_food = generate_food()
            isEaten = False
            delay -= game_speed

        if isEaten_slowpill:
            x_slowpill, y_slowpill = generate_slowpill()
            isEaten_slowpill = False
            delay = 140 #set speed back to the start
            
        if (x_player, y_player) == (x_food, y_food):
            isEaten = True
            tail_length += 1

        if (x_player, y_player) == (x_slowpill, y_slowpill):
            isEaten_slowpill = True


        while (len(bodies) > tail_length):
            del (bodies[0])
              
        screen.fill((0, 0, 0))

        
        #draw food
        pygame.draw.rect(screen,colordict['blue'],(obs_x*gridSize,obs_y*gridSize,obs_w*gridSize,obs_h*gridSize))
        pygame.draw.rect(screen,colordict['yellow'], (x_food, y_food, gridSize, gridSize))

        #draw slowpill
        pygame.draw.rect(screen,colordict['red'],(x_slowpill,y_slowpill,gridSize,gridSize))

        #draw the body
        for body in bodies :
            pygame.draw.rect(screen, colordict['white'], (body[0], body[1], gridSize, gridSize))

        font = pygame.font.SysFont("None", 30)
        textScore = font.render("Score: {}".format(tail_length - 1), True, (100, 100, 100))
        screen.blit(textScore, (10, 10))

        if x_player == 0 and y_player == 0:
            start_time = pygame.time.get_ticks()
        game_time = pygame.time.get_ticks() - start_time
        font = pygame.font.SysFont('Calibri', 30)
        time_text = font.render('time: %ss'%str(game_time//1000), True, (255, 0, 0))
        screen.blit(time_text, (100,100))
        # pygame.display.flip()

        #update the screen
        pygame.display.update()

if __name__ == '__main__':
    snake_game()
