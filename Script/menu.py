import pyxel
import debug
import player
import enemi
from enemyVagueManager import VagueManager_var
from score import score
import time_game
# États possibles du menu
menu_state = "menu"  # "power up", "game", "game_over", "setting", "debug_portal"
window_size = 256
fps = 30

class Button:
        """
        Bouton cliquable pour le menu.
        """
        def __init__(self,x, y, width, height,cmx=0, cmy=0,color_background=pyxel.COLOR_GREEN,
        color_outline=pyxel.COLOR_RED,name="uname"):
            self.x = x
            self.y = y
            self.cmx = cmx
            self.cmy = cmy
            self.width = width
            self.height = height
            self.is_click = False
            self.background_color = color_background
            self.outline_color = color_outline
            self.name = name

        def update(self):
            """
            Vérifie si le bouton est cliqué.
            """
            self.is_click = False
            if (self.x <= pyxel.mouse_x + self.cmx <= self.x + self.width and
                self.y <= pyxel.mouse_y + self.cmy <= self.y + self.height and
                pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):

                self.is_click = True
                if debug.debug_mode == True:
                    print(f"bouton position {self.x},{self.y}, {self.name} appuie")

        def draw(self):
            """
            Affiche le bouton.
            """
            pyxel.rect(self.x, self.y, self.width, self.height, self.background_color)
            pyxel.rectb(self.x, self.y, self.width, self.height, self.outline_color)

