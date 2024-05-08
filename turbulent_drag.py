"""

This program simulates the movement of an object in a fluid where it is moving 
relatively quickly, so that the Reynolds number is high, and the drag force is
proportional to the square of the object's velocity.

Like friction, drag force is always opposite to an object's direction of 
motion. Therefore this simulation, where drag is the only force considered, is 
effectively one-dimensional. The fact that drag is proportional to the velocity 
also means it can't change the direction of motion, and so we can treat the 
velocity as a positive quantity (assuming it's not zero, in which case the object is stationary).

If k is the constant of proportionality for the drag, then the equation of motion in this scenario is

  dv/dt = -kv^2.

We can separate the variables to get

  dv/v^2 = -k dt.

Integrating both sides gives

  -1/v = C - kt,

where C is a constant. This can be rearranged as

  v = 1/(kt - C).

Substituting t = 0, we see that u = -1/C and hence C = -1/u, so we can rewrite the equation as

  v = 1/(kt + 1/u).

If k = 0, the velocity is constant at u, giving us the constant velocity situation. Otherwise, we can write the RHS as 1/k k/(kt + 1/u), allowing us to integrate both sides to get

  s = 1/k ln |kt + 1/u| + C.

Substituting t = 0, we see that r = 1/k ln |1/u| + C and hence C = r - 1/k ln |1/u|. Hence

  s = r + 1/k ln |kt + 1/u| - 1/k ln |1/u|
    = r + 1/k ln |kt + 1/u|/|1/u|
    = r + 1/k ln |kut + 1|.
"""

import math
import sys
import pygame as pg
from pygame import Vector2 as Vec

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

INITIAL_POS = Vec(0, 0)
INITIAL_VEL = Vec(SCREEN_WIDTH, SCREEN_HEIGHT).normalize()
INITIAL_VEL_MAG = INITIAL_VEL.length()
DRAG = 0.0075

def get_pos(t: int) -> Vec:
    if not DRAG:
        return INITIAL_POS + INITIAL_VEL * t

    distance = 1 / DRAG * math.log(abs(DRAG * INITIAL_VEL_MAG * t + 1))
    return INITIAL_POS + distance * INITIAL_VEL.normalize()
    
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