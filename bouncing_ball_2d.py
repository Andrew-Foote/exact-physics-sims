# There's a bug here somewhere---later bounces appear to jump horizontally.

import math
import sys
import pygame as pg
from pygame import Vector2 as Vec

W = 800 # screen width
H = 600 # screen height
R = 50 # ball radius

# initial position of the ball's bottom point
S0X = 0
S0Y = 2 * R

# the ball's initial velocity
U0X = 0.1
U0Y = 0.2

G = 0.001 # acceleration due to gravity
K = 0.8 # coefficient of restitution

if S0Y > H:
    raise RuntimeError('ball must be above ground')

DELTA = U0Y ** 2 + 2 * G * (H - S0Y)
print('DELTA=', DELTA)

# T1 is the time the first bounce begins
if G == 0 and U0Y < 0:
    t1 = (H - S0Y) / U0Y
    bounces_again = True
elif G == 0 or DELTA < 0:
    t1 = math.inf
    bounces_again = False
else:
    SQRT_DELTA = math.sqrt(DELTA)
    ROOTS = [(-U0Y + sign * SQRT_DELTA) / G for sign in (-1, 1)]
    t1 = min(r for r in ROOTS if r >= -sys.float_info.epsilon)
    bounces_again = min(ROOTS) < sys.float_info.epsilon

print('t1=', t1, 'bounces_again=', bounces_again)

S1X = S0X + U0X * t1 # x-position starting the first bounce

# velocity starting the first bounce
U1X = K * U0X
U1Y = -K * (U0Y + G * t1)
print('U1=', U1X, U1Y)

T = math.inf if K == 1 else t1 - 2 * U1Y / (G * (1 - K)) # time bouncing stops
print('T=', T)
ST = math.inf if K == 1 else S1X - 2 * U1Y * U1X / (G * (1 - K)) # x-position when bouncing stops

def get_pos(t: int) -> Vec:
    if t <= t1:
        sx = S0X + U0X * t
        sy = S0Y + U0Y * t + G * t ** 2 / 2
    else:
        t_ = t - t1

        if not bounces_again:
            sx = H + U1X * t_
            sy = H + U1Y * t_ + G * t_ ** 2 / 2
        elif t >= T:
            sx = ST
            sy = H
        else:
            n = (
                math.floor(-G * t_ / (2 * U1Y)) if K == 1
                else 1 + math.floor(math.log(
                    1 + G * t_ * (1 - K) / (2 * U1Y),
                    K
                ))
            )

            k = K ** (n - 1)
            ux = k * U1X
            uy = k * U1Y
            t0 = (-2 * U1Y / G) * (n if K == 1 else (1 - k) / (1 - K))
            dt = t_ - t0
            sx0 = S1X + (-2 * U1X * U1Y / G) * (n if K == 1 else (1 - k) / (1 - K))

            if t % 100 == 0:
                print('n=', n, 'k=', k, 'u=', ux, uy, 't0=', t0, 'dt=', dt, 'sx0=', sx0)

            sx = sx0 + ux * dt
            sy = H + uy * dt + G * dt ** 2 / 2

    if t % 100 == 0:
        print('t=', t, 's=', sx, sy)


    # if t % 1000 == 0:
    #     print('t=', t, 'n=', n, 'u=', u, 't0=', t0, 's=', s)

    return Vec(sx, sy - R)

def screen_pos(pos: Vec) -> tuple[int, int]:
    return (round(pos.x) % W, round(pos.y))

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
pg.display.set_mode((W, H))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    screen().fill('black')
    pos = get_pos(get_time())
    pg.draw.circle(screen(), 'white', screen_pos(pos), R)
    pg.display.flip()