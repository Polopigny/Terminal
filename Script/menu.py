import pyxel
import debug
import player
import enemi
from enemyVagueManager import VagueManager_var
import score

# États possibles du menu
menu_state = "menu"  # "power up", "game", "end_game", "setting"
window_size = 256


class Button:
    """
    Bouton cliquable pour le menu.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_click = False
        self.background_color = pyxel.COLOR_GREEN
        self.outline_color = pyxel.COLOR_RED

    def update(self):
        """
        Vérifie si le bouton est cliqué.
        """
        self.is_click = False
        if (self.x <= pyxel.mouse_x <= self.x + self.width and
            self.y <= pyxel.mouse_y <= self.y + self.height and
            pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)):

            self.is_click = True

    def draw(self):
        """
        Affiche le bouton.
        """
        pyxel.rect(self.x, self.y, self.width, self.height, self.background_color)
        pyxel.rectb(self.x, self.y, self.width, self.height, self.outline_color)


class Menu:
    """
    Menu principal du jeu.
    """
    def __init__(self):
        self.background_color = pyxel.COLOR_ORANGE
        self.button_play = Button(30, window_size // 4, 80, 20)
        self.button_setting = Button(30, window_size // 2, 80, 20)
        self.button_quit = Button(30, 3 * window_size // 4, 80, 20)

    def buttons(self):
        """
        Gère les clics sur les boutons.
        """
        global menu_state

        self.button_play.update()
        if self.button_play.is_click:
            menu_state = "game"

        self.button_setting.update()
        if self.button_setting.is_click:
            menu_state = "setting"

        self.button_quit.update()
        if self.button_quit.is_click:
            pyxel.quit()

    def update(self):
        self.buttons()

    def draw(self):
        pyxel.cls(self.background_color)
        pyxel.text(window_size // 2 - 20, 10, "TERMINAL", pyxel.COLOR_BLACK)

        self.button_play.draw()
        pyxel.text(50, window_size // 4 + 5, "PLAY", pyxel.COLOR_BLACK)

        self.button_setting.draw()
        pyxel.text(45, window_size // 2 + 5, "SETTING", pyxel.COLOR_BLACK)

        self.button_quit.draw()
        pyxel.text(50, 3 * window_size // 4 + 5, "QUIT", pyxel.COLOR_BLACK)


class Game:
    """
    Gère l'état principal de jeu.
    """
    def __init__(self):
        self.background_color = pyxel.COLOR_DARK_BLUE
        self._score = score.Score()
        #pyxel.load('..\Template\2.pyxres')
        
    def update(self):
        global menu_state

        player.player.update()
        debug.update()
        VagueManager_var.update()

        for e in enemi.list_enemi_global:
            e.update()
        
        for e in enemi.list_projectile_global:
            e.update()

        enemi.update_global()

        if player.player.life <= 0:
            if debug.debug_mode:
                print("Player DIED")
            menu_state = "menu"
            VagueManager_var.reset()
            player.player.reset()
            enemi.reset_enemi_list()
        pyxel.camera(player.player.x - 128, player.player.y-128)
        self._score.update_score()

    def draw(self):
        pyxel.cls(self.background_color)
        pyxel.bltm(0,0,0,0,0,768,768,colkey=2)
        debug.draw()
        enemi.debug_enemi()
        VagueManager_var.draw()

        for e in enemi.list_enemi_global:
            e.draw()
        
        for e in enemi.list_projectile_global:
            e.draw()
        
        self._score.draw()
        player.player.draw()

# Instances uniques
menu = Menu()
game = Game()