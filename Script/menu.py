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
        self.list_enemy = []
        self.dmin_player_attack=3
        self.e_is_top=False
        self.e_is_left=False
        self.d_enemy_2_player=9999999999

    def setEnemyPosition(self):
        '''
        Avoir la position cardinal d'un ennemi par rapport au joueur.
        '''
        if player.x>self.getEnemyList()[0].x:
            self.e_is_left=True
        if player.x<self.getEnemyList()[0].x:
            self.e_is_left=False
        if player.y>self.getEnemyList()[0].y:
            self.e_is_top=True
        if player.y<self.getEnemyList()[0].y:
            self.e_is_top=False

    def getEnemyPosition(self):
        return self.e_is_top,self.e_is_left
    
    def evaluateDistanceEnemy2Player(self):
        if self.getEnemyPosition()[1]:
            d_x_enemy_2_player=player.x-self.getEnemyList()[0].x
        else : d_x_enemy_2_player=self.getEnemyList()[0].x-player.x
        if self.getEnemyPosition()[0]:
            d_y_enemy_2_player=self.getEnemyList()[0].y-player.y
        else : d_y_enemy_2_player=player.y-self.getEnemyList()[0].y
        self.d_enemy_2_player=d_x_enemy_2_player**2+d_y_enemy_2_player**2

    def getDistanceEnemy2Player(self):
        return self.d_enemy_2_player
    
    def evaluateCollisionStatus(self):
        self.evaluateDistanceEnemy2Player()
        if self.getDistanceEnemy2Player()<=self.getDMinPlayerAttack():
            self.collision=True
        else:self.collision=False

    def getCollisionstatus(self):
        return self.collision
    
    def setEnemyList(self,enemy):
        self.list_enemy.append(enemy)

    def getEnemyList(self):
        return self.list_enemy
    
    def getCountEnemy(self):
        return len(self.list_enemy)
    
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
        if self.getCountEnemy()>0:
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
