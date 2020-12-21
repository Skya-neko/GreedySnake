# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 14:58:37 2020

@author: Vivian
"""



import pygame
import time
import random
 
pygame.init()
pygame.mixer.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
body = (14, 242, 170)
color_light = (170,170,170)
color_dark = (100,100,100) # dark shade of the button  
game_start = 3


dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

star = pygame.image.load("./img/star.png")
star.convert()

snakeHead = pygame.image.load("./img/snake-head.png")
snakeHead.convert()
 
clock = pygame.time.Clock()
 
snake_block = 20
snake_speed = 10
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


#遊戲歡迎畫面
def welcomePage():
    text = score_font.render('start' , True , white)  

    Button1_w = 140
    Button1_h = 55
    # Button1_w_c = (dis_width - Button1_w)/2
    # Button1_h_c = (dis_height - Button1_h)/2
    Button1_w_c = (dis_width - Button1_w)*3/4
    Button1_h_c = (dis_height - Button1_h)*3/4
    
      
    
    
    running = True
    while running:  
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():  
            
            #用叉叉關掉視窗的寫法
            if ev.type == pygame.QUIT:    
                pygame.quit()  
                  
            # 滑鼠點擊button，就關閉
            if ev.type == pygame.MOUSEBUTTONDOWN:  
                if Button1_w_c <= mouse[0] <= Button1_w_c + Button1_w and Button1_h_c <= mouse[1] <= Button1_h_c + Button1_h:  
                    # pygame.quit()  
                    running = False
                    
        #背景填滿            
        # dis.fill(white)  
        bg = pygame.image.load("./img/snake_smaller.png")
        dis.blit(bg, bg.get_rect())

          
        # 如果滑鼠在按鈕上，則會呈現較亮的顏色 
        if Button1_w_c <= mouse[0] <= Button1_w_c + Button1_w and Button1_h_c <= mouse[1] <= Button1_h_c + Button1_h:  
            pygame.draw.rect(dis,color_light,[Button1_w_c, Button1_h_c, Button1_w, Button1_h])  
              
        else:  
            pygame.draw.rect(dis,color_dark,[Button1_w_c, Button1_h_c, Button1_w, Button1_h])  
          
        # superimposing the text onto our button  
        dis.blit(text ,(Button1_w_c + 29, Button1_h_c)) 
          
        # updates the frames of the game  
        pygame.display.update()


def countDownPage(t):
    Button1_w = 140
    Button1_h = 55
    Button1_w_c = (dis_width - Button1_w)/2
    Button1_h_c = (dis_height - Button1_h)/2
    
    # running = True
    # while running:  
    if t > 0:
        for ev in pygame.event.get():  
            
            #用叉叉關掉視窗的寫法
            if ev.type == pygame.QUIT:    
                pygame.quit()  
                
        dis.fill(white)
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs)
        text = score_font.render(timer , True , black)
        dis.blit(text ,(Button1_w_c + 29, Button1_h_c))
        pygame.display.update()
        time.sleep(1) 
        t -= 1
        countDownPage(t)





def our_snake(snake_list, i, eated):
    angle = 90 * i
    rotated_image = pygame.transform.rotate(snakeHead, angle)
    dis.blit(rotated_image, (snake_list[-1][0], snake_list[-1][1]))


    idx = 0
    for x in snake_list[:-1]:
        if x in eated:
            pygame.draw.rect(dis, yellow, [x[0], x[1], snake_block, snake_block])
            if idx == 0:
                del eated[0]
        else:
            color1 = 180 + idx * 10
            if color1 >= 255:
                color1 = 255
            pygame.draw.rect(dis, (body[0], color1, body[2]), [x[0], x[1], snake_block, snake_block])
        idx = idx + 1
    return eated

 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# Get the coordinate of food
def getCoordinate(dis):
    print('得到座標', round(random.randrange(0, dis - snake_block) / snake_block) * snake_block)
    return round(random.randrange(0, dis - snake_block) / snake_block) * snake_block


def getNewFoodPos(snake_List):
    food = [getCoordinate(dis_width), getCoordinate(dis_height)]
    print('getNew', food)
    if food in snake_List:
        return getNewFoodPos(snake_List)
    return food


def gameLoop():
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
    iRotate = 0
    eated = []
    snake_List = []
    Length_of_snake = 1
 
    foodx = getCoordinate(dis_width)
    foody = getCoordinate(dis_height)
 
    while not game_over:
 
        while game_close == True:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
 
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    iRotate = 1
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    iRotate = 3
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    iRotate = 0
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    iRotate = 2
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
            pygame.mixer.music.load("./sound/crash.mp3")
            pygame.mixer.music.play(1)

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        dis.blit(star,(foodx, foody))
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                pygame.mixer.music.load("./sound/crash.mp3")
                pygame.mixer.music.play(1)
                game_close = True

        eated = our_snake(snake_List, iRotate, eated)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.music.load("./sound/eat.mp3")
            pygame.mixer.music.play(1)
            eated.append([foodx, foody])
            food = getNewFoodPos(snake_List)
            foodx = food[0]
            foody = food[1]
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 

welcomePage()
countDownPage(game_start)
gameLoop()