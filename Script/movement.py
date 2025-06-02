'''Class file for movement in game. Movement only concern the sprite that the player has to move.
Movements allowed : go left, go right, go backward, go forward in 2D and press space while pressing movement key to degained your sword
I changed the name of the variable because we don t have anymore shot in game but a sword so direction_x became DIRECCTION_S_x and direction_y became DIRECCTION_S_y.'''

import pyxel as pyxel
class Movement:
  def __init__(self, SPPED_x, SPEED_y, POS_j_x, POS_j_y, DIRECTION_S_x, DIRECTION_S_y) :
    self.SPEED_x=SPEED_x
    self.SPEED_y=SPEED_y
    self.POS_j_x=POS_j_x
    self.POS_j_y=POS_j_y
    self.DIRECTIOn_S_x=DIRECTIOn_S_x
    self.DIRECTIOn_S_y=DIRECTIOn_S_y

  
  def key_up(self, SPEED_y, POS_j_y, DIRECTION_S_x, DIRECTION_S_y):
    if POS_j_y>18:
      if pyxel.btn(pyxel.KEY_UP):
        SPEED_y=-4
        POS_j_y+=SPEED_y
        DIRECTION_S_y=-25
        DIRECCTION_S_x=0
        
  def key_down(self, SPEED_y, POS_j_y, DIRECTION_S_x, DIRECTION_S_y):
    if POS_j_y<734:
      if pyxel.btn(pyxel.KEY_DOWN):
        SPEED_y=4
        POS_j_y+=SPEED_y
        DIRECTION_S_y=30
        DIRECCTION_S_x=0
        
  def key_left(self, SPEED_x, POS_j_x, DIRECTION_S_x, DIRECTION_S_y):
    if POS_j_y>18:
      if pyxel.btn(pyxel.KEY_LEFT):
        SPEED_x=-4
        POS_j_x+=SPEED_x
        DIRECTION_S_y=0
        DIRECCTION_S_x=-25
        
  def key_right(self, SPEED_x, POS_j_x, DIRECTION_S_x, DIRECTION_S_y):
    if POS_j_y<734:
      if pyxel.btn(pyxel.KEY_RIGHT):
        SPEED_x=4
        POS_j_x+=SPEED_x
        DIRECTION_S_y=0
        DIRECCTION_S_x=30
 
