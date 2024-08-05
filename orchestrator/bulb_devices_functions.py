import time

import tinytuya

# for testing purposes
d = tinytuya.BulbDevice(
    dev_id='eb93fc2a1cc62cb31cpnxj',
    address='Auto',
    local_key="'|}|CS_-2T{rSMY1",
    version=3.3)

d.set_socketPersistent(True)


# ---------------------------------------- SETTING COLORS --------------------------------------------------------------
# RED COLORS
def set_red():  # Red (255, 0, 0)
    d.set_colour(255, 0, 0, nowait=False)


def set_blue():  # Blue (0, 0, 255)
    d.set_colour(0, 0, 255, nowait=False)


def set_green():  # Green (0, 255, 0)
    d.set_colour(0, 255, 0, nowait=False)


def set_yellow():  # Yellow (255, 255, 0)
    d.set_colour(255, 255, 0, nowait=False)


def set_purple():  # Purple (128, 0, 128)
    d.set_colour(128, 0, 128, nowait=False)


def set_orange():  # Orange (255, 165, 0)
    d.set_colour(255, 165, 0, nowait=False)


def set_pink():  # Pink (255, 192, 203)
    d.set_colour(255, 192, 203, nowait=False)


def set_indigo():
    d.set_colour(75, 0, 130, nowait=False)


def set_cyan():
    d.set_colour(0, 255, 255, nowait=False)


def set_magenta():
    d.set_colour(255, 0, 255, nowait=False)


def set_teal():
    d.set_colour(0, 128, 128, nowait=False)


def set_lime():
    d.set_colour(0, 255, 0, nowait=False)


def set_white_color():  # White (255, 255, 255)
    d.set_colour(255, 255, 255, nowait=False)


# ---------------------------------------- SATURATION CHANGES ----------------------------------------------------------
def decrease_saturation():
    h, s, v = d.colour_hsv()
    new_saturation = max(s - 0.25, 0)
    d.set_hsv(h, new_saturation, v, nowait=False)


def increase_saturation():
    h, s, v = d.colour_hsv()
    new_saturation = min(s + 0.25, 1)
    d.set_hsv(h, new_saturation, v, nowait=False)

# ---------------------------------------- BRIGHTNESS CHANGES ----------------------------------------------------------


def increase_brightness():
    current_brightness = d.brightness()
    new_brightness = min(current_brightness + 250, 1000)
    d.set_brightness(new_brightness)


def decrease_brightness():
    brightness = d.brightness()
    new_brightness = max(brightness - 250, 0)
    d.set_brightness(new_brightness, nowait=False)
