import pyxel
import debug
from player import player
import enemi

class App:
    def __init__(self):
        pyxel.init(256, 256, "Terminal V1.1", fps=30)
        pyxel.load("../Template/2.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        player.update()
        debug.update()

        for e in enemi.list_enemi_global:
            e.update()

        enemi.update_global()

    def draw(self):
        pyxel.cls(0)
        player.draw()
        debug.draw()
        enemi.debug_enemi()

        for e in enemi.list_enemi_global:
            e.draw()
        

App()
