import pyxel

debug_mode = False

def update():
    global debug_mode
    if pyxel.btnp(pyxel.KEY_O):
        debug_mode = not debug_mode

def draw():
    if debug_mode:
        pyxel.text(256//2 - 30, 5, "DEBUG MODE ENABLE", pyxel.COLOR_YELLOW)