import pygame
from pygame.locals import *
import Defs
import random
import os
import sys
import math

size = width, height = (800, 700)
healthval = 0

pygame.init()
running = True
speed = 30

#GAME_FONT = pygame.freetype.Font("Comic Sans MS", 24)

screen = pygame.display.set_mode(size)  # display size
pygame.display.set_caption("Shooter boat")  # title name
# screen.fill((40, 100, 250)) #bg solid fill color - blue

pygame.display.update()

#####################
# player boat png image load
pboat_raw = pygame.image.load("assets//Boat1.png")
pboat = pygame.transform.scale(pboat_raw, (160, 200))
pboat_loc = pboat.get_rect()
pboat_loc.center = width/4, height*0.5


# healthbar
phealthb = pygame.image.load("assets//healthbar.png")
#phealth = pygame.transform.scale(pboat_raw, (160,200))
phealthb_loc = pboat.get_rect()
phealthb_loc.center = width - 128, height*0.1

# health
phealth = pygame.image.load("assets//health.png")
#phealth = pygame.transform.scale(pboat_raw, (160,200))
phealth_loc = pboat.get_rect()
phealth_loc.center = width - 129, height * 0.07

# obstacle 1
bg_s1x = 600
bg_s1y = 650
bg_obs1 = pygame.image.load("assets//obs1.png")


# water
# water background texture load
bg = pygame.image.load("assets//water_texture.png")
bgX = -256
bgX2 = bg.get_width() - 256
bgy = bg
bgY = -256
bgY2 = bgX2

# sand
# sand background texture load
bg_sand = pygame.image.load("assets//sand_texture.png")
bg_sX = 0
bg_sX2 = bg_sand.get_width()

# tree
# tree backgroung texture load
# player rock png image load
bg_trees = pygame.image.load("assets//PlaceholderCow.png")
bg_tX = 0
bg_tX2 = bg_trees.get_width()

######################
lval = 2
steerval = 0.5
edgecol = 0


def redrawWindow():
    global phealth, healthval
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512))  # arg 2 denotes up/down in screen
    screen.blit(bgy, (bgY2, 512))
    screen.blit(pboat, pboat_loc)
    phealth = pygame.transform.scale(phealth, (200 - healthval*2, 197))
    phealth_loc.center = width - 129 + healthval/2.5, height * 0.07
    screen.blit(bg_obs1, (bg_s1x, 0))
    screen.blit(bg_obs1, (bg_s1y, 0))
    screen.blit(phealthb, phealthb_loc)
    screen.blit(phealth, phealth_loc)
    screen.blit(bg_sand, (bg_sX, 650))
    screen.blit(bg_sand, (bg_sX2, 650))
    screen.blit(bg_trees, (bg_tX, 545))
    screen.blit(bg_trees, (bg_tX2, 545))
    pygame.display.update()  # updates the screen


def redrawWindowDownSteer():
    global edgecol
    global phealth, healthval
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512))  # arg 2 up/down
    screen.blit(bgy, (bgY2, 512))
    screen.blit(bg_obs1, (bg_s1x, 0))
    screen.blit(bg_obs1, (bg_s1y, 0))
    dsteer = pygame.transform.rotate(pboat, -20)
    screen.blit(dsteer, pboat_loc)
    phealth = pygame.transform.scale(phealth, (200 - healthval*2, 197))
    phealth_loc.center = width - 129 + healthval/2.5, height * 0.07
    screen.blit(phealthb, phealthb_loc)
    screen.blit(phealth, phealth_loc)
    screen.blit(bg_sand, (bg_sX, 650))
    screen.blit(bg_sand, (bg_sX2, 650))
    screen.blit(bg_trees, (bg_tX, 545))
    screen.blit(bg_trees, (bg_tX2, 545))
    edgecol = edgecol - 1
    pygame.display.update()  # updates the screen


