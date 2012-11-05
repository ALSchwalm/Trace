'''
Created on Nov 3, 2012

@author: Adam
'''
import render
import pygame,sys
import obj
from pygame.locals import *
from consts import *

movement = [0, 0]
tenative = set([])


def move():
    old_x = player.x
    old_y = player.y
    
    new_x = player.x + movement[0]
    new_y = player.y + movement[1]
    
    if not render.is_passable(new_x, new_y): return 0
    
    if 0 < new_x < FIELD_WIDTH:
        player.x = new_x
    if 0 < new_y < FIELD_HEIGHT:
        player.y = new_y
        
    if not render.is_edge(player.x, player.y) and player.on_edge:
        print("off edge")
        player.on_edge = False
        render.drawPoint(old_x, old_y, player.on_edge)
        
    elif render.is_edge(player.x, player.y) and not player.on_edge:
        print("on edge")
        player.on_edge = True
        render.drawPoint(player.x, player.y, False)
        
        min_area = None
        min_point = None
        for i, j in [p for p in [(1, 0), (-1, 0), (0, 1), (0, -1)]]:
            area = render.floodfill(player.x+i, player.y+j, BACKGROUND_COLOR, 0xF0F00F)
            point = (player.x+i, player.y+j)
            if area and min_area == None:
                min_area = area
                min_point = point
            elif area and area < min_area:
                min_area = area
                min_point = point
        print((player.x, player.y), min_point)
        render.floodfill(min_point[0], min_point[1], BACKGROUND_COLOR, AREA_COLOR, True)
        render.remove_line()
        
    if not player.on_edge:
        tenative.add((player.x, player.y))
    render.drawPoint(player.x, player.y, player.on_edge) #edge should not be passed


def input(events):

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.key == K_LEFT:
                movement[0] -= 1
            elif event.key == K_UP:
                movement[1] -= 1
            elif event.key == K_RIGHT:
                movement[0] += 1
            elif event.key == K_DOWN:
                movement[1] += 1
        elif event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                movement[0] += 1
            elif event.key == K_UP:
                movement[1] += 1
            elif event.key == K_RIGHT:
                movement[0] -= 1
            elif event.key == K_DOWN:
                movement[1] -= 1

def setup():
    global player
    
    player = obj.Player(1, 1, 1)
        
    render.setup()
    #render.updateArray()
    
def run():
    while True:
        move()
        input(pygame.event.get())
        render.draw()
        