import pyxel
import player
import debug
from score import score
import time_game

list_enemi_global = []
list_projectile_global = []
nb_enemi_global = 0 # attention +1 pour normal(mini boss +5) 
                    #           +2 pour mage(mini boss + 1)





list_enemi_kill_debug = []



#default enemi : squeletton
poid_enemi = 10
class Enemi:
    def __init__(self,coo_x,coo_y):
        self.x = coo_x
        self.y = coo_y
        self.base_speed = 1
        self.speed = 1
        self.base_life = 1
        self.life = 1
        self.width = 16
        self.height = 16

        self.can_move = True
        self.can_be_kill = False

        self.tileset = 0
        self.tileset_x_base = 64
        self.tileset_x = self.tileset_x_base
        self.tileset_y_base = 16
        self.tileset_y = self.tileset_y_base
        self.tileset_x_kill = 96
        self.tileset_y_kill = 32

        self.anim_mouvement = True
        self.anim_i = 0
        self.anim_old_time = 0
        self.anim_speed = 5  # en frames
        self.nb_frame_for_anim = 4
        self.nb_anim_kill = 10
        self.anim_i_kill = 0
        self.nb_scale_kill = 1/self.nb_anim_kill
        self.anim_kill = False
        self.anim_kill_speed = 4

        self.side = 1

        self.scale = pyxel.rndf(1,1.3)

        self.dmin_player_attack = 3
        self.distance_to_player = 0
        self.distance_to_closer_enemi = 0
        self.id_to_closer_enemi = 0
        self.index = 0

        self.repulse_dx = 0
        self.repulse_dy = 0
        self.dx_closer_enemi = 0
        self.dy_closer_enemi = 0

        self.time_kill_colldown = 2
        self.colldown_over = True
        self.start_kill_colldown = False
        self.time_cooldown = 0

    def update_distance_to_player(self):
        self.dx_player = player.player.x - self.x
        self.dy_player = player.player.y - self.y

        self.distance_to_player = (self.dx_player**2 + self.dy_player**2) ** 0.5
    
    def update_side(self):
        self.side = -1 if self.dx_player < 0 else 1

    def update_life(self):
        global nb_enemi_global
        if self.life <= 0:
            nb_enemi_global -= 1
            score.update_killed_enemies_count()
            list_enemi_kill_debug.append(self)
            list_enemi_kill_debug.append(time_game.time_game_seconds_x)
            list_enemi_global.remove(self)
    
    def update_player_interaction(self):
        #attack du monstre
        if (self.distance_to_player <= self.dmin_player_attack) and self.colldown_over:
            player.player.life -=1
            player.player.anim_kill_old_time = pyxel.frame_count
            player.player.anim_kill = True
            self.start_kill_colldown = True
            if debug.debug_mode == True:
                print(f"Player HIT by {self.__class__} n°:{self.index},\nremaining life={player.player.life}")
        
        #attack du joueur
        if pyxel.btnp(pyxel.KEY_SPACE) and len(list_enemi_global)>0 and player.player.attack_range >= self.distance_to_player:
            self.anim_kill = True
    
    def kill_by_player(self):
        if self.can_be_kill == True:
                self.life -= 1
            
            
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
        if self.distance_to_player >= self.dmin_player_attack-2 and self.can_move == True:
            self.x += (self.speed * self.dx_player / self.distance_to_player) * time_game.time_speed
            self.y += (self.speed * self.dy_player / self.distance_to_player) * time_game.time_speed

    def repulse(self):
        push_force = 0.5
        if abs(self.dx_closer_enemi) != abs(self.dx_player) and abs(self.dy_closer_enemi) != abs(self.dy_player):
            if abs(self.dx_closer_enemi)< self.width : 
                self.x -= self.repulse_dx * push_force
            if abs(self.dy_closer_enemi) < self.height:
                self.y -= self.repulse_dy * push_force

    def kill_cooldown(self,start_time):
        if self.colldown_over == True:
            self.time_cooldown = start_time
            self.colldown_over = False

        if self.colldown_over == False:
            if pyxel.frame_count % 30 == 0:
                self.time_cooldown += 1

        if self.time_kill_colldown == self.time_cooldown:
            self.colldown_over = True
            self.start_kill_colldown = False

    def update(self):
        self.index = list_enemi_global.index(self)
        self.update_distance_to_player()
        self.move()
        self.update_closer_enemi()
        self.repulse()
        self.update_player_interaction()
        self.kill_by_player()
        self.update_life()

        if self.start_kill_colldown == True:
            self.kill_cooldown(0)

        self.animation_mouvement()
        self.animation_kill()
        self.update_side()

    def animation_mouvement(self):
        if self.anim_mouvement == True:
            if pyxel.frame_count >= self.anim_old_time + self.anim_speed:
                self.tileset_x += 16
                self.anim_old_time = pyxel.frame_count
                self.anim_i += 1
                if self.anim_i >= self.nb_frame_for_anim:
                    self.anim_i = 0
                    self.tileset_x = self.tileset_x_base
    
    def animation_kill(self):
        if self.anim_kill:
            self.anim_mouvement = False
            self.can_move = False

            if self.anim_i_kill % self.anim_kill_speed == 0:
                self.tileset_x = self.tileset_x_base
                self.tileset_y = self.tileset_y_base
            else:
                self.tileset_x = self.tileset_x_kill
                self.tileset_y = self.tileset_y_kill

            self.scale = max(0.1, self.scale - self.nb_scale_kill)  # évite scale < 0
            self.anim_i_kill += 1

            if self.anim_i_kill >= self.nb_anim_kill:
                self.can_be_kill = True
                self.anim_kill = False

        
    def draw(self):
        pyxel.blt(self.x, self.y, self.tileset, self.tileset_x, self.tileset_y, self.width * self.side, self.height, colkey = 2, scale=self.scale)

