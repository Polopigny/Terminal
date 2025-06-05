import pyxel
import debug
from player import player
from enemi import ENemi


class App:
    def __init__(self):
        pyxel.init(256, 256, "Terminal V1.1", fps=30)
        pyxel.load("../Template/2.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        player.update()
        debug.update()
        ENemi.update()

    def draw(self):
        pyxel.cls(0)
        player.draw()
        debug.draw()
        ENemi.draw()
        pyxel.line(ENemi.x,ENemi.y,player.x,player.y,pyxel.COLOR_CYAN)
        

App()
