import pyxel

# Variables globales
time_speed = 1
debug_mode = False
windowX = 0
windowY = 0

def update():
    """
    Met à jour le mode debug et la vitesse du temps selon les touches.
    """
    global debug_mode, time_speed

    if pyxel.btnp(pyxel.KEY_O):
        debug_mode = not debug_mode

    if debug_mode:
        if pyxel.btnp(pyxel.KEY_P):
            time_speed = 0
        elif pyxel.btnp(pyxel.KEY_L):
            time_speed = 0.25
    else:
        time_speed = 1

def draw():
    """
    Affiche les infos de debug à l'écran.
    """
    if debug_mode:
        pyxel.text(windowX - 30, windowY - 123, "DEBUG MODE ENABLE", pyxel.COLOR_YELLOW)
        pyxel.text(windowX + 50, windowY - 123, f"time_speed: {time_speed}", pyxel.COLOR_YELLOW)
