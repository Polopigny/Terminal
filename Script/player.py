import pyxel
import debug

class Player:
    def __init__(self):
        self.x = 256//2
        self.y = 256//2
        self.base_speed = 1
        self.speed = 1
        self.base_life = 3
        self.life = 3
        self.width = 8
        self.height = 16
        self.color = pyxel.COLOR_RED
        #movements
        self.SPEED_x=SPEED_x
        self.SPEED_y=SPEED_y
        self.POS_j_x=POS_j_x
        self.POS_j_y=POS_j_y
        self.DIRECTIOn_S_x=DIRECTIOn_S_x
        self.DIRECTIOn_S_y=DIRECTIOn_S_y
        #debug
        self.debug_text_x = 0 
        self.debug_text_y = 0
        self.debug_text = ""
        self.debug_speed = 0

    def move(self):
        self.speed = self.debug_speed if debug.debug_mode else self.base_speed

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
    
    def debug(self):
        #mettre text pos(x,y) au dessus du joueur
        self.debug_text_x = self.x - 12
        self.debug_text_y = self.y - 8
        self.debug_text = str(self.x) + " , " + str(self.y)

        #booster vitesse
        self.debug_speed = 4

    def update(self):
        self.move()
        if debug.debug_mode == True:
            self.debug()

    #methods for movements
    def go_up(self, SPEED_y, POS_j_y, DIRECTION_S_x, DIRECTION_S_y):
        if POS_j_y>18:
            if pyxel.btn(pyxel.KEY_UP):
                SPEED_y=-4
                POS_j_y+=SPEED_y
                DIRECTION_S_y=-25
                DIRECCTION_S_x=0
        
    def go_down(self, SPEED_y, POS_j_y, DIRECTION_S_x, DIRECTION_S_y):
        if POS_j_y<734:
            if pyxel.btn(pyxel.KEY_DOWN):
                SPEED_y=4
                POS_j_y+=SPEED_y
                DIRECTION_S_y=30
                DIRECCTION_S_x=0
        
    def go_left(self, SPEED_x, POS_j_x, DIRECTION_S_x, DIRECTION_S_y):
        if POS_j_y>18:
            if pyxel.btn(pyxel.KEY_LEFT):
                SPEED_x=-4
                POS_j_x+=SPEED_x
                DIRECTION_S_y=0
                DIRECCTION_S_x=-25
        
  def go_right(self, SPEED_x, POS_j_x, DIRECTION_S_x, DIRECTION_S_y):
      if POS_j_y<734:
          if pyxel.btn(pyxel.KEY_RIGHT):
              SPEED_x=4
              POS_j_x+=SPEED_x
              DIRECTION_S_y=0
              DIRECCTION_S_x=30

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

        if debug.debug_mode == True:
            pyxel.text(self.debug_text_x,self.debug_text_y,self.debug_text,pyxel.COLOR_WHITE)

player = Player()
