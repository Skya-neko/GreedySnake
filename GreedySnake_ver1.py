import pygame
import time
import random
 
pygame.init()
 
#標記顏色
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
color_light = (170,170,170)
color_dark = (100,100,100) # dark shade of the button 

#標記視窗大小
dis_width = 600
dis_height = 400
 
#創建screen
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
game_time = 3

#物體移動的速度(??????
clock = pygame.time.Clock()
 
#蛇的寬度與速度
snake_block = 10
snake_speed = 15
 
#標記字體
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

#welcomePage parameter



#倒數計時開始遊戲
def countdown(t): 
    if t > 0: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\n") 
        time.sleep(1) 
        t -= 1
        countdown(t)

#遊戲歡迎畫面
def welcomePage():
    text = score_font.render('start' , True , white)  

    Button1_w = 140
    Button1_h = 55
    Button1_w_c = (dis_width - Button1_w)/2
    Button1_h_c = (dis_height - Button1_h)/2
    
      
    
    
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
        dis.fill(white)  
  
        #得到(x,y)的滑鼠位置
        mouse = pygame.mouse.get_pos()  
          
        # 如果滑鼠在按鈕上，則會呈現較亮的顏色 
        if Button1_w_c <= mouse[0] <= Button1_w_c + Button1_w and Button1_h_c <= mouse[1] <= Button1_h_c + Button1_h:  
            pygame.draw.rect(dis,color_light,[Button1_w_c, Button1_h_c, Button1_w, Button1_h])  
              
        else:  
            pygame.draw.rect(dis,color_dark,[Button1_w_c, Button1_h_c, Button1_w, Button1_h])  
          
        # superimposing the text onto our button  
        dis.blit(text ,(Button1_w_c + 29, Button1_h_c)) 
          
        # updates the frames of the game  
        pygame.display.update()





 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

 
def gameLoop():
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    
    while not game_over:
 
        while game_close == True:
            dis.fill(blue)
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
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        # print(snake_List)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        print(snake_List)
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
 
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
    print("haha")
    pygame.quit()
    quit()

welcomePage()
countdown(game_time)
gameLoop()



# updateTimes = n
# def updateTimes(n):
#     if n >