class Slider:
    def __init__(self, x, y, width, height, cmx=0, cmy=0,
                 color_background=pyxel.COLOR_GREEN,
                 color_outline=pyxel.COLOR_RED,
                 circle_color=pyxel.COLOR_CYAN,
                 start_nb=0,name="uname"):
        self.x = x
        self.y = y
        self.cmx = cmx
        self.cmy = cmy
        self.width = width  # longueur du slider en pixels
        self.height = height
        self.is_click = False
        self.background_color = color_background
        self.outline_color = color_outline
        self.circle_color = circle_color
        self.marge = 5  # distance mini aux bords en pixels
        self.circle_x = x + self.marge

        self.nb_slider = 0
        self.nb_slider_start = start_nb
        self.name = name

    def update(self):
        self.is_click = False
        mouse_x = pyxel.mouse_x + self.cmx
        mouse_y = pyxel.mouse_y + self.cmy

        if (self.x <= mouse_x <= self.x + self.width and
            self.y - 10 <= mouse_y <= self.y + self.height + 10 and
            pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)):
            self.is_click = True
            self.circle_x = max(self.x + self.marge,
                                min(self.x + self.width - self.marge, mouse_x))
            if debug.debug_mode == True:
                    print(f"slider position {self.x},{self.y}, {self.name} appuier : valeur {self.circle_x}")
            
        
        self.nb_slider = int(self.circle_x - self.x - self.marge + self.nb_slider_start)

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.background_color)
        pyxel.rectb(self.x, self.y, self.width, self.height, self.outline_color)
        circle_y = self.y + self.height // 2
        pyxel.circ(self.circle_x, circle_y, self.height // 2 + 2, self.circle_color)
        pyxel.text(self.circle_x - 2,circle_y - 2,f"{str(int(self.nb_slider))}", pyxel.COLOR_BLACK)


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

class Debug_portal:
    def __init__(self):
        self.background_color = pyxel.COLOR_ORANGE
        self.button_back = Button(window_size//2 - 45,230,100,15,name="bakc")
        self.button_menu = Button(window_size//4 - 45,50,100,15,name="menu")
        self.button_game = Button(window_size//4 - 45,80,100,15,name="game")
        self.button_gameOver = Button(window_size//4 - 45,100,100,15,name="gameover")
        self.button_debug = Button(window_size//4 - 45,120,100,15,name="debugtoggle")
        self.button_invacibility = Button(window_size//4 - 45,140,100,15,name="invacibility")
        self.button_moins_vague = Button(window_size//4 - 45,160,30,10,name="-vague")
        self.button_plus_vague = Button(window_size//4 + 10,160,30,10,name="+vague")
        self.button_attente_debut_vague = Button(window_size//4 - 45,180,100,10,name="attente_debut_vague")
        self.slider_vitesse_joueur = Slider(window_size//4 - 45,200,100,15,start_nb=2,name="vitesse joueur")

    def update(self):
        global menu_state
        debug.update()
        time_game.update()
        #bouton back
        self.button_back.update()
        if self.button_back.is_click:
            menu_state = "setting"
        #bouton menu
        self.button_menu.update()
        if self.button_menu.is_click:
            menu_state = "menu"
        #bouton game
        self.button_game.update()
        if self.button_game.is_click:
            menu_state = "game"
        #bouton game over
        self.button_gameOver.update()
        if self.button_gameOver.is_click:
            player.player.life = 0
            menu_state = "game"
        #bouton debug
        self.button_debug.update()
        if self.button_debug.is_click:
            debug.debug_mode = True
        #bouton invincible
        self.button_invacibility.update()
        if self.button_invacibility.is_click:
            player.player.invincibility = not player.player.invincibility
            if debug.debug_mode == True:
                print(f"invincibilité : {player.player.invincibility} ")
        #bouton moin et plus vague
        self.button_moins_vague.update()
        if self.button_moins_vague.is_click:
            VagueManager_var.current_wave -= 1
        self.button_plus_vague.update()
        if self.button_plus_vague.is_click:
            VagueManager_var.current_wave += 1
        #bouton attente début vague
        self.button_attente_debut_vague.update()
        if self.button_attente_debut_vague.is_click:
            VagueManager_var.start_delay_over = not VagueManager_var.start_delay_over
        #Slider vitesse joueur
        self.slider_vitesse_joueur.update()
        player.player.speed = self.slider_vitesse_joueur.nb_slider

    def draw(self):
        pyxel.cls(self.background_color)
        #bouton back 
        self.button_back.draw()
        pyxel.text(window_size//2,235,"BACK",pyxel.COLOR_WHITE)
        #bouton menu 
        self.button_menu.draw()
        pyxel.text(window_size//4,55,"MENU",pyxel.COLOR_WHITE)
        #bouton game
        self.button_game.draw()
        pyxel.text(window_size//4,85,"GAME",pyxel.COLOR_WHITE)
        #bouton game over
        self.button_gameOver.draw()
        pyxel.text(window_size//4,105,"GAME OVER",pyxel.COLOR_WHITE)
        #bouton game over
        self.button_debug.draw()
        pyxel.text(window_size//4,125,"DEBUG TOGGLE",pyxel.COLOR_WHITE)
        #bouton invincible
        self.button_invacibility.draw()
        pyxel.text(window_size//4 - 30,145,f"INVICIBILITY :{player.player.invincibility}",pyxel.COLOR_WHITE)
        #bouton moins et plus vague
        self.button_plus_vague.draw()
        pyxel.text(window_size//4 + 23,163,"+",pyxel.COLOR_WHITE)
        self.button_moins_vague.draw()
        pyxel.text(window_size//4 - 30,163,"-",pyxel.COLOR_WHITE)
        pyxel.text(window_size//4 - 5,163,f"{VagueManager_var.current_wave}",pyxel.COLOR_BLACK)
        #bouton attente début vague
        self.button_attente_debut_vague.draw()
        pyxel.text(window_size//4- 20,185,f"Attente début vague :{VagueManager_var.start_delay_over}",pyxel.COLOR_WHITE)
        #slider vitesse
        self.slider_vitesse_joueur.draw()
        pyxel.text(window_size//4- 20,220,f"vitesse joueur ↑",pyxel.COLOR_WHITE)

class Setting:
    def __init__(self):
        self.background_color = pyxel.COLOR_ORANGE

        self.difficulte_slider = Slider(window_size/6,30,100,10,start_nb=4,name="difficulte")
        self.fps_slider = Slider(window_size/6,160,200,10,start_nb=15,name="fps")        
        self.vie_joueur_slider = Slider(window_size/6,60,100,10,start_nb=3,name="vie")

        self.button_back = Button(window_size//2 - 45,230,100,15,name="back")
        self.button_debug = Button(200,230,50,15,name="debugportal")

        self.button_sound = Button(window_size/6,80,100,15,name="sound")
        self.button_control = Button(window_size/6,100,100,15,name="control")
        self.button_reset = Button(window_size/6,120,100,15,name="reset")
        self.button_color_pallette = Button(window_size/6,180,100,15,name="color_pallette")

        #si update à copier coller dans le reset !!!!
    def buttons_update(self):
        global menu_state
        self.button_sound.update()
        if self.button_sound.is_click:
            menu_state = "sound_setting"
        
        self.button_control.update()
        if self.button_control.is_click:
            menu_state = "control_setting"

        self.button_reset.update()
        if self.button_reset.is_click:
            player.player.reset()
            score.reset()
            enemi.reset_enemi_list()
            self.reset_setting()
        
        self.button_color_pallette.update()
        if self.button_color_pallette.is_click:
            pass
    
    def buttons_draw(self):
        self.button_sound.draw()
        pyxel.text(window_size/6 + 20,85,"SOUND",pyxel.COLOR_WHITE)

        self.button_control.draw()
        pyxel.text(window_size/6 + 20,105,"CONTROL",pyxel.COLOR_WHITE)

        self.button_reset.draw()
        pyxel.text(window_size/6 + 20,125,"RESET",pyxel.COLOR_WHITE)
        if self.button_reset.is_click:
            pyxel.text(window_size/6 + 20,125,"RESET MADE",pyxel.COLOR_WHITE)
        
        self.button_color_pallette.draw()
        pyxel.text(window_size/6 + 20,185,"COLOR PALETTE",pyxel.COLOR_WHITE)
        if self.button_color_pallette.is_click:
            if self.button_color_pallette.background_color <= 16:
                self.button_color_pallette.background_color += 1
            else:
                self.button_color_pallette.background_color = 0

    def sliders_update(self):
        self.difficulte_slider.update()
        VagueManager_var.difficulty = self.difficulte_slider.nb_slider

        self.vie_joueur_slider.update()
        player.player.life = self.vie_joueur_slider.nb_slider

        self.fps_slider.update()
        self.fps = self.fps_slider.nb_slider
      

    def sliders_draw(self):
        #titre
        pyxel.text(window_size/6 - 10, 20, "DIFFICULTE", pyxel.COLOR_WHITE)
        pyxel.text(window_size/6 + 38, 20, "// Attention peut provoquer beug/lag", pyxel.COLOR_WHITE)
        #slider
        self.difficulte_slider.draw()
        #titre
        pyxel.text(window_size/6, 48, "VIE JOUEUR", pyxel.COLOR_WHITE)
        #slider
        self.vie_joueur_slider.draw()
        #titre
        pyxel.text(window_size/6, 140, "FPS", pyxel.COLOR_WHITE)
        pyxel.text(window_size/6 - 40, 150, "Alors pour que ca marche faut attendre la prochaine mise à jour", pyxel.COLOR_WHITE)
        #slider
        self.fps_slider.draw()
    
    def reset_setting(self):
        self.background_color = pyxel.COLOR_ORANGE

        self.difficulte_slider = Slider(window_size/6,30,100,10,start_nb=4,name="difficulte")
        self.fps_slider = Slider(window_size/6,160,200,10,start_nb=15,name="fps")        
        self.vie_joueur_slider = Slider(window_size/6,60,100,10,start_nb=3,name="vie")

        self.button_back = Button(window_size//2 - 45,230,100,15,name="back")
        self.button_debug = Button(200,230,50,15,name="debugportal")

        self.button_sound = Button(window_size/6,80,100,15,name="sound")
        self.button_control = Button(window_size/6,100,100,15,name="control")
        self.button_reset = Button(window_size/6,120,100,15,name="reset")
        self.button_color_pallette = Button(window_size/6,180,100,15,name="color_pallette")


    def button_back_update(self):
        global menu_state
        self.button_back.update()
        if self.button_back.is_click:
            menu_state = "menu"
    
    def button_debug_portal_update(self):
        global menu_state
        self.button_debug.update()
        if self.button_debug.is_click:
            menu_state = "debug_portal"


    def draw(self):
        pyxel.cls(self.background_color)
        #titre
        pyxel.text(window_size//2 - 10,5,"SETTINGS", pyxel.COLOR_WHITE)
        #paramétre
        self.buttons_draw()
        self.sliders_draw()
        #bouton back 
        self.button_back.draw()
        pyxel.text(window_size//2,235,"BACK",pyxel.COLOR_WHITE)
        #bouton debug portal
        self.button_debug.draw()
        pyxel.text(202,235,"DEBUG PORTAL",pyxel.COLOR_WHITE)


    def update(self):
        #paramètre
        self.buttons_update()
        self.sliders_update()
        #boutons
        self.button_back_update()
        self.button_debug_portal_update()

class Sound_setting:
    def __init__(self):
        self.background_color = pyxel.COLOR_ORANGE

        self.button_back = Button(window_size//2 - 45,230,100,15,name="back")

    def button_back_update(self):
        global menu_state
        self.button_back.update()
        if self.button_back.is_click:
            menu_state = "setting"

    def update(self):
        self.button_back_update()
    
    def draw(self):
        pyxel.cls(self.background_color)
        pyxel.text(window_size/2 - 70,window_size/2 - 30,"déso, flemme de faire à attendre prochaine maj", pyxel.COLOR_WHITE)
        #bouton back 
        self.button_back.draw()
        pyxel.text(window_size//2,235,"BACK",pyxel.COLOR_WHITE)

class Control_setting:
    def __init__(self):
        self.background_color = pyxel.COLOR_ORANGE

        self.button_back = Button(window_size//2 - 45,230,100,15,name="back")

    def button_back_update(self):
        global menu_state
        self.button_back.update()
        if self.button_back.is_click:
            menu_state = "setting"

    def update(self):
        self.button_back_update()
    
    def draw(self):
        pyxel.cls(self.background_color)
        pyxel.text(window_size/2  - 70,window_size/2 - 30,"déso, flemme de faire à attendre prochaine maj", pyxel.COLOR_WHITE)
        #bouton back 
        self.button_back.draw()
        pyxel.text(window_size//2,235,"BACK",pyxel.COLOR_WHITE)


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

            if player.player.life <= 0 and player.player.invincibility == False:
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
            
class Game_over:
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

            self.button_restart = Button(self.x + 64, self.y + 200, 60, 15,self.x,self.y,name="restart")
            self.button_menu = Button(self.x + 160,self.y +200, 60, 15,self.x, self.y,name="menu")
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
            pyxel.rect(self.x + 20,self.y + 49,150,100,self.overlay_color)
            pyxel.text(self.x + 30,self.y + 50, f"enemi kill = {score._killed_enemies}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 57, f"SCORE = {score._score}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 64, f"time = {time_game.time_game_min} (min) {time_game.time_game_seconds_x} (sc)", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 71, f"wave = {VagueManager_var.current_wave}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 78, f"weapon = {player.player.weapon}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 85, f"difficulty = {VagueManager_var.difficulty}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 92, f"nb enemy in game = {len(enemi.list_enemi_global)}", pyxel.COLOR_WHITE)
            pyxel.text(self.x + 30,self.y + 99, f"hit taken = {player.player.hit_counter}", pyxel.COLOR_WHITE)

        
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
setting = Setting()
debug_portal = Debug_portal()
sound_setting = Sound_setting()
control_setting = Control_setting()