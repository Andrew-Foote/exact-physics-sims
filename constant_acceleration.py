import sys
import pygame as pg
from pygame import Vector2 as Vec

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

INITIAL_POS = Vec(0, SCREEN_HEIGHT / 2)
INITIAL_VEL = Vec(0.5, -0.5)
ACC = Vec(0, 0.001)

def get_pos(t: int) -> Vec:
    return INITIAL_POS + t * (INITIAL_VEL + (t / 2) * ACC)

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