import pyxel
import debug
import enemi
class Player:
    def __init__(self):
        self.x = 256 // 2
        self.y = 256 // 2

        self.base_speed = 1
        self.debug_speed = 4
        self.speed = self.base_speed

        self.base_life = 3
        self.life = self.base_life

        self.width = 16
        self.height = 16
        self.color = pyxel.COLOR_RED

        self.debug_text = ""
        self.debug_text_x = 0
        self.debug_text_y = 0

    def move(self):
        self.speed = self.debug_speed if debug.debug_mode else self.base_speed
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed * debug.time_speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed * debug.time_speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed * debug.time_speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed * debug.time_speed

    def update_debug_info(self):
        self.debug_text_x = self.x - 12
        self.debug_text_y = self.y - 8
        self.debug_text = f"{int(self.x)}, {int(self.y)}"

    def update_camera_and_window(self):
        debug.windowX = self.x
        debug.windowY = self.y

    def update(self):
        self.move()
        self.update_camera_and_window()
        if debug.debug_mode:
            self.update_debug_info()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 16, self.width, self.height, colkey = 2)
        pyxel.text(self.x+88, self.y - 118, f"live = {self.life}", pyxel.COLOR_GREEN)

        if debug.debug_mode:
            pyxel.text(self.debug_text_x, self.debug_text_y, self.debug_text, pyxel.COLOR_WHITE)
            pyxel.circb(self.x+self.width/2, self.y+self.height/2, 9, pyxel.COLOR_GREEN)

    def reset(self):
        self.x = 256 // 2
        self.y = 256 // 2

        self.base_speed = 1
        self.debug_speed = 4
        self.speed = self.base_speed

        self.base_life = 3
        self.life = self.base_life

        self.width = 8
        self.height = 16
        self.color = pyxel.COLOR_RED

        self.debug_text = ""
        self.debug_text_x = 0
        self.debug_text_y = 0

        
player = Player()
