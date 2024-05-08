"""

This program simulates the movement of an object along a surface where the only 
force to be considered is a force of friction, of constant magnitude, acting
opposite to the movement. This is apparently a reasonable model of friction for 
solid objects sliding over a surface, although it is an approximation of a very 
messy reality.

The force of friction disappears once the object's velocity is zero; indeed, in 
this case the object has no direction, so it would not be meaningful to talk 
about a force opposite to it. This is interesting as it means that in this 
model, the force is a *discontinuous* function of time. It will "jump" to
zero whenever the velocity is zero.

One can write the equation of motion as something like

  (d^2 s)/(d t^2) = { 0                   if ds/dt = 0,
                    { -a/|ds/dt| (ds/dt)  otherwise,

but this does not really help with finding an exact solution. It's better to think of each case in the above equation as a separate equation of motion, solve them separately, and then figure out how they interact.

Intuitively, we can divide the object's motion into two phases. First it will move with constant acceleration, in a direction opposite to its initial velocity. Then, once the velocity reaches 0, it will stop and remain stationary. I'm not quite sure how to justify this in a fully mathematically rigorous way, but it's obvious from intuition.

Note an edge case: the first phase will not occur if the object's initial velocity is already 0. In that case we only get the second phase, where the object is stationary.

We can calculate the duration of the first phase by observing that since acceleration in the first phase is constant at -a/|u| u, we have v = u - at/|u| u = (1 - at/|u|) u. Substituting v = 0 in this equation gives the scalar equation

  1 = at/|u|,

given that u != 0. This equation has no solution if a = 0. Otherwise, we can solve for t:

  t = |u|/a.

The solution t must be nonzero, and it is positive iff |u|/a > 0, i.e. a > 0. So if a <= 0, then the first phase never finishes, and we can simply use the constant acceleration equation

  s = r + t(u - at/2|u| u) = r + t(1 - at/2|u|) u.

If, on the other hand, a > 0, then the first phase does end. Afterwards, the object will be stationary; we just need to know what its position will be. Substituting t = |u|/a into the above equation gives

  r + |u|/a (1 - a(|u|/a)/2|u|) u,

which simplifies to

  r + |u|/2a u.

This can also be expressed as r + T/2 u where T is the stopping time.
"""

import sys
import pygame as pg
from pygame import Vector2 as Vec

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

INITIAL_POS = Vec(0, 0)
INITIAL_VEL = Vec(SCREEN_WIDTH, SCREEN_HEIGHT).normalize()
INITIAL_VEL_MAG = INITIAL_VEL.length()
FRICTION = 0.00075

STOPPING_TIME = None if FRICTION <= 0 else INITIAL_VEL.length() / FRICTION

def get_pos(t: int) -> Vec:
    if not INITIAL_VEL:
        return INITIAL_POS
    
    if STOPPING_TIME is None or t <= STOPPING_TIME:
        return (
            INITIAL_POS
            + t * (1 - FRICTION * t / (2 * INITIAL_VEL_MAG)) * INITIAL_VEL
        )

    return INITIAL_POS + INITIAL_VEL * STOPPING_TIME / 2

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