#https://github.com/RuyaKH/Pygame-Hangman
import pygame, sys, random
from time import sleep
from pygame.locals import *
from timeit import default_timer as timer

fps = 30
pygame.init()
width = 800
height = 600

black = (0,0,0)
white = (255,255,255)
lightred = (255, 165, 145)
darklightred = (255, 97, 81)
lightblue = (126,178,255)
darklightblue = (42, 129, 255)
lightgrey = (192, 192, 192)

textBoxSpace = 5
textBoxNumber = 0

def button(word,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))

    buttonText = pygame.font.Font("freesansbold.ttf",20)
    buttonTextSurf = buttonText.render(word, True, white)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x+(w/2)), (y+(h/2)))
    buttonTextSurf.get_rect().center = ((x+(w/2)), (y+(h/2)))
    screen.blit(buttonTextSurf, buttonTextRect)

def endGame():
    global textBoxSpace, textBoxNumber, end, start
    end = timer()
    print("Time it took: ",end - start)
    timeTaken = (end - start)
    textBoxSpace = 5
    textBoxNumber = 0
    message = "Time taken: " + str(round(timeTaken)) + "s"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        button("Yes",(width/2)-50,420,100,50,darklightred,lightred,quitGame)
        button("No",(width/2)-50,500,100,50,darklightred,lightred,hangman)
        
        largeText = pygame.font.SysFont("comicsansms",60)
        TextSurf = largeText.render("End Game?",True,darklightred)
        TextRect = TextSurf.get_rect()
        TextRect.center = (width / 2, height / 2)
        screen.blit(TextSurf, TextRect)

        textSurf = largeText.render(message,True,darklightred)
        textRect = textSurf.get_rect()
        textRect.center = (width/2,200)
        screen.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(fps)
        
def quitGame():
    pygame.quit()
    sys.exit()

def unpause():
    global pause
    pause = False

def pause():
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf = largeText.render("Paused",True,black)
    TextRect = TextSurf.get_rect()
    TextRect.center = (width / 2, height / 2)
    screen.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(white)
        

        button("Continue",150,450,100,50,darklightred,lightred,unpause)
        button("Quit",550,450,100,50,darklightblue,lightblue,quitgame)

        pygame.display.update()
        clock.tick(fps)

def textObjects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
    
def main():
    global clock, screen, play
    play = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hangman!")

    while True:
        hangman()

def placeLetter(letter):
    global pick, pickSplit
    space = 10
    wordSpace = 0
    while wordSpace < len(pick):
        text = pygame.font.Font('freesansbold.ttf',40)
        if letter in pickSplit[wordSpace]:
            textSurf = text.render(letter,True,black)
            textRect = textSurf.get_rect()
            textRect.center = (((150)+space),(200))
            screen.blit(textSurf, textRect)
        wordSpace += 1
        space += 60

    pygame.display.update()
    clock.tick(fps)
        
def textBoxLetter(letter):
    global textBoxSpace, textBoxNumber
    temp = 0
    for i in range(4):
        if textBoxNumber <= 5*(i+1):
            temp += 1
            if temp != 1:
                continue
            text = pygame.font.Font("freesansbold.ttf",40)
            textSurf = text.render(letter,True,black)
            textRect = textSurf.get_rect()
            textRect.center = (((105)+textBoxSpace),(300+50*(i+1)))
            screen.blit(textSurf, textRect)
        
    pygame.display.update()
    clock.tick(fps)

def hangman():
    global textBoxSpace, textBoxNumber
    textBoxSpace = 5
    textBoxNumber = 0
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)
        space = 10
        textBoxSpace = 5
        
        text = pygame.font.Font("freesansbold.ttf",20)
        textSurf = text.render("Choose a catagory",True,black)
        textRect = textSurf.get_rect()
        textRect.center = ((width/2),(height/2))
        screen.blit(textSurf, textRect)

        button("Animals",150,450,150,100,black,lightgrey,Animals)
        button("Vehicles",550,450,150,100,black,lightgrey,Vehicles)
        button("Food",150,50,150,100,black,lightgrey,Foods)
        button("Sports",550,50,150,100,black,lightgrey,Sports)
                    
        pygame.display.update()
        clock.tick(fps)

