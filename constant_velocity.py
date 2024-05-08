import sys
import pygame as pg
from pygame import Vector2 as Vec

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

INITIAL_POS = Vec(0, 0)
VEL = Vec(SCREEN_WIDTH, SCREEN_HEIGHT).normalize()

def get_pos(t: int) -> Vec:
    return INITIAL_POS + t * VEL

def screen_pos(pos: Vec) -> tuple[int, int]:
    return (round(pos.x) % SCREEN_WIDTH, round(pos.y) % SCREEN_HEIGHT)

def screen() -> pg.Surface:
    return pg.display.get_surface()

initial_ticks = None

def get_time() -> int:
    global initial_ticks

    if initial_ticks is None:
        initial_ticks = pg.time.get_ticks()
        return initial_ticks
    
    return pg.time.get_ticks() - initial_ticks

pg.init()
pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    screen().fill('black')
    pos = get_pos(get_time())
    pg.draw.circle(screen(), 'white', screen_pos(pos), 50)
    pg.display.flip()

