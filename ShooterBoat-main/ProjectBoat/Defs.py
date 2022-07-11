import pygame
from pygame.locals import *
import random
import os
import sys
import math

size = width, height = (800, 700)

running = True
speed = 30

#GAME_FONT = pygame.freetype.Font("Comic Sans MS", 24)

screen = pygame.display.set_mode(size)  #display size
pygame.display.set_caption("Shooter boat")  #title name

pboat_raw = pygame.image.load("assets//Boat1.png")      #player boat png image load
pboat = pygame.transform.scale(pboat_raw, (160,200))
pboat_loc = pboat.get_rect()
pboat_loc.center = width/4 , height*0.5

##################### water
bg = pygame.image.load("assets//water_texture.png")     #water background texture load
bgX = -256
bgX2 = bg.get_width() - 256

bgy = bg
bgY = -256
bgY2 = bgX2

###################### sand
bg_sand = pygame.image.load("assets//sand_texture.png")     #sand background texture load
bg_sX = 0
bg_sX2 = bg_sand.get_width()

######################
bg_trees = pygame.image.load("assets//PlaceholderCow.png")        #tree backgroung texture load
bg_tX = 0
bg_tX2 = bg_trees.get_width()

######################
lval=2
steerval=0.5


def endGame():
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512)) # arg 2 denotes up/down in screen
    screen.blit(bgy, (bgY2, 512))
    screen.blit(pboat, pboat_loc)
    screen.blit(bg_sand, (bg_sX, 650))
    screen.blit(bg_sand, (bg_sX2, 650))
    screen.blit(bg_trees, (bg_tX, 545))
    screen.blit(bg_trees, (bg_tX2, 545))
    pygame.display.update()  # updates the screen


def redrawWindow():
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512)) # arg 2 denotes up/down in screen
    screen.blit(bgy, (bgY2, 512))
    screen.blit(pboat, pboat_loc)
    screen.blit(bg_sand, (bg_sX, 650))
    screen.blit(bg_sand, (bg_sX2, 650))
    screen.blit(bg_trees, (bg_tX, 545))
    screen.blit(bg_trees, (bg_tX2, 545))
    pygame.display.update()  # updates the screen

def redrawWindowDownSteer():
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512)) # arg 2 up/down
    screen.blit(bgy, (bgY2, 512))
    dsteer = pygame.transform.rotate(pboat, -20)
    screen.blit(dsteer, pboat_loc)
    screen.blit(bg_sand, (bg_sX, 650))
    screen.blit(bg_sand, (bg_sX2, 650))
    screen.blit(bg_trees, (bg_tX, 545))
    screen.blit(bg_trees, (bg_tX2, 545))
    pygame.display.update()  # updates the screen

def redrawWindowUpSteer():
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512)) # arg 2 up/down
    screen.blit(bgy, (bgY2, 512))
    dsteer = pygame.transform.rotate(pboat, 20)
    screen.blit(dsteer, pboat_loc)
    screen.blit(bg_sand, (bg_sX, 650))
    screen.blit(bg_sand, (bg_sX2, 650))
    screen.blit(bg_trees, (bg_tX, 545))
    screen.blit(bg_trees, (bg_tX2, 545))
    pygame.display.update()  # updates the screen

def resetBackground():
    global bg, bg_trees, bg_sand, bgX, bgX2, bgY, bgY2, bg_sX, bg_sX2, bg_tX, bg_tX2
    ##################### water
    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    if bgY < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgY = bg.get_width()

    if bgY2 < bg.get_width() * -1:
        bgY2 = bg.get_width()

    #################### sand
    if bg_sX < bg_sand.get_width() * -1:  # If our bg is at the -width then reset its position
        bg_sX = bg_sand.get_width()

    if bg_sX2 < bg_sand.get_width() * -1:
        bg_sX2 = bg_sand.get_width()

    ####################### trees
    if bg_tX < bg_trees.get_width() * -1:  # If our bg is at the -width then reset its position
        bg_tX = bg_trees.get_width()

    if bg_tX2 < bg_trees.get_width() * -1:
        bg_tX2 = bg_trees.get_width()
