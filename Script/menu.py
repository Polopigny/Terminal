import pyxel
import debug
from player import player
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
        self.background_color = pyxel.COLOR_BLACK
        self.score=score.Score()
        self.collision=False
        self.list_enemi = []
        self.dmin_player_attack=3

    def evaluateCollisionStatus(self):
        '''
        Gérer le statut des collisons de l'épée et des ennemis.
        '''
        if len(self.getEnemyList())>0 and \
            (player.x>self.getEnemyList()[0].x+self.getDMinPlayerAttack() or \
             player.x<self.getEnemyList()[0].x+self.getDMinPlayerAttack()
            player.x==self.getEnemyList()[0].x-self.getDMinPlayerAttack()) and \
            (player.y==self.getEnemyList()[0].y+self.getDMinPlayerAttack() or \
            player.y==self.getEnemyList()[0].y-self.getDMinPlayerAttack()) :
            self.collision=True
        else: self.collision=False

    def getCollisionstatus(self):
        return self.collision
    
    def setEnemyList(self,enemy):
        self.list_enemi.append(enemy)

    def getEnemyList(self):
        return self.list_enemi
    
    def getCountEnemy(self):
        return len(self.list_enemi)
    
    def setDMinPlayerAttack(self,radius:int):
        self.dmin_player_attack=radius
    
    def getDMinPlayerAttack(self):
        return self.dmin_player_attack

    def reset_enemi_list(self):
        self.setEnemyList([])
    
    def update(self):
        
        global menu_state

        player.update()
        debug.update()
        VagueManager_var.update

        for e in self.getEnemyList():
            e.update()

        self.update_global()

    def update_global(self):
        self.evaluateCollisionStatus()
        enemi.mise_jour_liste_enemi()
        if pyxel.btnp(pyxel.KEY_U):
            enemi.creation()
        if pyxel.btnp(pyxel.KEY_SPACE) and self.getCountEnemy()>0 \
            and self.getCollisionstatus():
            self.getEnemyList().pop()
        if player.life <= 0:
            if debug.debug_mode:
                print("joueur mort")
            menu_state = "menu"
            VagueManager_var.reset()
            player.reset()
            self.reset_enemi_list()
        pyxel.camera(player.x-128,player.y-128)
        self.score.getScore()

    def draw(self):
        pyxel.cls(self.background_color)

        player.draw()
        debug.draw()
        enemi.debug_enemi()
        VagueManager_var.draw()

        for e in self.getEnemyList():
            e.draw()
        
        self.score.draw_local()


# Instances uniques
menu = Menu()
game = Game()
