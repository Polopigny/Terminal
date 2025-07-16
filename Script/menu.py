import pyxel
import debug
import player
import enemi
from enemyVagueManager import VagueManager_var
from score import score
import time_game
# États possibles du menu
menu_state = "menu"  # "power up", "game", "game_over", "setting"
window_size = 256

class Button:
        """
        Bouton cliquable pour le menu.
        """
        def __init__(self,x, y, width, height,cmx=0, cmy=0,color_background=pyxel.COLOR_GREEN,
        color_outline=pyxel.COLOR_RED):
            self.x = x
            self.y = y
            self.cmx = cmx
            self.cmy = cmy
            self.width = width
            self.height = height
            self.is_click = False
            self.background_color = color_background
            self.outline_color = color_outline

        def update(self):
            """
            Vérifie si le bouton est cliqué.
            """
            self.is_click = False
            if (self.x <= pyxel.mouse_x + self.cmx <= self.x + self.width and
                self.y <= pyxel.mouse_y + self.cmy <= self.y + self.height and
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
            time_game.update()

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
            #pyxel.load('..\Template\2.pyxres')
            
        def update(self):
            global menu_state, game_over
            time_game.update()
            time_game.update_time_game()
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
                game_over.__init__()
                menu_state = "game_over"
                

            pyxel.camera(player.player.x - 128, player.player.y-128)
            score.update_score()

        def draw(self):
            pyxel.cls(self.background_color)
            #map
            pyxel.bltm(0,0,0,0,0,768,768,colkey=2)
            #debug
            debug.draw()
            enemi.debug_enemi()
            #dessiner le temps debug
            if debug.debug_mode == True:
                 pyxel.text(player.player.x-118, player.player.y+98, f"time = {time_game.time_game_seconds}", pyxel.COLOR_WHITE)
            #hud vague
            VagueManager_var.draw()
            #enemi
            for e in enemi.list_enemi_global:
                e.draw()
            #enemi projectile
            for e in enemi.list_projectile_global:
                e.draw()
            #hud score
            score.draw()
            #hud player + player
            player.player.draw()
            
class Game_over():
        #---------------------------------------------
        #---------Reprise de tout le jeu--------------
        #---------------------------------------------
        def __init__(self):
            #---Reprise des trucs du jeu----------------------
            self.background_color = pyxel.COLOR_DARK_BLUE
            #-------------------------------------------------
            #---tt ce qui à a faire une fois le joueur mort---
            self.oppacity = 0.7 #entre 0 et 1 max
            self.overlay_color = pyxel.COLOR_BLACK
            self.x = player.player.x -128
            self.y = player.player.y -128

            self.button_restart = Button(self.x + 64, self.y + 200, 60, 15,self.x,self.y)
            self.button_menu = Button(self.x + 160,self.y +200, 60, 15,self.x, self.y)
            #-------------------------------------------------


        def draw_game(self):
            pyxel.cls(self.background_color)
            #map
            pyxel.bltm(0,0,0,0,0,768,768,colkey=2)
            #debug
            debug.draw()
            enemi.debug_enemi()
            #enemi
            for e in enemi.list_enemi_global:
                e.draw()
            #enemi projectile
            for e in enemi.list_projectile_global:
                e.draw()
            #hud player + player
            player.player.draw()
        
        #---------------------------------------------
        #------TT la partie qui gére end screen-------
        #---------------------------------------------
        def game_reset(self):
            VagueManager_var.reset()
            player.player.reset()
            enemi.reset_enemi_list()
            score.reset()
            time_game.reset_game_time()
            pyxel.camera(player.player.x - 128, player.player.y-128)
        
        
        def buttons_update(self):
            global menu_state

            self.button_menu.update()
            if self.button_menu.is_click:
                self.game_reset()
                menu_state = "menu"

            self.button_restart.update()
            if self.button_restart.is_click:
                self.game_reset()
                menu_state = "game"
        
        def buttons_draw(self):
            self.button_menu.draw()
            pyxel.text(self.x + 185,self.y +207,"Menu",pyxel.COLOR_WHITE)

            self.button_restart.draw()
            pyxel.text(self.x + 89,self.y +207,"Restart",pyxel.COLOR_WHITE)
        
        def draw_game_over_overlay(self):
            pyxel.dither(self.oppacity)
            pyxel.rect(self.x,self.y,pyxel.width,pyxel.height,self.overlay_color)
            pyxel.dither(1)
        
        def draw_stat(self):
            pyxel.rect(self.x + 110,self.y + 2,45,25,self.overlay_color)
            pyxel.text(self.x + 118,self.y+5,"GAME OVER", pyxel.COLOR_RED)
            pyxel.text(self.x + 118,self.y + 15,"Stat :", pyxel.COLOR_RED)
            pyxel.rect(self.x + 20,self.y + 49,150,50,self.overlay_color)
            pyxel.text(self.x + 30,self.y + 50, f"enemi kill = {score._killed_enemies}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 57, f"SCORE = {score._score}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 64, f"time = {time_game.time_game_min} (min) {time_game.time_game_seconds_x} (sc)", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 71, f"wave = {VagueManager_var.current_wave}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 78, f"weapon = {player.player.weapon}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 85, f"difficulty = {VagueManager_var.difficulty}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 92, f"nb enemy in game = {len(enemi.list_enemi_global)}", pyxel.COLOR_WHITE)

        
        def draw(self):
            self.draw_game()
            self.draw_game_over_overlay()
            self.draw_stat()
            self.buttons_draw()

            pyxel.text(self.x + 40,self.y +130,"j'ai eu la flemme de le faire beau déso ;)",pyxel.COLOR_WHITE)

        def update(self):
            time_game.update()
            debug.update()
            self.buttons_update()
            


# Instances uniques
menu = Menu()
game = Game()
game_over = Game_over()