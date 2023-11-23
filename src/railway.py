#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Petter J. Barhaugen (petter@petternett.no)"

import os
import sys
import time
import random
import math
from datetime import datetime, timedelta
from pynput import keyboard
import threading
from emoji import emojize

n = len(sys.argv)
UNITS = "km"
for i in range(1, n):
    if sys.argv[i] == "-u" or sys.argv[i] == "--units":
        import reverse_geocoder as rg
        import geocoder
        g = geocoder.ip('me')
        country = rg.search(g.latlng)[0]['cc']
        if country in ["US", "LR", "MM"]: # Liberia, Myanmar, USA (imperial system countries")
            UNITS = "mi"


WIDTH = 16
PLAYER_POS = 3

FPS = 30
DELAY = 1.0 / FPS
MAX_SPEED = 1
FRICTION_CONST = 0.8
velocity = 0.0
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache/railway_status")
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
CACHE_FILE = os.path.join(CACHE_DIR, "KM.txt")
with open(CACHE_FILE, 'r') as CACHE_OPP:
    file_content = CACHE_OPP.read()
    if file_content != "":
        TOTAL_DISTANCE = float(file_content)
    else:
        TOTAL_DISTANCE = 0.0

RAIL_CHAR = '..'
PLAYER_CHAR = emojize(":railway_car:")
FIRE_CHAR = emojize(":fire:")
CACTUS_CHAR = emojize(":cactus:")
MTN_CHAR = emojize(":snow-capped_mountain:")

world = [None] * WIDTH
foreground = [None] * WIDTH
background = [None] * WIDTH
PARA_CONST = 9
MAX_PARA_ELEMENTS = 2

fire_disp = 0
no_mnts = 0
MAX_NO_MNTS = 3

new_press_event = None
key_pressed = False

debug_text = None


def render():

    # Print km counter
    print(f"Total {UNITS}: {TOTAL_DISTANCE:.2f} ", end="")

    global fire_disp
    # Compose world
    world = [x for x in background]

    for i in range(0, WIDTH):
        if foreground[i] is not None:
            world[i] = foreground[i]
        elif world[i] == None:
            world[i] = RAIL_CHAR

    world[PLAYER_POS] = PLAYER_CHAR
    if velocity > 0.9:
        world[PLAYER_POS-1] = FIRE_CHAR
        if fire_disp % 3 == 0 or fire_disp % 2 == 0:
            world[PLAYER_POS-2] = FIRE_CHAR
        fire_disp += 1


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
    global new_press_event, key_pressed
    new_press_event.set()
    key_pressed = True

def run():
    global velocity, foregroud, background, no_mnts, TOTAL_DISTANCE, new_press_event, key_pressed

    ax = 0.0
    counter = 0.0
    para = 0

    new_press_event = threading.Event()
    listener = keyboard.Listener(on_release=on_release)
    listener.start()


    # Initial render
    render()


    # Actual "game" loop:
    # - Process input
    # - Update physics, world
    # - Render
    # - Sleep
    while True:

        # In case I ever need to implement for >1 event per tick
        n_evts = 0

        # Process input. If key event happens in tick:
        if (key_pressed):
            n_evts += 1
            key_pressed = False
        elif n_evts > 0:
            n_evts -= 1


        # Add number of events to velocity. If no events, reduce velocity.
        if n_evts > 0:
            ax += 0.02
        elif velocity > 0:
            ax -= 0.005  # TODO: replace with Cubic ease in/out
        elif velocity <= 0:
            ax = 0
            velocity = 0

        # debug(f"velocity: {velocity}, ax: {ax}")
        velocity += ax - velocity * FRICTION_CONST

        # Limit speed
        velocity = min(velocity, MAX_SPEED)

        # If stopped
        if (velocity == 0):
            new_press_event.wait()
            new_press_event.clear()

        cur_time = time.time()

        # Add to counter
        counter += velocity

        # Update world
        # for i in range(0, velocity):  # TODO: If moving 2 tiles over 1 frame
        if (counter >= 1):
            foreground.pop(0)
            if (random.randint(0, 5) ==  1):
                foreground.append(CACTUS_CHAR)
            else:
                foreground.append(None)

            if para == 0:
                if background[0] == MTN_CHAR: no_mnts -= 1

                background.pop(0)
                if (random.randint(0, 2) == 1 and no_mnts < MAX_NO_MNTS):
                    background.append(MTN_CHAR)
                    no_mnts += 1
                else:
                    background.append(None)

            # para = (para + 1) % PARA_CONST
            para += 1
            para %= PARA_CONST

            counter -= 1
            TOTAL_DISTANCE += 0.01 # TODO: adjust
            cache = open(CACHE_FILE, 'w+')
            TOTAL_DISTANCE += 0.01 # TODO: adjust
            cache.write(str(TOTAL_DISTANCE)[:5])
            cache.close()


        # debug(f"vel: {velocity:.4f}, ax: {ax}")
        render()


        # Sleep
        time.sleep(cur_time + DELAY - time.time())





if __name__ == "__main__":
    run()
