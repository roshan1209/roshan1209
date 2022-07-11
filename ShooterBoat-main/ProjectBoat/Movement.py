import pygame
from pygame.locals import *
import random
import os
import sys
import math

size = width, height = (800, 700)

pygame.init()
running = True
speed = 30

screen = pygame.display.set_mode(size)  #display size
pygame.display.set_caption("Shooter boat")  #title name
screen.fill((40, 100, 250)) #bg solid fill color - blue

pygame.display.update()

pboat_raw = pygame.image.load("Boat1.png")      #player boat png image load
pboat = pygame.transform.scale(pboat_raw, (160,200))
pboat_loc = pboat.get_rect()
pboat_loc.center = width/2 , height*0.5

bg = pygame.image.load("water_texture.png")     #background texture load
bgX = -256
bgX2 = bg.get_width() - 256

bgy = bg
bgY = -256
bgY2 = bgX2

lval=2

def redrawWindow():
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512)) # arg 2 up/down
    screen.blit(bgy, (bgY2, 512))
    screen.blit(pboat, pboat_loc)
    pygame.display.update()  # updates the screen


while running:         

    #right scroll
    bgX -= lval  # Move both background images front #push right
    bgX2 -= lval
    bgY -= lval
    bgY2 -= lval
    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    if bgY < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgY = bg.get_width()

    if bgY2 < bg.get_width() * -1:
        bgY2 = bg.get_width()


    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        lval=2
        #left scroll
        if pygame.key.get_pressed()[K_d]:
            lval = 3.5
            bgX -= lval  # Move both background images back #push left
            bgX2 -= lval
            bgY -= lval
            bgY2 -= lval
            if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
                bgX = bg.get_width()
    
            if bgX2 < bg.get_width() * -1:
                bgX2 = bg.get_width()

            if bgY < bg.get_width() * -1:  # If our bg is at the -width then reset its position
                bgY = bg.get_width()
    
            if bgY2 < bg.get_width() * -1:
                bgY2 = bg.get_width()

        
        #right scroll
        if pygame.key.get_pressed()[K_a]:
            lval = 0.5
            bgX -= lval  # Move both background images front #push right
            bgX2 -= lval
            bgY -= lval
            bgY2 -= lval
            
            if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
                bgX = bg.get_width()
    
            if bgX2 < bg.get_width() * -1:
                bgX2 = bg.get_width()

            if bgY < bg.get_width() * -1:  # If our bg is at the -width then reset its position
                bgY = bg.get_width()
    
            if bgY2 < bg.get_width() * -1:
                bgY2 = bg.get_width()
            
           

    redrawWindow()
    pygame.display.update()