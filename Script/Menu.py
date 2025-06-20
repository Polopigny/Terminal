import pyxel
import debug
from player import player
import enemi

menu_state = "menu" # "power up", "game", "end_game", "setting"
window = 256

class Menu:
    def __init__(self):
        self.background_color = pyxel.COLOR_ORANGE

        self.button_play_var = Button(30, window//4, 20, 80)
        self.button_setting_var = Button(30, window//2, 20, 80)
        self.button_quit_var = Button(30, window//4 * 3, 20, 80)

    def buttons(self):
        global menu_state

        self.button_play_var.update()
        if self.button_play_var.is_click == True:
            menu_state = "game"

        self.button_setting_var.update()
        if self.button_setting_var.is_click == True:
            menu_state = "setting"

        self.button_quit_var.update()
        if self.button_quit_var.is_click == True:
            pyxel.quit()
    
    
    def update(self):
        self.buttons()

    def draw(self):
        pyxel.cls(self.background_color)

        pyxel.text(window//2 - 10, 10, "TERMINAL", pyxel.COLOR_BLACK)

        self.button_play_var.draw()
        pyxel.text(35, window//4 + 5, "PLAY", pyxel.COLOR_BLACK)

        self.button_setting_var.draw()
        pyxel.text(35, window//2 + 5, "SETTING", pyxel.COLOR_BLACK)

        self.button_quit_var.draw()
        pyxel.text(35, window//4 * 3 + 5, "QUIT", pyxel.COLOR_BLACK)

class Game:

    def __init__(self):
        self.background_color = pyxel.COLOR_BLACK

    def update(self):
        player.update()
        debug.update()

        for e in enemi.list_enemi_global:
            e.update()

        enemi.update_global()

    def draw(self):
        pyxel.cls(self.background_color)
        player.draw()
        debug.draw()
        enemi.debug_enemi()

        for e in enemi.list_enemi_global:
            e.draw()


#--------------------------------------------------------------------------
#------------tous ce qui faut pour rendre joli et à dupliquer--------------
#--------------------------------------------------------------------------

class Button:
    def __init__(self,x,y,heigth,width):
        self.x = x
        self.y = y
        self.heigth = heigth
        self.width = width

        self.background_color = pyxel.COLOR_GREEN
        self.outline_color = pyxel.COLOR_RED

        self.is_click = False

    def update(self):
        self.is_click = False

        if (self.x <= pyxel.mouse_x <= self.x + self.width and
            self.y <= pyxel.mouse_y <= self.y + self.heigth):
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.is_click = True
 

    def draw(self):
        pyxel.rect(self.x,self.y,self.width,self.heigth,self.background_color)
        pyxel.rectb(self.x,self.y,self.width,self.heigth,self.outline_color)


menu = Menu()
game = Game()