import pyxel
from player import player
import debug

list_enemi_global = []

class Enemi:
    def __init__(self,coo_x,coo_y):
        self.x = coo_x
        self.y = coo_y
        self.base_speed = 1
        self.speed = 1
        self.base_life = 1
        self.life = 1
        self.width = 8
        self.height = 16
        self.color = pyxel.COLOR_PURPLE

        self.distance_to_player = 0
        self.distance_to_closer_enemi = 0
        self.id_to_closer_enemi = 0
        self.index = 0

        self.repulse_dx = 0
        self.repulse_dy = 0
        self.dx_closer_enemi = 0
        self.dy_closer_enemi = 0

    def update_distance_to_player(self):
        self.dx_player = player.x - self.x
        self.dy_player = player.y - self.y

        self.distance_to_player = (self.dx_player**2 + self.dy_player**2) ** 0.5
    
    def update_closer_enemi(self):
        dx = 0
        dy = 0
        d_min = 99999999999
        for e in list_enemi_global:
            if e.x != self.x and e.y != self.y:
                dx = e.x - self.x
                dy = e.y - self.y

                self.distance_to_closer_enemi = (dx**2 + dy**2) ** 0.5

                if self.distance_to_closer_enemi < d_min :
                    d_min = self.distance_to_closer_enemi
                    self.id_to_closer_enemi = e.index
                    self.repulse_dx = dx / self.distance_to_closer_enemi  
                    self.repulse_dy = dy / self.distance_to_closer_enemi
                    self.dy_closer_enemi = dy
                    self.dx_closer_enemi = dx
        
        self.distance_to_closer_enemi = d_min
    
    def move(self):
        if self.distance_to_player >= 2:
            self.x += (self.speed * self.dx_player / self.distance_to_player) * debug.time
            self.y += (self.speed * self.dy_player / self.distance_to_player) * debug.time

    def repulse(self):
        push_force = 0.5
        if abs(self.dx_closer_enemi) != abs(self.dx_player) and abs(self.dy_closer_enemi) != abs(self.dy_player):
            if abs(self.dx_closer_enemi)< self.width : 
                self.x -= self.repulse_dx * push_force
            if abs(self.dy_closer_enemi) < self.height:
                self.y -= self.repulse_dy * push_force

    def update(self):
        self.index = list_enemi_global.index(self)
        self.update_distance_to_player()
        self.move()
        self.update_closer_enemi()
        self.repulse()

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

def creation():

    spwan_radius_protection = 50

    max_pos_x_spwan = 250  - 8
    max_pos_y_spwan = 250  - 16
    min_pos_x_spwan = 10  + 8
    min_pos_y_spwan = 10  + 16

    #trouver une position pour spwan l'enemi
    distance = 0

    while distance < spwan_radius_protection :

        pos_e_x = pyxel.rndi(min_pos_x_spwan,max_pos_x_spwan)
        pos_e_y = pyxel.rndi(min_pos_y_spwan,max_pos_y_spwan)

        distance = abs(pyxel.sqrt((pos_e_x - player.x)**2 + (pos_e_y - player.y)**2))

    list_enemi_global.append(Enemi(pos_e_x, pos_e_y))

def mise_jour_liste_enemi():
    for i in range(len(list_enemi_global)):
        for ii in range(len(list_enemi_global)-1-i):
            if list_enemi_global[ii].distance_to_player < list_enemi_global[ii+1].distance_to_player:
                list_enemi_global[ii],list_enemi_global[ii+1]=list_enemi_global[ii+1],list_enemi_global[ii]


def debug_enemi():
    if debug.debug_mode == True:
        
        for e in list_enemi_global:
            pyxel.text(e.x - 7, e.y - 15, f"index:{e.index}", pyxel.COLOR_RED)
            pyxel.text(e.x - 15, e.y - 7, f"closer e:{e.id_to_closer_enemi}", pyxel.COLOR_RED)


        pyxel.text(10, 5, f"nb enemi:{len(list_enemi_global)}", pyxel.COLOR_YELLOW)

def update_global():
    mise_jour_liste_enemi()
    if pyxel.btnp(pyxel.KEY_U):
        creation()
    if pyxel.btnp(pyxel.KEY_SPACE) and len(list_enemi_global)>0:
        list_enemi_global.pop()