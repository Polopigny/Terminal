import pyxel

time = 1
debug_mode = False

def update():
    global debug_mode,time
    if pyxel.btnp(pyxel.KEY_O):
        debug_mode = not debug_mode


    if debug_mode == True and pyxel.btnp(pyxel.KEY_P):
        time = 0
    elif debug_mode == True and pyxel.btnp(pyxel.KEY_L):
        time = 0.25
    if debug_mode == False:
        time = 1
    

def draw():
    if debug_mode:
        pyxel.text(256//2 - 30, 5, "DEBUG MODE ENABLE", pyxel.COLOR_YELLOW)
        pyxel.text(256//2 + 50, 5, f"time:{time}", pyxel.COLOR_YELLOW)