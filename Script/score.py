import pyxel
import enemi
import debug
import menu


class Score:

    def __init__(self):
        '''
        Initialiser les variables nécessaires au calcul des points.
        '''
        self.score=0
        self.enemy_killed=0

    def setCountEnemyKilled(self):
        '''
        Compter le nombre d'ennemis tuer.
        '''
        if pyxel.btnp(pyxel.KEY_SPACE) and len(menu.game.getEnemyList())>0 and menu.game.setCollisionStatus():
            self.enemy_killed+=1

    def getCountEnemyKilled(self):
        return self.enemy_killed
    
    def setScore(self):
        '''
        Calculer le score.
        '''
        self.score=self.getCountEnemyKilled()*10

    def getScore(self):
        return self.score
    
    def draw_local(self):
        '''
        Afficher le score.
        '''
        pyxel.text(10,10,"Score :"+ str(self.getScore()),pyxel.COLOR_WHITE)

    def setDebugMode(self):
        if debug.debug_mode == True:
            print("Ennemis tués : ",self.getCountEnemyKilled())

    