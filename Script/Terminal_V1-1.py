import pyxel

debug_mode = False

class Player:
    def __init__(self):
        self.x = 256//2
        self.y = 256//2
        self.base_speed = 1
        self.speed = 1
        self.base_life = 3
        self.life = 3
        self.width = 8
        self.height = 16
        self.color = pyxel.COLOR_RED

        #debug
        self.debug_text_x = 0 
        self.debug_text_y = 0
        self.debug_text = ""
        self.debug_speed = 0

    def move(self):
        self.speed = self.debug_speed if debug_mode else self.base_speed

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
    
    def debug(self):
        #mettre text pos(x,y) au dessus du joueur
        self.debug_text_x = self.x - 12
        self.debug_text_y = self.y - 8
        self.debug_text = str(self.x) + " , " + str(self.y)

        #booster vitesse
        self.debug_speed = 4

    def update(self):
        self.move()
        if debug_mode == True:
            self.debug()

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

        if debug_mode == True:
            pyxel.text(self.debug_text_x,self.debug_text_y,self.debug_text,pyxel.COLOR_WHITE)

class Debug:
    global debug_mode
    def __init__(self):
        pass

    def update(self):
        global debug_mode
        if pyxel.btnp(pyxel.KEY_O):
            debug_mode = not debug_mode

    def draw(self):
        if debug_mode == True:
            pyxel.text(256//2 - 30,5,"DEBUG MODE ENABLE",pyxel.COLOR_YELLOW)

class App:
    def __init__(self):
        self.player = Player()
        self.debug = Debug()

        pyxel.init(256, 256, "Terminal V1.1", fps=30)
        pyxel.load("../Template/2.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.debug.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        self.debug.draw()

App()
