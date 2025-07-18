# title: Pyxel Terminal Alpha
# author: @Polopigny @CamMouren
# desc: A Pyxel inspired version of Vampire Survivors
# site: https://github.com/Polopigny/Terminal/
# license: GPLv3
# version: 1.0

import pyxel
import menu 
import debug
import anti_cheat

class App():
    def __init__(self):
        """
        Initialise la fenêtre Pyxel, charge les ressources et démarre le jeu.
        """
        self.fps = 30

        pyxel.init(256, 256, title="Terminal V1.1", fps=self.fps)
        pyxel.load("../Template/2.pyxres")

        self.current_scene = menu.menu  # Scène actuelle : menu par défaut
        self.old_scene = self.current_scene

        pyxel.run(self.update, self.draw)

    def switch_scene(self):
        """
        Change la scène selon l'état du menu.
        """
        match menu.menu_state:
            case "menu":
                self.current_scene = menu.menu
                anti_cheat.scene = "menu"
                pyxel.camera() 
            case "game":
                self.current_scene = menu.game
                anti_cheat.scene = "game"
            case "game_over":
                self.current_scene = menu.game_over
                anti_cheat.scene = "game_over"
                pyxel.camera(self.current_scene.x,self.current_scene.y)
            case "setting":
                self.current_scene = menu.setting
                anti_cheat.scene = "setting"
                pyxel.camera()
            case "debug_portal":
                self.current_scene = menu.debug_portal
                anti_cheat.scene = "debug_portal"
                pyxel.camera()
            case "sound_setting":
                self.current_scene = menu.sound_setting
                anti_cheat.scene = "sound_setting"
                pyxel.camera()
            case "control_setting":
                anti_cheat.scene = "control_setting"
                self.current_scene = menu.control_setting 
                pyxel.camera()
    
    def debug_main(self):
        if self.old_scene != self.current_scene:
            self.old_scene = self.current_scene
            if debug.debug_mode == True:
                print(f"scene : {self.current_scene}")

    def update(self):
        """
        Met à jour la scène actuelle et active la souris.
        """
        self.switch_scene()
        pyxel.mouse(True)
        self.current_scene.update()
        #mettre à jour fps si modif dans setting
        self.fps = menu.fps
        self.debug_main()

    def draw(self):
        """
        Dessine la scène actuelle.
        """
        self.current_scene.draw()


App()
