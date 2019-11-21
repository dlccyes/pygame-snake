import pygame
import random
import sys
import time

pygame.init()

screen = pygame.display.set_mode((1200, 800))

#initial variable
screenHeight = 800
screenWidth = 1200
gridSize = 40
isGame = True
isEaten = True
delay = 140
x_food = 0
y_food = 0
x_player = 0
y_player = 0
velocity = gridSize
up = False
down = False
right = False 
left = False
bodies = list()
tail_length = 1
isEaten = True


def how_snake_die():
    font = pygame.font.SysFont('Calibri', 30)
    score_text = font.render("Congrats you got " + str(tail_length - 1) + " points!",4,(255,0,0))
    screen.blit(score_text,(425,350))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def generate_food():
    #global x_food, y_food
    x_food = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize
    y_food = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize
    while (x_food, y_food) in bodies:
        x_food = random.randint(0, (screenWidth - gridSize) / gridSize) * gridSize
        y_food = random.randint(0, (screenHeight - gridSize) / gridSize) * gridSize
    return x_food, y_food
#Game Loop
while isGame :
    #Game's delay 
    pygame.time.delay(delay)

    if up != False or down != False or right != False or left != False :
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


    if x_player > screenWidth - gridSize :
        x_player = 0
    if y_player > screenHeight - gridSize :
        y_player = 0
    if x_player < 0 :
        x_player = screenWidth - gridSize
    if y_player < 0 :
        y_player = screenHeight - gridSize

    if isEaten:
        x_food, y_food = generate_food()
        isEaten = False
        delay -= 3
        
    if (x_player, y_player) == (x_food, y_food):
        isEaten = True
        tail_length += 1

    while (len(bodies) > tail_length):
        del (bodies[0])
    
    

    
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 255, 0), (x_food, y_food, gridSize, gridSize))

    #draw the body
    for body in bodies :
        pygame.draw.rect(screen, (255, 255, 255), (body[0], body[1], gridSize, gridSize))

    font = pygame.font.SysFont("None", 30)
    textScore = font.render("Score: {}".format(tail_length - 1), True,   (100, 100, 100))
    screen.blit(textScore, (10, 10))


    #update the screen
    pygame.display.update()