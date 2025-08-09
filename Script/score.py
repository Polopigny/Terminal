import pyxel
import debug
import player
import enemi
import time_game


class Score:
    def __init__(self):
        '''
        Initialiser les variables nécessaires au calcul des points.
        '''
        self._killed_enemies=0
        self._score=0
        self.debug_pos = 256 // 2 - 10      
    
    def update_score(self, enemy_score):
        ''' 
        Calculer le score.
        '''
        self._score += enemy_score
        self._killed_enemies += 1

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
                       f"Killed enemies: {self._killed_enemies=}", pyxel.COLOR_YELLOW)   
    def reset(self):
        self._score          = 0
        self._killed_enemies = 0



score = Score()