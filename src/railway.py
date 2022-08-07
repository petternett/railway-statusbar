#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Petter J. Barhaugen (petter@petternett.no)"

import os
import time
import random
import math
from datetime import datetime, timedelta
from pynput import keyboard
import threading

FPS = 30
DELAY = 1.0 / FPS

WIDTH = 16
PLAYER_POS = 3

MAX_SPEED = 1
FRICTION_CONST = 0.8

PLAYER_CHAR = '🚃'
RAIL_CHAR = '..'
FIRE_CHAR = '🔥'
CACTUS_CHAR = '🌵'

world = [RAIL_CHAR] * WIDTH
foreground = [RAIL_CHAR] * WIDTH
background = [None] * WIDTH

velocity = 0.0
total_km = 0.0
c = 0

new_press = None
pressed = False

debug_text = None

# TODO: stop using so much cpu when idle
# TODO: persistent km counter, store in XDG_DATA_HOME (python-xdg)


def render():

    # Print km counter
    print(f"Total km: {total_km:.2f} ", end="")

    global c
    # Compose world
    world = [x for x in foreground]
    # for i in range(0, WIDTH):
    #     if background[i] is not None: world[i] = background[i]
    world[PLAYER_POS] = PLAYER_CHAR
    if velocity > 0.9:
        world[PLAYER_POS-1] = FIRE_CHAR
        if c % 3 == 0 or c % 2 == 0:
            world[PLAYER_POS-2] = FIRE_CHAR
        c += 1


    # Print world
    for i in range(0, WIDTH-1):
        print(world[i], end="")
    print()


    # Print debug
    if debug_text: print(f"DEBUG: {debug_text}")


def debug(text):
    global debug_text
    debug_text = text

def on_release(key):
    global new_press, pressed
    new_press.set()
    pressed = True

def run():
    global velocity, foregroud, background, total_km, new_press, pressed

    ax = 0.0
    counter = 0.0

    new_press = threading.Event()
    listener = keyboard.Listener(on_release=on_release)
    listener.start()


    # Initial render
    render()


    # Actual game loop:
    # - Process input
    # - Update physics, world
    # - Render
    # - Sleep
    while True:

        # In case I ever need to implement for >1 event per tick
        n_evts = 0

        # Process input. If key event happens in tick:
        if (pressed):
            n_evts += 1
            pressed = False
        elif n_evts > 0:
            n_evts -= 1


        # Add number of events to velocity. If no events, reduce velocity.
        if n_evts > 0:
            ax += 0.02
        elif velocity > 0:
            ax -= 0.005
        elif velocity <= 0:
            ax = 0
            velocity = 0

        # debug(f"velocity: {velocity}, ax: {ax}")
        velocity += ax - velocity * FRICTION_CONST

        # Limit speed
        velocity = min(velocity, MAX_SPEED)

        # If stopped
        if (velocity == 0):
            new_press.wait()
            new_press.clear()
        
        cur_time = time.time()

        # Add to counter
        counter += velocity

        # Update world
        # for i in range(0, velocity):  # If moving 2 tiles over 1 frame
        if (counter >= 1):
            foreground.pop(0)
            if (random.randint(0, 5) ==  1):
                foreground.append(CACTUS_CHAR)
            else:
                foreground.append(RAIL_CHAR)

            counter -= 1
            total_km += 0.01 # TODO: adjust


        # Render
        # debug(f"vel: {velocity:.4f}, ax: {ax}")
        # TODO: put in update if-check?
        render()


        # Sleep
        time.sleep(cur_time + DELAY - time.time())


        # Background (parallax)
        # background.pop(0)
        # if (random.randint(0, 20) == 1):
        #     background.append("🏔️")
        # else:
        #     background.append(None)
                   


if __name__ == "__main__":
    run()
