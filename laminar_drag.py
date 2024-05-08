"""

This program simulates the movement of an object in a fluid where it is moving 
relatively slowly, so that the Reynolds number is low, and the drag force is
proportional to the object's velocity.

Like friction, drag force is always opposite to an object's direction of 
motion. Therefore this simulation, where drag is the only force considered, is 
effectively one-dimensional. The fact that drag is proportional to the velocity 
also means it can't change the direction of motion, and so we can treat the 
velocity as a positive quantity (assuming it's not zero, in which case the object is stationary).

If k is the constant of proportionality for the drag, then the equation of 
motion in this scenario is

  (d^2 s)/(d t^2) = -k ds/dt.

If we set up our coordinates so that s is never zero, we can rearrange the 
equation as

  [(d^2 s)/(d t^2)]/(ds/dt) = -k.

Integrating both sides gives us a solution:

  ln |ds/dt| = -kt + C,

where C is a constant. This can be rearranged as

  ds/dt = sgn(ds/dt) e^C e^(-kt).

Since we are regarding the velocity as always positive we can ignore the sign 
factor, and set A = e^C, giving

  ds/dt = Ae^(-kt).

Setting t = 0 gives ds/dt = A, so A is the initial velocity u.

If k = 0, the velocity is constant at u, so we have the constant velocity 
situation. Otherwise, integrating both sides gives

  s = B - u/k e^(-kt).

Setting t = 0 gives us r = B - u/k. Hence we can write B = r + u/k, giving us 
the equation

  s = r + u/k (1 - e^(-kt)).
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
DRAG = -0.00075

def get_pos(t: int) -> Vec:
    if not INITIAL_VEL:
        return INITIAL_POS

    if not DRAG:
        return INITIAL_POS + INITIAL_VEL * t

    return INITIAL_POS + ((1 - math.exp(-DRAG * t)) / DRAG) * INITIAL_VEL

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