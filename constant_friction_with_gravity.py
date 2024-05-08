"""
This program simulates the movement of an object along a surface where the only 
forces to be considered are:
  a) a constant force of gravity which makes the object continuously accelerate.
  b) a force of friction, of constant magnitude, acting
   opposite to the movement.

An example of a situation where this model apply is if something is sliding 
down a tube---gravity produces a constant force moving the object downwards, and
while the object is moving it is subject to friction.

In order for the object to stop moving in this situation, the object has to be 
moving in the same direction as the gravity and the friction's magnitude has to
exceed the gravity's magnitude. Otherwise, the object never stops moving for 
any period of time---even if its velocity momentarily reaches zero, it will 
continue to change due to the gravity. Although you could say that the friction 
is zero at such moments, since the set of such moments is of measure zero it 
has no effect---the velocity, the integral of the acceleration, is the same 
regardless of what acceleration you choose to regard the object as having at 
those moments.

I'll consider only the one-dimensional case for now. This is especially 
nice because we don't have to worry about the possibility of the velocity 
changing direction continuously. Let f be the magnitude of friction and let g 
be the gravity.

If the velocity at some time t0 is 0, then the object is subject to gravity only
at that moment. If the gravity is 0, this means the object remains stationary.
But if gravity is nonzero, it will accelerate the object. However, as soon as
the object starts accelerating, friction comes into play and alters the 
acceleration. If the acceleration is set back to 0 or a value in the opposite
direction of the gravity, then the gravity is "cancelled" out, and the object 
just remains stationary. So the object remains stationary iff

  f >= |g|.

Otherwise, we have f < |g|. After time t0, the velocity will be in the same 
direction as the gravity, and the friction will accordingly be opposite. But 
since the friction is less in magnitude than the gravity, the object can't 
change direction from now on. So the equation of motion is simply

  s = r + (g - sgn(g) f)(t - t0)^2/2                                   (1)
 
similar to the constant-acceleration case.

This all holds if the velocity at time t0 is 0. Now we need to account for the 
possibility of a nonzero initial velocity. In this case the friction will be in
the opposite direction as the velocity, and this gets added to the gravity,
which may be in the same direction as the velocity, or opposite, or zero. 
Whatever the case, the equations

  v = u + (g - sgn(u) f)(t - t0),
  s = r + u(t - t0) + (g - sgn(u) f)(t - t0)^2/2

apply until the velocity goes to zero (if it ever does). Setting v = 0, we get
the equation

  u + (g - sgn(u) f)(t - t0) = 0.

Equivalently, (g - sgn(u) f)(t - t0) = 0. Now if g = sgn(u) f, then the only 
solution is u = 0, so the velocity only goes to zero if it's already zero at
the start (which case we already dealt with). So we can assume g and sgn(u) f
are distinct, and then the solution is

  t - t0 = -u/(g - sgn(u) f).

This time will be non-negative only if 0 <= -u/(g - sgn(u) f), i.e. u and g - sgn(u) f have opposite signs. If they have the same signs, the object never changes direction. The corresponding position at this time will be

  r - u^2/(g - sgn(u) f) + u^2 / 2(g - sgn(u) f)
  = r - u^2/2(g - sgn(u) f)
"""

import math
import sys
import pygame as pg
from pygame import Vector2 as Vec

def sign(x: float) -> int:
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

INITIAL_POS = SCREEN_HEIGHT - 50
INITIAL_VEL = -1.5
INITIAL_VEL_SIGN = sign(INITIAL_VEL)
GRAVITY = 0.001
FRICTION_MAG = 0.0005
INITIAL_FRICTION = INITIAL_VEL_SIGN * FRICTION_MAG

if GRAVITY == INITIAL_FRICTION:
    transition_time = math.inf
else:
    transition_time = -INITIAL_VEL / (GRAVITY - INITIAL_FRICTION)

if transition_time < 0:
    transition_time = math.inf

if GRAVITY == INITIAL_FRICTION:
    transition_pos = None
else:
    transition_pos = INITIAL_POS - INITIAL_VEL ** 2 / (2 * (GRAVITY - INITIAL_FRICTION))

def get_pos(t: int) -> Vec:
    if INITIAL_VEL == 0:
        if FRICTION_MAG >= abs(GRAVITY):
            s = INITIAL_POS
        else:
            s = INITIAL_POS + (GRAVITY - sign(GRAVITY) * FRICTION_MAG) * t ** 2
    elif sign(INITIAL_VEL) == sign(GRAVITY - INITIAL_FRICTION) or t <= transition_time:
        s = INITIAL_POS + INITIAL_VEL * t + (GRAVITY - INITIAL_FRICTION) * t ** 2
    else:
        if FRICTION_MAG >= abs(GRAVITY):
            s = transition_pos
        else:
            s = transition_pos + (GRAVITY - sign(GRAVITY) * FRICTION_MAG) * t ** 2

    return Vec(SCREEN_WIDTH / 2, s)

def screen_pos(pos: Vec) -> tuple[int, int]:
    return (round(pos.x), round(pos.y))

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