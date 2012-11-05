'''
Created on Nov 3, 2012

@author: Adam
'''
import pygame
import core
from consts import *

array = None

def remove_line():
    for x in range(len(array)):
        for y in range(len(array[0])):
            if array[x, y] == LINE_COLOR:
                array[x, y] = BACKGROUND_COLOR

def nearby(x, y):
    l = []
    for i in range(-1, 1):
        for j in range(-1, 1):
            print(x+i, y+j)
            l.append(array[x+i, y+j])
    return l


def floodfill(x, y, target_color, new_color, apply=False):
    global array
    temp_array = pygame.PixelArray(array.make_surface())
    if temp_array[x, y] == LINE_COLOR or temp_array[x, y] == AREA_COLOR:
        return None
    
    q = [(x, y)]
    area = 0
    for n in q:
        area += 1
        w = n
        e = n
        while temp_array[w] == target_color:
            w = (w[0]-1, w[1])
        while temp_array[e] == target_color:
            e = (e[0]+1, e[1])
        temp_array[w[0]:e[0], n[1]] = new_color

        for i in range(w[0], e[0]):
            if temp_array[i, n[1]+1] == target_color:
                q.append((i, n[1]+1))
            elif temp_array[i, n[1]-1] == target_color:
                q.append((i, n[1]-1))
                    
                    
    if apply:
        array = temp_array
    return area

def is_passable(x, y):
    try:
        if array[x, y] == AREA_COLOR or array[x, y] == LINE_COLOR:
            return False
    except Exception:
        return False
    else:
        return True

def is_edge(x, y):
    for i, j in [p for p in [(1, 0), (-1, 0), (0, 1), (0, -1)]]: #use nearby?
        if array[x+i, y+j] == AREA_COLOR:
            return True
    return False

def drawPoint(x, y, edge):
    if not edge:
        array[x, y] = LINE_COLOR


def draw():
    global Surface
    global clock
    
    rect = pygame.Rect((0, 0), (FIELD_WIDTH, FIELD_HEIGHT))
    Surface.fill(BACKGROUND_COLOR, rect)
    
    Surface.blit(array.make_surface(), (0, 0))
    
    rect = pygame.Rect((core.player.x, core.player.y), (PLAYER_SIZE, PLAYER_SIZE))
    Surface.fill(PLAYER_COLOR, rect)

    pygame.display.flip()
    clock.tick(MAX_FPS)


def setup():
    global Surface
    global clock
    global array
    
    pygame.init()
    
    Surface = pygame.display.set_mode((FIELD_WIDTH,FIELD_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    covered_area = pygame.Surface((FIELD_WIDTH,FIELD_HEIGHT))
    array = pygame.PixelArray(covered_area)
    for row in array:
        row[0] = AREA_COLOR
        row[-1] = AREA_COLOR
        
    array[0,:] = AREA_COLOR
    array[-1,:] = AREA_COLOR
    
    pygame.display.set_caption('Trace v0.2')