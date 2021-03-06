import pygame
import random
import sys
import time
import tkinter as tk
import os
from PIL import ImageTk,Image  

def main():
    global screenWidth,screenHeight,game_speed,gridSize,delay,\
    x_food,y_food,x_player,y_player,bodies,tail_length,isGame,isEaten_food,\
    isEaten_slowpill,generate_slowpill,colordict,next_level_unlocked,\
    generate_food, l_obs_x,l_obs_y,l_obs_w,l_obs_h,dict_level,total_score,obstacle_index,\
    moving_obs_y_1,moving_obs_y_2,moving_obstacle,bullet_pos_n_dir,\
    isEaten_ammunition,generate_ammunition,ammunition_count,snakey,ticks,root,\
    play_button,difficlulty_button,tutorial_button,x_slowpill,y_slowpill,x_ammunition,y_ammunition,\
    blackk,aisnake_length,init_delay,aisnake_speed,ragemode_length,score_multiplier

    blackk.lift()

    #initial variable
    game_speed = 5

    try:
        delay = init_delay
    except:
        init_delay = 140
        aisnake_length = 6
        ragemode_length = 3
        aisnake_speed = 4
        delay = init_delay
        score_multiplier = 1

    x_player = 1*gridSize #snake's head's x pos
    y_player = 1*gridSize #snake's head's y pos
    bodies = list()
    tail_length = 1
    isGame = True
    #food
    x_food = 0 #food's x pos
    y_food = 0 #food's y pos
    isEaten_food = True
    generate_food = True
    #slowpill
    x_slowpill = 0
    y_slowpill = 0
    isEaten_slowpill = True
    generate_slowpill = False
    #ammunition
    x_ammunition = 0
    y_ammunition = 0
    isEaten_ammunition = True
    generate_ammunition = True
    ammunition_count = 0

    next_level_unlocked = False
    l_obs_x,l_obs_y,l_obs_w,l_obs_h = [],[],[],[]
    dict_level={'level1':True,'level2':False,'level3':False, 'level4':False}
    colordict = {'yellow':(255,255,0),'blue':(40,126,255),'black':(0,0,0),\
    'white':(255,255,255),'pink':(255,131,239),'red':(255,0,0),'orange':(255, 80, 42),\
    'green':(94,203,46),'purple':(204,0,182)}
    total_score = 18
    obstacle_index = dict()
    moving_obs_y_1,moving_obs_y_2 = 0,0
    bullet_pos_n_dir = dict()
    ticks = 0 #total loop counts

    snakey = AISnake(pos=(screenWidth-gridSize,(screenHeight/gridSize-1)//2*gridSize),length=aisnake_length)

    snake_game()

def initial():
    global root,screenWidth,screenHeight,gridSize,menuscreen

    screenWidth = 1080
    screenHeight = 600
    gridSize = 40

    root = tk.Tk()
    root.title('Snake')
    root.geometry(f'{screenWidth}x{screenHeight}-100+10')
    root['bg'] = 'black'
    
    menu()

def restart():
    pygame.quit()
    menu()

def menu():
    global menuscreen,play_button,difficlulty_button,tutorial_button,root,\
    screenWidth,screenHeight,gridSize,to_menu_button,blackk

    # if menuscreen exist → do nothing
    # if not → create it
    try:
        bool(menuscreen)
    except:
        menuscreen = tk.Frame(root,width=1080,height=600,bg='black')
        menuscreen.pack()

    blackk = tk.Label(menuscreen,bg='black')
    blackk.place(x=0,y=0,width=screenWidth,height=screenHeight)

    img = Image.open("snakecover.png")
    img = img.resize((screenWidth,screenHeight))
    renderimg = ImageTk.PhotoImage(img)

    cover = tk.Label(menuscreen, image=renderimg)
    cover.image = renderimg
    cover.place(relx=0.5,rely=0.5,anchor='center')
    cover['bd']=0

    #buttons
    play_button = tk.Button(menuscreen,text='Play',command=main)
    difficlulty_button = tk.Button(menuscreen,text='Difficulty',command=difficlulty)
    tutorial_button = tk.Button(menuscreen,text='Tutorials',command=page_1)

    play_button.place(anchor='center',relx=0.18,rely=0.87,width=280,height=120)
    play_button.config(font=('Arial',48),bg='#0036ff',fg='white')
    play_button.config(activebackground=play_button['bg'],activeforeground=play_button['fg'],bd=3,relief='raised')

    difficlulty_button.place(anchor='center',relx=0.6,rely=0.87,width=200,height=100)
    difficlulty_button.config(font=('Arial',30),bg='#ff7000',fg='white')
    difficlulty_button.config(activebackground=difficlulty_button['bg'],activeforeground=difficlulty_button['fg'],bd=3,relief='raised')

    tutorial_button.place(anchor='center',relx=0.85,rely=0.87,width=200,height=100)
    tutorial_button.config(font=('Arial',30),bg='#ff7000',fg='white')
    tutorial_button.config(activebackground=tutorial_button['bg'],activeforeground=tutorial_button['fg'],bd=3,relief='raised')
    
    pygame.init()
    root.mainloop()

def difficlulty():
    '''select difficulty'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    difficlultycanvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    difficlultycanvas.place(x=0,y=0)

    hard_button = tk.Button(difficlultycanvas,text='Hard',command=hard)
    hard_button.place(anchor='s',relx=0.5,rely=0.4,width=200,height=100)
    hard_button.config(font=('Arial',30),bg='#ff0000',fg='white')
    hard_button.config(activebackground=hard_button['bg'],activeforeground=hard_button['fg'],bd=3,relief='raised')

    easy_button = tk.Button(difficlultycanvas,text='Default',command=easy)
    easy_button.place(anchor='s',relx=0.5,rely=0.8,width=200,height=100)
    easy_button.config(font=('Arial',30),bg='#ff0000',fg='white')
    easy_button.config(activebackground=easy_button['bg'],activeforeground=easy_button['fg'],bd=3,relief='raised')

def hard():
    global init_delay,aisnake_length,aisnake_speed,ragemode_length,score_multiplier
    init_delay = 120
    aisnake_length = 10
    ragemode_length = 5
    aisnake_speed = 2
    score_multiplier = 2
    menu()

def easy():
    global init_delay,aisnake_length,aisnake_speed,ragemode_length,score_multiplier
    init_delay = 140
    aisnake_length = 6
    ragemode_length = 3
    aisnake_speed = 4
    score_multiplier = 1
    menu()

def page_1():
    '''controls & food explained'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    p1canvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    p1canvas.place(x=0,y=0)

    to_menu_button = tk.Button(p1canvas,text='Menu',command=menu)
    to_menu_button.place(anchor='s',relx=0.5,rely=1,width=130,height=60)
    to_menu_button.config(font=('Arial',18),bg='#0036ff',fg='white')
    to_menu_button.config(activebackground=to_menu_button['bg'],activeforeground=to_menu_button['fg'],bd=3,relief='raised')
    
    to_p2_button = tk.Button(p1canvas,text='Next Page',command=page_2)
    to_p2_button.place(anchor='se',relx=1,rely=1,width=150,height=60)
    to_p2_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p2_button.config(activebackground=to_p2_button['bg'],activeforeground=to_p2_button['fg'],bd=3,relief='raised')

    img = Image.open("startpic.png")
    img = img.resize((900,int(900*(867/1613))))
    renderimg = ImageTk.PhotoImage(img)

    ppimg = tk.Label(p1canvas, image=renderimg)
    ppimg.image = renderimg
    ppimg.place(relx=0.5,rely=0.45,anchor='center')
    ppimg['bd']=0

    text_you = tk.Label(p1canvas,text='This white block is you,\nuse up/down/left/right arrow to move.\nYou can also press p to pause.',font=('Segoe Print',16),bd=2,relief='solid')
    text_you.place(anchor='center',relx=0.25,rely=0.27,width=450,height=140)
    text_you.config(bg='#7ecd62',fg='black')

    text_food = tk.Label(p1canvas,text='This yellow block is food, eat it to become longer, \nand your score will +1 (+2 for Hard mode).\nThe speed will also become faster.',font=('Segoe Print',16),bd=2,relief='solid')
    text_food.place(anchor='center',relx=0.6,rely=0.68,width=580,height=140)
    text_food.config(bg='#7ecd62',fg='black')

    root.update()

def page_2():
    '''slowpill explained'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    p2canvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    p2canvas.place(x=0,y=0)

    to_p1_button = tk.Button(p2canvas,text='Previous Page',command=page_1)
    to_p1_button.place(anchor='sw',relx=0,rely=1,width=200,height=60)
    to_p1_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p1_button.config(activebackground=to_p1_button['bg'],activeforeground=to_p1_button['fg'],bd=3,relief='raised')

    to_menu_button = tk.Button(p2canvas,text='Menu',command=menu)
    to_menu_button.place(anchor='s',relx=0.5,rely=1,width=130,height=60)
    to_menu_button.config(font=('Arial',18),bg='#0036ff',fg='white')
    to_menu_button.config(activebackground=to_menu_button['bg'],activeforeground=to_menu_button['fg'],bd=3,relief='raised')
    
    to_p3_button = tk.Button(p2canvas,text='Next Page',command=page_3)
    to_p3_button.place(anchor='se',relx=1,rely=1,width=150,height=60)
    to_p3_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p3_button.config(activebackground=to_p3_button['bg'],activeforeground=to_p3_button['fg'],bd=3,relief='raised')

    img = Image.open("slowpillpic.png")
    img = img.resize((900,int(900*(867/1613))))
    renderimg = ImageTk.PhotoImage(img)

    ppimg = tk.Label(p2canvas, image=renderimg)
    ppimg.image = renderimg
    ppimg.place(relx=0.5,rely=0.45,anchor='center')
    ppimg['bd']=0

    text_slowpill = tk.Label(p2canvas,text='This red block is slowpill,\nit will be generated when you reach a certain speed,\neat it to become slower. ',font=('Segoe Print',16),bd=2,relief='solid')
    text_slowpill.place(anchor='center',relx=0.6,rely=0.5,width=600,height=120)
    text_slowpill.config(bg='#7ecd62',fg='black')

    root.update()

def page_3():
    '''go to next level explained'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    p3canvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    p3canvas.place(x=0,y=0)

    to_p2_button = tk.Button(p3canvas,text='Previous Page',command=page_2)
    to_p2_button.place(anchor='sw',relx=0,rely=1,width=200,height=60)
    to_p2_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p2_button.config(activebackground=to_p2_button['bg'],activeforeground=to_p2_button['fg'],bd=3,relief='raised')

    to_menu_button = tk.Button(p3canvas,text='Menu',command=menu)
    to_menu_button.place(anchor='s',relx=0.5,rely=1,width=130,height=60)
    to_menu_button.config(font=('Arial',18),bg='#0036ff',fg='white')
    to_menu_button.config(activebackground=to_menu_button['bg'],activeforeground=to_menu_button['fg'],bd=3,relief='raised')
    
    to_p4_button = tk.Button(p3canvas,text='Next Page',command=page_4)
    to_p4_button.place(anchor='se',relx=1,rely=1,width=150,height=60)
    to_p4_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p4_button.config(activebackground=to_p4_button['bg'],activeforeground=to_p4_button['fg'],bd=3,relief='raised')

    img = Image.open("nextlevelpic.png")
    img = img.resize((900,int(900*(867/1613))))
    renderimg = ImageTk.PhotoImage(img)

    ppimg = tk.Label(p3canvas, image=renderimg)
    ppimg.image = renderimg
    ppimg.place(relx=0.5,rely=0.45,anchor='center')
    ppimg['bd']=0

    text_slowpill = tk.Label(p3canvas,text='When you reach a certain score,\na hole will appear,\ngo through the hole to enter the next level. ',font=('Segoe Print',16),bd=2,relief='solid')
    text_slowpill.place(anchor='center',relx=0.6,rely=0.6,width=550,height=120)
    text_slowpill.config(bg='#7ecd62',fg='black')

    root.update()

def page_4():
    '''obstacle explained'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    p4canvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    p4canvas.place(x=0,y=0)

    to_p3_button = tk.Button(p4canvas,text='Previous Page',command=page_3)
    to_p3_button.place(anchor='sw',relx=0,rely=1,width=200,height=60)
    to_p3_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p3_button.config(activebackground=to_p3_button['bg'],activeforeground=to_p3_button['fg'],bd=3,relief='raised')

    to_menu_button = tk.Button(p4canvas,text='Menu',command=menu)
    to_menu_button.place(anchor='s',relx=0.5,rely=1,width=130,height=60)
    to_menu_button.config(font=('Arial',18),bg='#0036ff',fg='white')
    to_menu_button.config(activebackground=to_menu_button['bg'],activeforeground=to_menu_button['fg'],bd=3,relief='raised')
    
    to_p5_button = tk.Button(p4canvas,text='Next Page',command=page_5)
    to_p5_button.place(anchor='se',relx=1,rely=1,width=150,height=60)
    to_p5_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p5_button.config(activebackground=to_p5_button['bg'],activeforeground=to_p5_button['fg'],bd=3,relief='raised')

    img = Image.open("obstaclepic.png")
    img = img.resize((900,int(900*(867/1613))))
    renderimg = ImageTk.PhotoImage(img)

    ppimg = tk.Label(p4canvas, image=renderimg)
    ppimg.image = renderimg
    ppimg.place(relx=0.5,rely=0.45,anchor='center')
    ppimg['bd']=0

    text_obstacle = tk.Label(p4canvas,text="This big blue thing is obstacle,\nyou die if you touch it.\nYou'll also die if you touch the blue parameters.",font=('Segoe Print',16),bd=2,relief='solid')
    text_obstacle.place(anchor='center',relx=0.6,rely=0.75,width=550,height=120)
    text_obstacle.config(bg='#7ecd62',fg='black')

    root.update()

def page_5():
    '''levels explained'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    p5canvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    p5canvas.place(x=0,y=0)

    to_p4_button = tk.Button(p5canvas,text='Previous Page',command=page_4)
    to_p4_button.place(anchor='sw',relx=0,rely=1,width=200,height=60)
    to_p4_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p4_button.config(activebackground=to_p4_button['bg'],activeforeground=to_p4_button['fg'],bd=3,relief='raised')

    to_menu_button = tk.Button(p5canvas,text='Menu',command=menu)
    to_menu_button.place(anchor='s',relx=0.5,rely=1,width=130,height=60)
    to_menu_button.config(font=('Arial',18),bg='#0036ff',fg='white')
    to_menu_button.config(activebackground=to_menu_button['bg'],activeforeground=to_menu_button['fg'],bd=3,relief='raised')
    
    to_p6_button = tk.Button(p5canvas,text='Next Page',command=page_6)
    to_p6_button.place(anchor='se',relx=1,rely=1,width=150,height=60)
    to_p6_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p6_button.config(activebackground=to_p6_button['bg'],activeforeground=to_p6_button['fg'],bd=3,relief='raised')

    img = Image.open("aisnakepic.png")
    img = img.resize((900,int(900*(867/1613))))
    renderimg = ImageTk.PhotoImage(img)

    ppimg = tk.Label(p5canvas, image=renderimg)
    ppimg.image = renderimg
    ppimg.place(relx=0.5,rely=0.45,anchor='center')
    ppimg['bd']=0

    text_levelsexplain = tk.Label(p5canvas,text="This game has 4 level,\n1st level: normal snake game\n2nd level: fixed obstacle\n3rd level: falling obstacles\nfinal level: boss-AI snake.",font=('Segoe Print',16),bd=2,relief='solid')
    text_levelsexplain.place(anchor='center',relx=0.3,rely=0.3,width=370,height=200)
    text_levelsexplain.config(bg='#7ecd62',fg='black')

    text_aisnake = tk.Label(p5canvas,text="This purple snake is the boss - AI snake.\nIt will follow you,\nand you'll lose health (also score) if it touches you.\n(your health = your length)",font=('Segoe Print',16),bd=2,relief='solid')
    text_aisnake.place(anchor='center',relx=0.7,rely=0.7,width=560,height=180)
    text_aisnake.config(bg='#7ecd62',fg='black')

    root.update()

def page_6():
    '''ammunition and others explained'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    p6canvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    p6canvas.place(x=0,y=0)

    to_p5_button = tk.Button(p6canvas,text='Previous Page',command=page_5)
    to_p5_button.place(anchor='sw',relx=0,rely=1,width=200,height=60)
    to_p5_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p5_button.config(activebackground=to_p5_button['bg'],activeforeground=to_p5_button['fg'],bd=3,relief='raised')

    to_menu_button = tk.Button(p6canvas,text='Menu',command=menu)
    to_menu_button.place(anchor='s',relx=0.5,rely=1,width=130,height=60)
    to_menu_button.config(font=('Arial',18),bg='#0036ff',fg='white')
    to_menu_button.config(activebackground=to_menu_button['bg'],activeforeground=to_menu_button['fg'],bd=3,relief='raised')
    
    to_p7_button = tk.Button(p6canvas,text='Next Page',command=page_7)
    to_p7_button.place(anchor='se',relx=1,rely=1,width=150,height=60)
    to_p7_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p7_button.config(activebackground=to_p7_button['bg'],activeforeground=to_p7_button['fg'],bd=3,relief='raised')

    img = Image.open("fireballpic.png")
    img = img.resize((900,int(900*(867/1613))))
    renderimg = ImageTk.PhotoImage(img)

    ppimg = tk.Label(p6canvas, image=renderimg)
    ppimg.image = renderimg
    ppimg.place(relx=0.5,rely=0.45,anchor='center')
    ppimg['bd']=0

    text_ammunition = tk.Label(p6canvas,text="This green block is ammunition,\neat it to get fireballs,\nyou can store a maximum of 3 firaballs.",font=('Segoe Print',16),bd=2,relief='solid')
    text_ammunition.place(anchor='center',relx=0.75,rely=0.22,width=450,height=130)
    text_ammunition.config(bg='#7ecd62',fg='black')

    text_fireball = tk.Label(p6canvas,text="Press space to fire a fireball.\nIf the fireball hit the boss, boss's health will -1,\n and your score will +2 (+4 for Hard mode)",font=('Segoe Print',16),bd=2,relief='solid')
    text_fireball.place(anchor='center',relx=0.3,rely=0.65,width=550,height=120)
    text_fireball.config(bg='#7ecd62',fg='black')

    text_fireballicon = tk.Label(p6canvas,text="This shows how many fireballs you can shoot.",font=('Segoe Print',16),bd=2,relief='solid')
    text_fireballicon.place(anchor='center',relx=0.27,rely=0.17,width=530,height=50)
    text_fireballicon.config(bg='#7ecd62',fg='black')

    root.update()

def page_7():
    '''rage mode explained'''
    global menuscreen,root,screenWidth,screenHeight,gridSize

    p7canvas = tk.Canvas(menuscreen,width=screenWidth,height=screenHeight,bg='black',highlightthickness=0)
    p7canvas.place(x=0,y=0)

    to_p6_button = tk.Button(p7canvas,text='Previous Page',command=page_6)
    to_p6_button.place(anchor='sw',relx=0,rely=1,width=200,height=60)
    to_p6_button.config(font=('Arial',18),bg='#ff0000',fg='white')
    to_p6_button.config(activebackground=to_p6_button['bg'],activeforeground=to_p6_button['fg'],bd=3,relief='raised')

    to_menu_button = tk.Button(p7canvas,text='Menu',command=menu)
    to_menu_button.place(anchor='s',relx=0.5,rely=1,width=130,height=60)
    to_menu_button.config(font=('Arial',18),bg='#0036ff',fg='white')
    to_menu_button.config(activebackground=to_menu_button['bg'],activeforeground=to_menu_button['fg'],bd=3,relief='raised')

    img = Image.open("ragemodepic.png")
    img = img.resize((900,int(900*(867/1613))))
    renderimg = ImageTk.PhotoImage(img)

    ppimg = tk.Label(p7canvas, image=renderimg)
    ppimg.image = renderimg
    ppimg.place(relx=0.5,rely=0.45,anchor='center')
    ppimg['bd']=0

    text_levelsexplain = tk.Label(p7canvas,text='When the boss is below a certain health,\n"rage mode" will be activated.\nIt will 甩尾, and thus you\'re more likely to be hit.',font=('Segoe Print',16),bd=2,relief='solid')
    text_levelsexplain.place(anchor='center',relx=0.4,rely=0.25,width=560,height=130)
    text_levelsexplain.config(bg='#7ecd62',fg='black')

    root.update()

def page_8():
    pass

def tutorials():
    tutor = TutorialsPages()
    tutor.page_1()


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

    font = pygame.font.SysFont('Arial', 40)
    button_text = font.render(text, True, colordict[text_color])
    button_text_rect = button_text.get_rect()
    button_text_rect.center = (x_pos+width/2 , y_pos+height/2)
    screen.blit(button_text, button_text_rect)
    pygame.display.flip()

def quit_game():
    pygame.quit()
    sys.exit() 

def pause():
    global isGame,colordict,screen,mouse_pos,colordict
    while isGame:
        screen.fill(colordict['black'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False
        # button()
        mouse_pos = pygame.mouse.get_pos()
        x_pos,y_pos,width,height=screenWidth/2-120/2,screenHeight/2-60/2,150,75

        if (x_pos < mouse_pos[0] < x_pos + width #click the button to resume
            and y_pos < mouse_pos[1] < y_pos + height):
            pygame.draw.rect(screen, colordict['pink'], (x_pos,y_pos,width,height))
            if pygame.mouse.get_pressed()[0] == 1:
                break
        else:
            pygame.draw.rect(screen, colordict['red'], (x_pos,y_pos,width,height))

        font = pygame.font.SysFont('Arial', 40)
        button_text = font.render('Resume', True, colordict['white'])
        button_text_rect = button_text.get_rect()
        button_text_rect.center = (x_pos+width/2 , y_pos+height/2)
        screen.blit(button_text, button_text_rect)
        pygame.display.flip()

def game_finished():
    global tail_length, screen, delay, isGame, colordict
    time.sleep(2)
    screen.fill(colordict['black'])

    font = pygame.font.SysFont('Segoe Print', 30)
    score_text = font.render("Congrats you got " + str(total_score) 
        + " points!",4,colordict['red'])
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (screenWidth/2 , screenHeight/2)
    screen.blit(score_text,score_text_rect)
    pygame.display.flip()
    time.sleep(2) # time.delay
    screen.fill(colordict['black'])
    
    while isGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False
        button('red','pink','Quit','white',380,screenHeight/2-60/2,150,75,quit_game)
        button('red','pink','Menu','white',580,screenHeight/2-60/2,150,75,restart)
        pygame.display.update()

def obstacle(x,y,w,h,index):
    global screen, colordict, x_player, y_player, x_food, y_food,\
    l_obs_x,l_obs_y,l_obs_w,l_obs_h,obstacle_index,gridSize
 
    #die if snake touches obstacles
    if ((x)*gridSize < (x_player*2+gridSize)/2 < (x+w)*gridSize 
        and (y)*gridSize < (y_player*2+gridSize)/2 < (y+h)*gridSize):
        game_finished()

    #die if "bodies" touch obstacle
    for body in bodies:
        if ((x)*gridSize < (body[0]*2+gridSize)/2 < (x+w)*gridSize 
            and (y)*gridSize < (body[1]*2+gridSize)/2 < (y+h)*gridSize):
            game_finished()    

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
    global x_food,y_food,x_ammunition,y_ammunition,x_slowpill,y_slowpill,bodies,\
    screenWidth, screenHeight, gridSize,l_obs_x,l_obs_y,l_obs_w,l_obs_h
    x_food = random.randint(1, screenWidth/gridSize - 2) * gridSize # grid num * grid size
    y_food = random.randint(1, screenHeight/gridSize - 2) * gridSize # make it only generate in parameter

    for obs_x,obs_y,obs_w,obs_h in zip(l_obs_x,l_obs_y,l_obs_w,l_obs_h):
        while ((x_food, y_food) in bodies
            or obs_x*gridSize < x_food+gridSize/2 < (obs_x+obs_w)*gridSize
            and obs_y*gridSize < y_food+gridSize/2 < (obs_y+obs_h)*gridSize):
            x_food = random.randint(1, screenWidth/gridSize - 2) * gridSize # grid num * grid size
            y_food = random.randint(1, screenHeight/gridSize - 2) * gridSize # make it only generate in parameter

    if x_food == x_slowpill and y_food == y_slowpill or x_food == x_ammunition and y_food == y_ammunition:
        x_food = random.randint(1, screenWidth/gridSize - 2) * gridSize
        y_food = random.randint(1, screenHeight/gridSize - 2) * gridSize

    return x_food, y_food

#same as a food except speed set back to default when eaten
def generate_slowpill_pos():
    '''a pill that make u move slower'''
    global x_food,y_food,x_ammunition,y_ammunition,x_slowpill,y_slowpill,bodies,\
    screenWidth, screenHeight, gridSize,l_obs_x,l_obs_y,l_obs_w,l_obs_h
    x_slowpill = random.randint(1, screenWidth/gridSize - 2) * gridSize # grid num * grid size
    y_slowpill = random.randint(1, screenHeight/gridSize - 2) * gridSize # make it only generate in parameter

    for obs_x,obs_y,obs_w,obs_h in zip(l_obs_x,l_obs_y,l_obs_w,l_obs_h):
        while ((x_slowpill, y_slowpill) in bodies
            or obs_x*gridSize < (x_slowpill*2+gridSize)/2 < (obs_x+obs_w)*gridSize 
             and obs_y*gridSize < (y_slowpill*2+gridSize)/2 < (obs_y+obs_h)*gridSize):
            x_slowpill = random.randint(1, screenWidth/gridSize - 2) * gridSize # grid num * grid size
            y_slowpill = random.randint(1, screenHeight/gridSize - 2) * gridSize # make it only generate in parameter
    if x_slowpill == x_food and y_slowpill == y_food or x_slowpill == x_ammunition and y_slowpill == y_ammunition:
        x_slowpill = random.randint(1, screenWidth/gridSize - 2) * gridSize
        y_slowpill = random.randint(1, screenHeight/gridSize - 2) * gridSize

    return x_slowpill, y_slowpill

def level_1():
    global tail_length, next_level_unlocked, x_player, y_player,obstacle,screenHeight,\
    screenWidth,gridSize,level_2,delay,level_common,obstacle_index

    if tail_length == 2: 
        next_level_unlocked = True

    level_common(level_1,level_2)

def level_2():
    """level 2 of the game"""
    global next_level_unlocked, obstacle, dict_level, gridSize, generate_food,screenHeight,\
    screenWidth,gridSize,tail_length,x_player,y_player,delay,level_3,level_common,obstacle_index

    if tail_length == 2:
        next_level_unlocked = True
        obstacle(0,0,0,0,obstacle_index['level2_obstacle'])
    else:
        next_level_unlocked = False

        obstacle_index['level2_obstacle'] = 8
        obstacle(10,7,4,4,obstacle_index['level2_obstacle'])


    level_common(level_2,level_3)

def level_3():
    """level 3 - falling obstacles"""
    global next_level_unlocked, obstacle, dict_level, gridSize, generate_food,screenHeight,\
    screenWidth,gridSize,tail_length,x_player,y_player,delay,level_3,level_common,obstacle_index,\
    moving_obs_y_1,moving_obs_y_2,moving_obstacle

    if tail_length == 7: 
        next_level_unlocked = True
        obstacle(0,0,0,0,obstacle_index['level3_moving_obstacle_1'])
        obstacle(0,0,0,0,obstacle_index['level3_moving_obstacle_2'])
    else:
        next_level_unlocked = False
        moving_obs_y_1 += 1
        moving_obs_y_2 += 1
        obstacle_index['level3_moving_obstacle_1'] = 9
        obstacle_index['level3_moving_obstacle_2'] = 10
        obstacle(7,moving_obs_y_1,1,3,obstacle_index['level3_moving_obstacle_1'])
        obstacle(17,moving_obs_y_2,1,3,obstacle_index['level3_moving_obstacle_2'])
        if moving_obs_y_1 >= screenHeight/gridSize:
            moving_obs_y_1 = 0
        if moving_obs_y_2 >= screenHeight/gridSize:
            moving_obs_y_2 = 0
    
    level_common(level_3,level_4)

def level_4():
    """level 4 - meet boss"""
    global next_level_unlocked, obstacle, dict_level, gridSize, generate_food,screenHeight,\
    screenWidth,gridSize,tail_length,x_player,y_player,delay,level_3,level_common,obstacle_index,\
    keys,x_ammunition,y_ammunition,snakey,ticks,total_score,bodies,x_food,y_food,x_slowpill,y_slowpill,\
    aisnake_speed,ragemode_length,stabbed_text,stabbed_time

    next_level_unlocked = False

    #press space to shoot
    if keys[pygame.K_SPACE]:
        bullet()
    if len(bullet_pos_n_dir) != 0:
        bullet_move()

    if ticks%aisnake_speed == 0: #make the AI snake move slower
        snakey.direction()
        snakey.update_pos()
        snakey.update_bodies()
    snakey.bodies_correction()
    snakey.draw_bodies()
    snakey.lose_health()
    snakey.if_die() #then game over
    if snakey.length <= ragemode_length:
        snakey.rage_mode()

    # if user touches AI snake
    for body in bodies:
        for ai_body in snakey.bodies:
            if (body[0] < ai_body[0]+gridSize/2 < body[0] + gridSize
                and body[1] < ai_body[1]+gridSize/2 < body[1] + gridSize):
                tail_length -= 1

                #show "You're hurt!" when hurt by aisnake
                font = pygame.font.SysFont('Segoe UI Black', 25)
                stabbed_text = font.render("You're hurt!", True, colordict['black'])
                stabbed_time = game_time//1000

                total_score -= 1
    
    # when AI snake touches the "foods", they generate elsewhere
    for ai_body in snakey.bodies:
        if x_food == ai_body[0] and y_food == ai_body[1]:
            x_food = random.randint(1, screenWidth/gridSize - 2) * gridSize
            y_food = random.randint(1, screenHeight/gridSize - 2) * gridSize
        if x_slowpill == ai_body[0] and y_slowpill == ai_body[1]:
            x_slowpill = random.randint(1, screenWidth/gridSize - 2) * gridSize
            y_slowpill = random.randint(1, screenHeight/gridSize - 2) * gridSize
        if x_ammunition == ai_body[0] and y_ammunition == ai_body[1]:
            x_ammunition = random.randint(1, screenWidth/gridSize - 2) * gridSize
            y_ammunition = random.randint(1, screenHeight/gridSize - 2) * gridSize

    level_common(level_4,level_5)

def level_5(): #end_game
    ''' the end of the game persumably'''
    pass

def level_common(level,next_level):
    global next_level_unlocked, obstacle, dict_level, gridSize, generate_food,screenHeight,\
    screenWidth,gridSize,tail_length,x_player,y_player,delay,level_1,level_2,level_3,obstacle_index,\
    level_4,init_delay

    if level != level_1:
        dict_level['level%s'%str(int(list(str(level))[list(str(level)).index('_')+1])-1)] = False
        dict_level['level%s'%str(list(str(level))[list(str(level)).index('_')+1])] = True

    #parameters
    obstacle_index['top_bar'] = 0
    obstacle_index['bottom_bar'] = 1
    obstacle_index['left_top_bar'] = 2
    obstacle_index['left_bottom_bar'] = 3
    obstacle_index['right_top_bar'] = 4
    obstacle_index['right_bottom_bar'] = 5
    obstacle(0,0,screenWidth/gridSize,1,obstacle_index['top_bar']) #top bar
    obstacle(0,screenHeight/gridSize-1,screenWidth/gridSize,1,obstacle_index['bottom_bar']) #bottom bar
    obstacle(0,0,1,(screenHeight/gridSize-1)//2,obstacle_index['left_top_bar']) #left top bar
    obstacle(0,(screenHeight/gridSize-1)//2+1,1,(screenHeight/gridSize-1)//2,obstacle_index['left_bottom_bar']) #left bottom bar
    obstacle(screenWidth/gridSize-1,0,1,(screenHeight/gridSize-1)//2,obstacle_index['right_top_bar']) #right top bar
    obstacle(screenWidth/gridSize-1,(screenHeight/gridSize-1)//2+1,1,(screenHeight/gridSize-1)//2,obstacle_index['right_bottom_bar']) #right bottom bar

    if next_level_unlocked == False:
        generate_food = True
        obstacle_index['right_middle_block'] = 6
        obstacle(screenWidth/gridSize-1,(screenHeight/gridSize-1)//2,1,1,obstacle_index['right_middle_block']) #right middle block
        if level == level_1:
            obstacle_index['left_middle_block'] = 7
            obstacle(0,(screenHeight/gridSize-1)//2,1,1,obstacle_index['left_middle_block']) #left middle block

    elif next_level_unlocked == True:
        obstacle(0,0,0,0,obstacle_index['right_middle_block']) #open a "hole" on the right parameter
        if x_player+gridSize/2 >= screenWidth-gridSize and (screenHeight-gridSize)//2 < y_player+gridSize/2 < (screenHeight-gridSize)//2+gridSize:
            tail_length = 1
            #snake goes into the hole then appears on the left
            x_player,y_player = 1*gridSize,(screenHeight-gridSize)/2
            bodies.append((x_player, y_player)) #to update to bodies immediately
            while (len(bodies) > tail_length):
                del bodies[0]
            if level == level_1:
                obstacle(0,0,0,0,obstacle_index['left_middle_block']) #open a "hole" on the left parameter

            delay = init_delay
            next_level()

def bullet():
    '''bullet in level 4'''
    global x_player,y_player,left,right,up,down,bullet_pos_n_dir,ammunition_count
    
    if ammunition_count > 0:
        if up:
            bullet_pos_n_dir[(x_player,y_player)] = 'up'
        elif down:
            bullet_pos_n_dir[(x_player,y_player)] = 'down'
        elif left:
            bullet_pos_n_dir[(x_player,y_player)] = 'left'
        elif right:
            bullet_pos_n_dir[(x_player,y_player)] = 'right'
        ammunition_count -= 1

def bullet_move():
    '''how bullets move'''
    global bullet_pos_n_dir,velocity

    for pos in list(bullet_pos_n_dir.keys()):
        temp_pos = [pos[0],pos[1]] #bc tuple can't change value
        k = 1.2 #bullet speed multiplier
        if bullet_pos_n_dir[pos] == 'up':
            temp_pos[1] -= k*velocity
        elif bullet_pos_n_dir[pos] == 'down':
            temp_pos[1] += k*velocity
        elif bullet_pos_n_dir[pos] == 'left':
            temp_pos[0] -= k*velocity
        elif bullet_pos_n_dir[pos] == 'right':
            temp_pos[0] += k*velocity

        #update new pos back to tuple replacing original tuple in dict
        bullet_pos_n_dir[tuple(temp_pos)] = bullet_pos_n_dir.pop(pos)

    #delete bullet when out of boundary
    for pos in list(bullet_pos_n_dir.keys()):
        if (not 0 < pos[0] < screenWidth-gridSize 
            or not 0 < pos[1] < screenHeight-gridSize):
            del bullet_pos_n_dir[pos]

def generate_ammunition_pos():
    '''ammunition'''
    global x_food,y_food,x_ammunition,y_ammunition,x_slowpill,y_slowpill,\
    bodies, screenWidth, screenHeight, gridSize,l_obs_x,l_obs_y,l_obs_w,l_obs_h

    x_ammunition = random.randint(1, screenWidth/gridSize - 2) * gridSize # grid num * grid size
    y_ammunition = random.randint(1, screenHeight/gridSize - 2) * gridSize # make it only generate in parameter

    for obs_x,obs_y,obs_w,obs_h in zip(l_obs_x,l_obs_y,l_obs_w,l_obs_h):
        while ((x_ammunition, y_ammunition) in bodies
            or obs_x*gridSize < (x_ammunition*2+gridSize)/2 < (obs_x+obs_w)*gridSize 
             and obs_y*gridSize < (y_ammunition*2+gridSize)/2 < (obs_y+obs_h)*gridSize):
            x_ammunition = random.randint(1, screenWidth/gridSize - 2) * gridSize # grid num * grid size
            y_ammunition = random.randint(1, screenHeight/gridSize - 2) * gridSize # make it only generate in parameter
    if x_ammunition == x_slowpill and y_ammunition == y_slowpill or x_ammunition == x_food and y_ammunition == y_food:
        x_ammunition = random.randint(1, screenWidth/gridSize - 2) * gridSize
        y_ammunition = random.randint(1, screenHeight/gridSize - 2) * gridSize

    return x_ammunition, y_ammunition


class AISnake:
    global x_player,y_player,velocity,ticks,bullet_pos_n_dir,total_score,game_time
    def __init__(self,pos,length):
        self.x = pos[0]
        self.y = pos[1]
        self.bodies = [(self.x + (length+1-i)*gridSize, self.y) for i in range(length)] #head pos is the last ones in list]
        self.length = length

    def direction(self):
        '''update direction'''
        
        if (y_player-self.y) != 0 and (x_player-self.x) != 0:
            if -1 <= (y_player-self.y)/(x_player-self.x) <= 1 and x_player < self.x:
                return 'left'
            elif -1 <= (y_player-self.y)/(x_player-self.x) <= 1 and x_player > self.x:
                return 'right'
            elif y_player < self.y:
                return 'up'
            elif y_player > self.y:
                return 'down'
        elif x_player-self.x == 0:
            if y_player < self.y:
                return 'up'
            elif y_player > self.y:
                return 'down'
        elif y_player-self.y == 0:
            if x_player < self.x:
                return 'left'
            elif x_player > self.x:
                return 'right'

    def update_pos(self):
        '''update position'''
        k = 1 # k = speed multiplier
        
        if self.direction() == 'left':
            self.x -= k*velocity
        elif self.direction() == 'right':
            self.x += k*velocity
        elif self.direction() == 'up':
            self.y -= k*velocity
        elif self.direction() == 'down':
            self.y += k*velocity

    def update_bodies(self):
        '''append bodies'''
        self.bodies.append([self.x,self.y])

    def bodies_correction(self):
        ''' make the AI snake be in correct length'''
        while len(self.bodies) > self.length:
            del self.bodies[0]

    def draw_bodies(self):
        '''draw the AI snake'''
        for body in self.bodies :
            pygame.draw.rect(screen, colordict['purple'], (body[0], body[1], gridSize, gridSize))

    def lose_health(self):
        '''lose health(length) when hit by fireball(bullet)'''
        global total_score,sot_text,sot_time,score_multiplier

        for pos in list(bullet_pos_n_dir.keys()):
            for body in self.bodies:
                if (body[0] < pos[0]+gridSize/2 < body[0]+gridSize
                    and body[1] < pos[1]+gridSize/2 < body[1]+gridSize):
                    self.length -= 1

                    # show 'Shot on target!' when hurt aisnake
                    font = pygame.font.SysFont('Segoe UI Black', 25)
                    sot_text = font.render('Shot on target!', True, colordict['black'])
                    sot_time = game_time//1000

                    total_score += 2**score_multiplier
                    del bullet_pos_n_dir[pos]

    def if_die(self):
        '''die'''
        if self.length == 0:
            game_finished()

    def rage_mode(self):
        '''rage mode'''
        global s,t
        if self.bodies[0][0] > self.x and self.bodies[0][1] == self.y: #3 o'clock
            s,t = 1,-1
        elif self.bodies[0][0] > self.x and self.bodies[0][1] < self.y: #1.5 o'clock
            s,t =  0,-1
        elif self.bodies[0][0] == self.x and self.bodies[0][1] < self.y: #12 o'clock
            s,t =  -1,-1
        elif self.bodies[0][0] < self.x and self.bodies[0][1] < self.y: #10.5 o'clock
            s,t =  -1,0
        elif self.bodies[0][0] < self.x and self.bodies[0][1] == self.y: #9 o'clock
            s,t =  -1,1
        elif self.bodies[0][0] < self.x and self.bodies[0][1] > self.y: #7.5 o'clock
            s,t =  0,1
        elif self.bodies[0][0] == self.x and self.bodies[0][1] > self.y: #6 o'clock
            s,t =  1,1
        elif self.bodies[0][0] > self.x and self.bodies[0][1] > self.y: #4.5 o'clock
            s,t =  1,0
        for i in range(len(self.bodies)):
            j = len(self.bodies) - (i+1)
            self.bodies[i][0] = self.x + s*j*gridSize
            self.bodies[i][1] = self.y + t*j*gridSize
           
#Game Loop
def snake_game():
    '''game loop'''
    global generate_slowpill,x_slowpill,y_slowpill,isEaten_slowpill, game_speed,\
    x_food, y_food, x_player, y_player, gridSize, screenWidth, screenHeight, bodies,\
    delay, tail_length, screen, isGame, isEaten_food, colordict, next_level_unlocked,\
    generate_food, next_level_unlocked,l_obs_x,l_obs_y,l_obs_w,l_obs_h,level_1,level_2,\
    total_score,obstacle_index,bullet_pos_n_dir,up,down,right,left,velocity,keys,\
    isEaten_ammunition,generate_ammunition,x_ammunition, y_ammunition,ammunition_count,\
    ticks,game_time,root,init_delay,sot_text,sot_time,stabbed_text,stabbed_time,score_multiplier
    
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    velocity = gridSize
    up = False
    down = False
    right = False 
    left = False

    score_now = 0 #for determining the generate slowpill threshold

    print_sot,print_stabbed = False,False

    while isGame :
        ticks += 1

        #Game's delay 
        pygame.time.delay(delay)

        screen.fill((0, 0, 0))

        #start_time updates as long as snake doensn't leave (i.e. move)
        if x_player == 1*gridSize and y_player == 1*gridSize:
            start_time = pygame.time.get_ticks()
        game_time = pygame.time.get_ticks() - start_time #in-game time

        if up != False or down != False or right != False or left != False :
            #die if snake's head touches its body
            for body in bodies :
                if x_player == body[0] and y_player == body[1] :
                    game_finished()
        
        if x_player < -gridSize:
            game_finished()
       #to let the game close 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGame = False

        if tail_length <= 0:
            game_finished()

        if dict_level['level1'] == True:
            level_1()
        if dict_level['level2'] == True:
            level_2()
        if dict_level['level3'] == True:
            level_3()
        if dict_level['level4'] == True:
            level_4()




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

        while (len(bodies) > tail_length):
            del bodies[0]

        #draw the body
        for body in bodies :
            pygame.draw.rect(screen, colordict['white'], (body[0], body[1], gridSize, gridSize))

        if next_level_unlocked == True:
            generate_slowpill = False
            generate_food = False
        elif next_level_unlocked == False:
            #food
            if isEaten_food == True:
                x_food, y_food = generate_food_pos()
                isEaten_food = False
                delay -= game_speed

            if generate_food == True and (x_player, y_player) == (x_food, y_food):
                isEaten_food = True
                tail_length += 1
                total_score += 1*score_multiplier

            #slowpill
            if isEaten_slowpill == True and delay < init_delay-20 - score_now:
                x_slowpill, y_slowpill = generate_slowpill_pos()
                isEaten_slowpill = False
                generate_slowpill = True
            elif isEaten_slowpill == True and delay >= 100:
                generate_slowpill = False
                
            if generate_slowpill == True and (x_player, y_player) == (x_slowpill, y_slowpill):
                isEaten_slowpill = True
                delay += game_speed*5 #set speed back to the start
                score_now = tail_length

            #ammunition
            if dict_level['level4'] == True:
                if isEaten_ammunition:         
                    x_ammunition,y_ammunition = generate_ammunition_pos()
                    isEaten_ammunition = False

                if generate_ammunition == True and (x_player, y_player) == (x_ammunition, y_ammunition):
                    isEaten_ammunition = True
                    ammunition_count += 1
                    if ammunition_count >= 3:
                        ammunition_count = 3
                #draw ammunition
                if generate_ammunition == True:
                    pygame.draw.rect(screen,colordict['green'],(x_ammunition,y_ammunition,gridSize,gridSize))

        #draw fireballs(bullets)
        fireball_image = pygame.image.load('fireball.png')
        fireball_image = pygame.transform.scale(fireball_image,(50,50))
        fireball_image.convert()
        for pos in list(bullet_pos_n_dir):
            screen.blit(fireball_image,(pos[0],pos[1]))
           
        #draw obstacle
        for obs_x,obs_y,obs_w,obs_h in zip(l_obs_x,l_obs_y,l_obs_w,l_obs_h):
            pygame.draw.rect(screen,colordict['blue'],(obs_x*gridSize,obs_y*gridSize,obs_w*gridSize,obs_h*gridSize))
        
        #draw food
        if generate_food == True:
            pygame.draw.rect(screen,colordict['yellow'], (x_food, y_food, gridSize, gridSize))

        #draw slowpill
        if generate_slowpill == True:
            pygame.draw.rect(screen,colordict['red'],(x_slowpill,y_slowpill,gridSize,gridSize))

        

        font = pygame.font.SysFont('Segoe UI Black', 25)
        textScore = font.render("Score: {}".format(total_score), True, colordict['black'])
        screen.blit(textScore, (10, 3))

        if dict_level['level4'] == True:
            #draw bullet image
            bullet_image = pygame.image.load('fireball.png')
            bullet_image = pygame.transform.scale(bullet_image,(30,30))
            bullet_image.convert()
            if ammunition_count >= 1:
                screen.blit(bullet_image,(135,6))
            if ammunition_count >= 2:
                screen.blit(bullet_image,(150,6))
            if ammunition_count == 3:
                screen.blit(bullet_image,(165,6))

        try:
            if game_time//1000 - sot_time <= 1 and print_stabbed == False:
                screen.blit(sot_text, (300, 3))
                print_sot = True
            else:
                print_sot = False
                del sot_time
        except:
            pass

        try:
            if game_time//1000 - stabbed_time <= 1 and print_sot == False:
                screen.blit(stabbed_text, (300, 3))
                print_stabbed = True
            else:
                print_stabbed = False
                del stabbed_time
        except:
            pass

        #update the screen
        pygame.display.update()
        root.update()

if __name__ == '__main__':
    initial()
