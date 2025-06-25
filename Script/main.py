import pyxel
import menu

class App:
    def __init__(self):
        """
        Initialise la fenêtre Pyxel, charge les ressources et démarre le jeu.
        """
        pyxel.init(256, 256, title="Terminal V1.1", fps=30)
        pyxel.load("../Template/2.pyxres")

        self.current_scene = menu.menu  # Scène actuelle : menu par défaut
        pyxel.run(self.update, self.draw)

    def switch_scene(self):
        """
        Change la scène selon l'état du menu.
        """
        match menu.menu_state:
            case "menu":
                self.current_scene = menu.menu
                pyxel.camera()
            case "game":
                self.current_scene = menu.game
            # possibilité d'ajouter "setting", "end_game" plus tard

    def update(self):
        """
        Met à jour la scène actuelle et active la souris.
        """
        self.switch_scene()
        pyxel.mouse(True)
        self.current_scene.update()

    def draw(self):
        """
        Dessine la scène actuelle.
        """
        self.current_scene.draw()


App()

