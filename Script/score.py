import pyxel
import debug
import player


class Score:
    def __init__(self):
        '''
        Initialiser les variables nécessaires au calcul des points.
        '''
        self._score          = 0
        self._killed_enemies = 0
        self.debug_pos = 256 // 2 - 10

    def update_killed_enemies_count(self):
        '''
        Compter le nombre d'ennemis tuer.
        '''
        self._killed_enemies += 1

    def get_killed_enemies_count(self):
        return self._killed_enemies
    
    def update_score(self):
        '''
        Calculer le score.
        '''
        self._score = self._killed_enemies * 10

    def get_score(self):
        return self._score
    
    def draw(self):
        '''
        Afficher le score.
        '''
        pyxel.text(player.player.x - self.debug_pos,
                   player.player.y - self.debug_pos,
                   f"Score : {self._score}",
                   pyxel.COLOR_WHITE)
        if debug.debug_mode == True:
            pyxel.text(player.player.x - self.debug_pos,
                       player.player.y - self.debug_pos + 7,
                       f"Killed enemies: {self._killed_enemies}", pyxel.COLOR_YELLOW)   
    def reset(self):
        self._score          = 0
        self._killed_enemies = 0

score = Score()