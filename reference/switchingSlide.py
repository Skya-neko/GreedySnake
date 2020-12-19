# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 18:21:10 2020

source code from: https://stackoverflow.com/questions/35242123/how-can-i-switch-between-slides-in-pygame
"""

import pygame

# === constants ===

SIZE = (800, 600)

WHITE = (255,255,255)

# === functions ===

def display_slide(screen, filename):

    # --- read slide ---

    image = pygame.image.load(filename)

    # --- display ---

    #screen.fill(WHITE)
    screen.blit(image, (0,0))
    pygame.display.flip()

    # --- get keypress ---

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                        running = False

# === main ===

# --- init ---

pygame.init()
screen = pygame.display.set_mode(SIZE)

# --- slides ---

display_slide(screen, 'test1.jpg')
display_slide(screen, 'test2.jpg')

# --- the end ---

pygame.quit()