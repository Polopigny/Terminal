import pyxel
import debug
from player import Player

class App:
    def __init__(self):
        self.player = Player()

        pyxel.init(256, 256, "Terminal V1.1", fps=30)
        pyxel.load("../Template/2.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        debug.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        debug.draw()
        

App()