poid_enemi_mage = 2
class Enemi_mage(Enemi):
    def __init__(self,coo_x,coo_y):
        super().__init__(coo_x,coo_y)

        self.base_speed = 0.3
        self.base_life = 2

        self.tileset_x_base = 128
        self.tileset_y_base = 16
        self.tileset_x = self.tileset_x_base
        self.tileset_y = self.tileset_y_base
        self.tileset_x_kill = 112

        self.anim_mouvement = False

        self.dmin_player_attack = 100

        self.time_kill_colldown = 5
    
    def update_player_interaction(self):
        #attack du monstre
        if (self.distance_to_player <= self.dmin_player_attack) and self.colldown_over:
            list_projectile_global.append(Enemi_mage_projectile(self,self.x,self.y))
            mise_jour_liste_projectile()
            self.start_kill_colldown = True
            if debug.debug_mode == True:
                print(f"enemi : {self.__class__} shot projectile")

        #attack du joueur
        if pyxel.btnp(pyxel.KEY_SPACE) and len(list_enemi_global)>0 and player.player.attack_range >= self.distance_to_player:
            self.anim_kill = True
            
    def update_side(self):
        self.side = 1 if self.dx_player < 0 else -1
    
class Enemi_mage_projectile:
    def __init__(self,Enemi_mage_parent,coo_x,coo_y):
        self.x = coo_x
        self.y = coo_y

        self.speed = 3

        self.index = 0
        
        self.tileset = 0
        self.tileset_x = 112
        self.tileset_y = 80
        self.width = 16
        self.height = 16

        self.distance_to_player = 0

        self.rotation = 0

        self.Enemi_mage_parent = Enemi_mage_parent

        self.scale = self.Enemi_mage_parent.scale

        self.nb_time_1 = 1
        self.nb_time =0

        self.dx = player.player.x - self.x
        self.dy = player.player.y - self.y
        self.distance = (self.dx**2 + self.dy**2) ** 0.5

        self.dx_player = 9999
        self.dy_player = 9999
        self.distance_to_player = 99999

    def move(self):
        if self.distance_to_player >= 1:
            self.x += (self.speed * self.dx / self.distance) * time_game.time_speed
            self.y += (self.speed * self.dy / self.distance) * time_game.time_speed

    def update_distance_to_player(self):
        self.dx_player = player.player.x - self.x
        self.dy_player = player.player.y - self.y

        self.distance_to_player = (self.dx_player**2 + self.dy_player**2) ** 0.5
    
    def update_player_interaction(self):
        if self.distance_to_player <= 4:
            player.player.anim_kill_old_time = pyxel.frame_count
            player.player.anim_kill = True
            if debug.debug_mode == True:
                print(f"Player HIT by {self.__class__} shoot by {self.Enemi_mage_parent.__class__} index :{self.Enemi_mage_parent.index},\nremaining life={player.player.life}")
                print(f"Projectile index : {self.index} going to be remove because it just touch player")
            list_projectile_global.remove(self)
            player.player.life -=1
    
    def autodestruction(self):
        if self.distance_to_player >= 200 and self in list_projectile_global:
            if debug.debug_mode == True:
                print(f"Projectile index : {self.index} going to be remove due to excessive distance to player:{self.distance_to_player}")
            list_projectile_global.remove(self)

    def update_rotation(self):
        angle = pyxel.atan2(self.dy_player, self.dx_player)  # angle en degrés
        self.rotation = angle % 360

    def update_nb_time(self):
        if self.nb_time <= self.nb_time_1:
            self.update_rotation()
            self.nb_time += 1
       
    def update(self):
        self.update_nb_time()
        self.update_distance_to_player()
        self.update_player_interaction()
        self.move()
        self.autodestruction()

    def draw(self):
        pyxel.blt(self.x, self.y, self.tileset, self.tileset_x, self.tileset_y, self.width, self.height, colkey = 2, rotate=self.rotation, scale=self.scale)