def redrawWindowUpSteer():
    global edgecol
    global phealth, healthval
    screen.blit(bg, (bgX, 0))  # draws our first bg image
    screen.blit(bg, (bgX2, 0))  # draws the seconf bg image
    screen.blit(bgy, (bgY, 512))  # arg 2 up/down
    screen.blit(bgy, (bgY2, 512))
    screen.blit(bg_obs1, (bg_s1x, 0))
    screen.blit(bg_obs1, (bg_s1y, 0))

    dsteer = pygame.transform.rotate(pboat, 20)
    phealth = pygame.transform.scale(phealth, (200 - healthval*2, 197))
    phealth_loc.center = width - 129 + healthval/2.5, height * 0.07
    screen.blit(dsteer, pboat_loc)
    screen.blit(phealthb, phealthb_loc)
    screen.blit(phealth, phealth_loc)
    screen.blit(bg_sand, (bg_sX, 650))
    screen.blit(bg_sand, (bg_sX2, 650))
    screen.blit(bg_trees, (bg_tX, 545))
    screen.blit(bg_trees, (bg_tX2, 545))
    edgecol = edgecol + 1
    pygame.display.update()  # updates the screen


def resetBackground():
    global bg, bg_trees, bg_sand, bg_obs1, bgX, bgX2, bgY, bgY2, bg_sX, bg_sX2, bg_tX, bg_tX2, bg_s1x, bg_s1y
    # water
    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    if bgY < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgY = bg.get_width()

    if bgY2 < bg.get_width() * -1:
        bgY2 = bg.get_width()

    # sand
    if bg_sX < bg_sand.get_width() * -1:  # If our bg is at the -width then reset its position
        bg_sX = bg_sand.get_width()

    if bg_sX2 < bg_sand.get_width() * -1:
        bg_sX2 = bg_sand.get_width()

    # trees
    if bg_tX < bg_trees.get_width() * -1:  # If our bg is at the -width then reset its position
        bg_tX = bg_trees.get_width()

    if bg_tX2 < bg_trees.get_width() * -1:
        bg_tX2 = bg_trees.get_width()

    # obstalces
    if bg_s1x < bg_obs1.get_width() * -1:  # If our bg is at the -width then reset its position
        bg_s1x = bg_obs1.get_width()

    if bg_s1y < bg_obs1.get_width() * -1:
        bg_s1y = bg_obs1.get_width()


while running:

    # right scroll
    bgX -= lval  # Move both background images front #push right
    bgX2 -= lval
    bgY -= lval
    bgY2 -= lval

    bg_sX -= lval  # Move both background images front #push right
    bg_sX2 -= lval

    bg_tX -= lval  # Move both background images front #push right
    bg_tX2 -= lval

    bg_s1x -= lval  # obstacles
    bg_s1y -= lval

    resetBackground()

######################
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if steerval >= 0.89 or steerval <= 0.04:
            healthval = healthval + 4

        if healthval >= 95:
            running = False
        lval = 2
        print(healthval)
        # left scroll
        if pygame.key.get_pressed()[K_d]:
            lval = 3.5
            bgX -= lval  # Move both background images back faster #push left
            bgX2 -= lval
            bgY -= lval
            bgY2 -= lval
            bg_s1x -= lval
            bg_s1y -= lval

            resetBackground()

        # right scroll
        if pygame.key.get_pressed()[K_a]:
            lval = 0.5
            bgX -= lval  # Move both background images back slower #pushes left
            bgX2 -= lval
            bgY -= lval
            bgY2 -= lval
            bg_s1x -= lval
            bg_s1y -= lval

            resetBackground()

        # steering controls
        if pygame.key.get_pressed()[K_w]:  # steer boat upwards
            steerval -= 0.01
            print(steerval)
            pboat_loc.center = width/4, height*steerval

        if pygame.key.get_pressed()[K_s]:  # steer boat downwards
            steerval += 0.01
            print(steerval)
            pboat_loc.center = width/4, height*steerval

    normalstate = True
    if pygame.key.get_pressed()[K_s]:
        redrawWindowDownSteer()
        normalstate = False

    if pygame.key.get_pressed()[K_w]:
        redrawWindowUpSteer()
        normalstate = False

    if normalstate:
        redrawWindow()

    pygame.display.update()
