import pyxel
import Menu


class App:
    def __init__(self):
        pyxel.init(256, 256, "Terminal V1.1", fps=30)
        pyxel.load("../Template/2.pyxres")

        self.current_scene = Menu.menu

        #toujours à la fin de init
        pyxel.run(self.update, self.draw)
        
    def switch_scene(self):
        match Menu.menu_state:
            case "menu":
                self.current_scene = Menu.menu
            case "game":
                self.current_scene = Menu.game



    def update(self):
        self.switch_scene()
        pyxel.mouse(True)
        self.current_scene.update()


    def draw(self):
        self.current_scene.draw()
        pyxel.line(127,0,127,256,pyxel.COLOR_WHITE)
        pyxel.line(63.5,0,63.5,256,pyxel.COLOR_WHITE)

        

App()