def hangmanGame(catagory,title):
    global pause, pick, pickSplit, textBoxSpace, textBoxNumber, start
    start = timer()
    chances = 20
    pick = random.choice(catagory)
    pickSplit = [pick[i:i+1] for i in range(0, len(pick), 1)]
    
    screen.fill(white)
    
    wordSpace = 0
    space = 10
    while wordSpace < len(pick):
        text = pygame.font.Font("freesansbold.ttf",40)
        textSurf1 = text.render("_",True,black)
        textRect1 = textSurf1.get_rect()
        textRect1.center = (((150)+space),(200))
        screen.blit(textSurf1, textRect1)
        space = space + 60
        wordSpace += 1
            
    guesses = ''
    gamePlay = True
    while gamePlay == True:
        guessLett = ''

        if textBoxNumber == 5:
            textBoxSpace = 5
        if textBoxNumber == 10:
            textBoxSpace = 5
        if textBoxNumber == 15:
            textBoxSpace = 5

        pygame.draw.rect(screen, white, [550,20,200,20])
        text = pygame.font.Font("freesansbold.ttf",20)
        textSurf = text.render(("Chances: %s" % chances),False,black)
        textRect = textSurf.get_rect()
        textRect.topright = (700,20)
        screen.blit(textSurf, textRect)

        textTitle = pygame.font.Font("freesansbold.ttf",40)
        textTitleSurf = textTitle.render(title,True,black)
        textTitleRect = textTitleSurf.get_rect()
        textTitleRect.center = ((width/2),50)
        screen.blit(textTitleSurf, textTitleRect)

        pygame.draw.rect(screen, black, [100,300,250,250],2)


        if chances == 19:
            pygame.draw.rect(screen,black,[450,550,100,10])
        elif chances == 18:
            pygame.draw.rect(screen,black,[550,550,100,10])
        elif chances == 17:
            pygame.draw.rect(screen,black,[650,550,100,10])
        elif chances == 16:
            pygame.draw.rect(screen,black,[500,450,10,100])
        elif chances == 15:
            pygame.draw.rect(screen,black,[500,350,10,100])
        elif chances == 14:
            pygame.draw.rect(screen,black,[500,250,10,100])
        elif chances == 13:
            pygame.draw.rect(screen,black,[500,250,150,10])
        elif chances == 12:
            pygame.draw.rect(screen,black,[600,250,100,10])
        elif chances == 11:
            pygame.draw.rect(screen,black,[600,250,10,50])
        elif chances == 10:
            pygame.draw.line(screen,black,[505,505],[550,550],10)
        elif chances == 9:
            pygame.draw.line(screen,black,[550,250],[505,295],10)
        elif chances == 8:
            pygame.draw.line(screen,black,[505,505],[460,550],10)
        elif chances == 7:
            pygame.draw.circle(screen,black,[605,325],30)
        elif chances == 6:
            pygame.draw.rect(screen,black,[600,350,10,60])
        elif chances == 5:
            pygame.draw.rect(screen,black,[600,410,10,60])
        elif chances == 4:
            pygame.draw.line(screen,black,[605,375],[550,395],10)
        elif chances == 3:
            pygame.draw.line(screen,black,[605,375],[650,395],10)
        elif chances == 2:
            pygame.draw.line(screen,black,[605,465],[550,485],10)
        elif chances == 1:
            pygame.draw.line(screen,black,[605,465],[650,485],10)

        button("Back",50,50,100,50,black,lightgrey,hangman)
        
        all_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                failed = 0
                print("Failed",failed)
                print("Chance", chances)
                
                if event.key == pygame.K_SPACE:
                    pause()
                    
                if event.key == pygame.K_ESCAPE:
                    gamePlay = False
                    

                # i = 96
                for i in range(26):
                    if event.key == i+97:

                        guessLett = guessLett + all_letters[i]
                        guesses += guessLett
                        print("letter %s guessed"%pygame.K_a)
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter(all_letters[i])
                
                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter(all_letters[i])

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was",pick)
                            endGame()


        pygame.display.update()
        clock.tick(fps)

    pygame.display.update()
    clock.tick(fps)

def Animals():
    animal = ['cow','dog','cat','pig','zebra','bird','giraffe','lion','tiger','penguin','hamster','fox','panda','bear','cheetah','ostrich','meerkat','whale','shark','horse','monkey','octopus','kitten','kangaroo','chicken','fish','rabbit','sheep']
    print("animal")
    title = "Animals"
    hangmanGame(animal,title)

def Vehicles():
    vehicle = ['car','bus','train','airplane','plane','ship','jet','boat','lorry','tractor','bike','motorbike','tram','van','ambulance','fire engine','rocket','taxi','caravan','coach','lorry','scooter','sleigh','tank','wagon','spaceship']
    print("vehicle")
    title = "Vehicles"
    hangmanGame(vehicle,title)
    
def Foods():
    food = ['apple','banana','orange','peach','pizza','donut','chips','sandwich','cookie','cucumber','carrot','sweetcorn','ice cream','pancake','bread','potato','tomato','nuts','yogurt','pasta','rice','cheese','soup','fish','egg','meat','ham','sausage']
    print("food")
    title = "Foods"
    hangmanGame(food,title)
    
def Sports():
    sport = ['rugby','football','netball','basketball','swimming','hockey','curling','running','golf','tennis','badmington','archery','volleyball','bowling','dancing','gym','skating','baseball','rounders','boxing','climbing','canoe','cycling','fencing','karate','shooting','cricket']
    print("sport")
    title = "Sports"
    hangmanGame(sport,title)

    
if __name__ == '__main__':
    main()