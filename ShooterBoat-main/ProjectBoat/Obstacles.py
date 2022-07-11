import pygame
from pygame.locals import *
import Defs
import random
import os
import sys
import math

size = width, height = (1000, 700)

pygame.init()
running = True
speed = 30

screen = pygame.display.set_mode(size)  #display size
pygame.display.set_caption("Shooter boat")  #title name
pygame.display.set_icon(pygame.image.load("Boat1.png"))
#screen.fill((40, 100, 250)) #bg solid fill color - blue

pygame.display.update()

pboat_raw = pygame.image.load("Boat1.png")      #player boat png image load
pboat = pygame.transform.scale(pboat_raw, (160,200))
pboat_loc = pboat.get_rect()
pboat_loc.center = width/4 , height*0.5
pboat_loc.bottomright = width/4 , height*0.1

##################### water
bg = pygame.image.load("water_texture.png")     #water background texture load
bgX = -256
bgX2 = bg.get_width() - 256

bgy = bg
bgY = -256
bgY2 = bgX2

###################### sand
bg_sand = pygame.image.load("sand_texture.png")     #sand background texture load
bg_sX = 0
bg_sX2 = bg_sand.get_width()

######################
bg_trees = pygame.image.load("PlaceholderCow.png")        #tree backgroung texture load
bg_tX = 0
bg_tX2 = bg_trees.get_width()

######################
lval=2
steerval=0.5



while running:         

    #right scroll
    bgX -= lval  # Move both background images front #push right
    bgX2 -= lval
    bgY -= lval
    bgY2 -= lval
    
    bg_sX -= lval  # Move both background images front #push right
    bg_sX2 -= lval

    bg_tX -= lval  # Move both background images front #push right
    bg_tX2 -= lval

    Defs.resetBackground()

######################
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        lval=2

        

        #left scroll
        if pygame.key.get_pressed()[K_d]:
            lval = 3.5
            bgX -= lval  # Move both background images back faster #push left
            bgX2 -= lval
            bgY -= lval
            bgY2 -= lval

            Defs.resetBackground()

        #right scroll
        if pygame.key.get_pressed()[K_a]:
            lval = 0.5
            bgX -= lval  # Move both background images back slower #pushes left
            bgX2 -= lval
            bgY -= lval
            bgY2 -= lval
            
            Defs.resetBackground()

        #steering controls
        if pygame.key.get_pressed()[K_w]: #steer boat upwards
            steerval -= 0.01
            pboat_loc.center = width/4 , height*steerval

        if pygame.key.get_pressed()[K_s]: #steer boat downwards
            steerval += 0.01
            pboat_loc.center = width/4 , height*steerval
    


    normalstate = True
    if pygame.key.get_pressed()[K_s]:
        Defs.redrawWindowDownSteer()
        normalstate = False

    if pygame.key.get_pressed()[K_w]:
        Defs.redrawWindowUpSteer()
        normalstate = False
    
    if normalstate:
        Defs.redrawWindow()

    
    pygame.display.update()