list_type_enemi = (
    [Enemi] * poid_enemi +
    [Enemi_mage] * poid_enemi_mage
)

    
def choose_enemi():
    x = pyxel.rndi(0,len(list_type_enemi)-1)

    return list_type_enemi[x]
        

def creation():
    global list_enemi_global,nb_enemi_global
    
    spwan_radius_protection = 150

    max_pos_x_spwan = 736  - 8
    max_pos_y_spwan = 736  - 16
    min_pos_x_spwan = 16  + 8
    min_pos_y_spwan = 16  + 16

    #trouver une position pour spwan l'enemi
    distance = 0

    while distance < spwan_radius_protection :

        pos_e_x = pyxel.rndi(min_pos_x_spwan,max_pos_x_spwan)
        pos_e_y = pyxel.rndi(min_pos_y_spwan,max_pos_y_spwan)

        distance = abs(pyxel.sqrt((pos_e_x - player.player.x)**2 + (pos_e_y - player.player.y)**2))


    enemi_to_spwan = choose_enemi()
    list_enemi_global.append(enemi_to_spwan(pos_e_x,pos_e_y))
    nb_enemi_global += 1
    if debug.debug_mode == True:
        print(f"new enemy : {enemi_to_spwan.__name__} at x={pos_e_x}, y={pos_e_y}")

def mise_jour_liste_enemi():
    for i in range(len(list_enemi_global)):
        for ii in range(len(list_enemi_global)-1-i):
            if list_enemi_global[ii].distance_to_player < list_enemi_global[ii+1].distance_to_player:
                list_enemi_global[ii],list_enemi_global[ii+1]=list_enemi_global[ii+1],list_enemi_global[ii]

def mise_jour_liste_projectile():
    for i, proj in enumerate(list_projectile_global):
        proj.index = i



def debug_enemi():  
    if debug.debug_mode == True:
        
        for e in list_enemi_global:
            pyxel.text(e.x - 7, e.y - 15, f"index:{e.index}", pyxel.COLOR_RED)
            pyxel.text(e.x - 15, e.y - 7, f"closer e:{e.id_to_closer_enemi}", pyxel.COLOR_RED)

        for e in list_projectile_global:
            pyxel.text(e.x - 7, e.y - 15, f"index:{e.index}", pyxel.COLOR_RED)

        pyxel.text(player.player.x -118, player.player.y -125, f"enemies:{len(list_enemi_global)}", pyxel.COLOR_YELLOW)
        pyxel.text(player.player.x -118, player.player.y -103, f"projectiles:{len(list_projectile_global)}", pyxel.COLOR_YELLOW)

def update_global():
    global nb_enemi_global

    mise_jour_liste_enemi()

def reset_enemi_list():
    global list_enemi_global, nb_enemi_global, list_projectile_global, list_enemi_kill_debug
    list_enemi_global = []
    list_projectile_global = []
    nb_enemi_global = 0
    list_enemi_kill_debug = []