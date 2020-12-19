# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 17:20:15 2020

source code from: https://www.geeksforgeeks.org/creating-start-menu-in-pygame/
"""

import pygame  
import sys  
  
  
# initializing the constructor  
pygame.init()  
  
# screen resolution  

dis_width = 600
dis_height = 400
res = (dis_width,dis_height)  
# opens up a window  
screen = pygame.display.set_mode(res)  
  
# white color  
color = (255,255,255)  
  
# light shade of the button  
color_light = (170,170,170)  
  
# dark shade of the button  
color_dark = (100,100,100)  
  
# stores the width of the  
# screen into a variable  
# width = screen.get_width()  
  
# stores the height of the  
# screen into a variable  
# height = screen.get_height()  
  
# defining a font  
smallfont = pygame.font.SysFont('Corbel',35)  
  
# rendering a text written in  
# this font  
text = smallfont.render('quit' , True , color)  

Button1_w = 140
Button1_h = 40
Button1_w_c = (dis_width - Button1_w)/2
Button1_h_c = (dis_height - Button1_h)/2

  
while True:  
     
    for ev in pygame.event.get():  
          
        if ev.type == pygame.QUIT:    #用叉叉關掉視窗的寫法
            pygame.quit()  
              
        #checks if a mouse is clicked  
        # if ev.type == pygame.MOUSEBUTTONDOWN:  
              
        #     #if the mouse is clicked on the  
        #     # button the game is terminated  
        #     if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
        #         pygame.quit()  
                  
    # fills the screen with a color  
    screen.fill((60,25,60))  
      
    # stores the (x,y) coordinates into  
    # the variable as a tuple  
    mouse = pygame.mouse.get_pos()  
      
    # if mouse is hovered on a button it  
    # changes to lighter shade  
    if Button1_w_c <= mouse[0] <= Button1_w_c + Button1_w and Button1_h_c <= mouse[1] <= Button1_h_c + Button1_h:  
        pygame.draw.rect(screen,color_light,[Button1_w_c, Button1_h_c, Button1_w, Button1_h])  
          
    else:  
        pygame.draw.rect(screen,color_dark,[Button1_w_c, Button1_h_c, Button1_w, Button1_h])  
      
    # superimposing the text onto our button  
    screen.blit(text ,(Button1_w_c + 41, Button1_h_c))  
      
    # updates the frames of the game  
    pygame.display.update()