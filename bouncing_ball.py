import itertools as it
import math
import sys
import pygame as pg
from pygame import Vector2 as Vec

W = 800 # screen width
H = 600 # screen height
R = 50 # ball radius
S0 = 100 # initial position of the ball's bottom point
U0 = 0.5 # initial velocity
G = 0.01 # acceleration due to gravity
K = 0.8 # coefficient of restitution

if S0 > H:
    raise RuntimeError('ball must be above ground')

DELTA = U0 ** 2 + 2 * G * (H - S0)
print('DELTA=', DELTA)

# t1 is the time the first bounce begins
if G == 0 and U0 > 0:
    t1 = (H - S0) / U0
    bounces_again = False
elif G == 0 or DELTA < 0:
    t1 = math.inf
    bounces_again = False
else:
    SQRT_DELTA = math.sqrt(DELTA)
    ROOTS = [(-U0 + sign * SQRT_DELTA) / G for sign in (-1, 1)]
    t1 = min(r for r in ROOTS if r >= -sys.float_info.epsilon)
    bounces_again = min(ROOTS) < sys.float_info.epsilon

print('t1=', t1, 'bounces_again=', bounces_again)

U1 = -K * (U0 + G * t1) # velocity starting the first bounce
print('U1=', U1)

T = math.inf if G == 0 or K == 1 else t1 - 2 * U1 / (G * (1 - K)) # time bouncing stops
print('T=', T)

def get_pos(t: int) -> Vec:
    if t <= t1:
        s = S0 + U0 * t + G * t ** 2 / 2
    else:
        t_ = t - t1

        if not bounces_again:
            s = H + U1 * t_ + G * t_ ** 2 / 2
        elif t >= T:
            s = H
        else:
            n = (
                math.floor(-G * t_ / (2 * U1)) if K == 1
                else 1 + math.floor(math.log(
                    1 + G * t_ * (1 - K) / (2 * U1),
                    K
                ))
            )

            k = K ** (n - 1)
            u = k * U1
            t0 = (-2 * U1 / G) * (n if K == 1 else (1 - k) / (1 - K))
            dt = t_ - t0

            if t % 100 == 0:
                print('n=', n, 'k=', k, 'u=', u, 't0=', t0, 'dt=', dt)

            s = H + u * dt + G * dt ** 2 / 2

    if t % 100 == 0:
        print('t=', t, 's=', s)

    return Vec(W / 2, s - R)

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
    s = get_pos(get_time())
    pg.draw.circle(screen(), 'white', screen_pos(s), R)
    pg.display.flip()