import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 800))
done = False
x = 50
y = 50
# clock = pygame.time.Clock()
# pygame.mixer.music.load('宮  01 崖の上のポニョ（崖の上のポニョ）.mp3')
# pygame.mixer.music.play(0)
# pygame.mixer.music.queue('宮  02 さんぽ（となりのトトロ）.mp3')    
# pygame.mixer.music.set_volume(0.5)

up, down, left ,right = False, False, False, False
while not done:
    pygame.time.delay(140)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # gray = (128,128,128)
        red = (255,0,0)
        color = red
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #     color = gray
        pressed = pygame.key.get_pressed()
        
        
        
        if pressed[pygame.K_UP] and down != True :
            up = True
            down = left = right = False
        if pressed[pygame.K_DOWN] and up != True :
            down = True
            up = left = right = False
        if pressed[pygame.K_LEFT] and right != True :
            left = True
            up = right = down = False
        if pressed[pygame.K_RIGHT] and left != True :
            right = True
            up = left = down = False
        if up == True: y-=10
        if down == True: y+=10
        if left == True: x-=10
        if right == True: x+=10

        
        # if pressed[pygame.K_k]: pygame.mixer.music.pause()
        # if pressed[pygame.K_LALT] and pressed[pygame.K_k]: pygame.mixer.music.unpause()
        # volume = pygame.mixer.music.get_volume()
        # if pressed[pygame.K_LALT] and pressed[pygame.K_UP]: pygame.mixer.music.set_volume(volume+0.1)
        # if pressed[pygame.K_LALT] and pressed[pygame.K_DOWN]: pygame.mixer.music.set_volume(volume-0.1)

        # musictime = pygame.mixer.music.get_pos()

        # if pressed[pygame.K_LALT] and pressed[pygame.K_LEFT]: pygame.mixer.music.set_pos(-10)
        # if pressed[pygame.K_LALT] and pressed[pygame.K_RIGHT]: pygame.mixer.music.set_pos(10)

        screen.fill((0, 0, 0))

        # font = pygame.font.SysFont("Calibri", 22)
        # text = font.render('time: %ss'%str(musictime//1000), True, (0, 128, 0))

        # screen.blit(text,(10, 10))

        pygame.draw.rect(screen, color, (x, y, 60, 60), 1)
        pygame.display.update()
        # clock.tick(60)