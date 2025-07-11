import pyxel
import player
import debug
import menu

list_enemi_global = []
list_projectile_global = []
nb_enemi_global = 0 # attention +1 pour normal(mini boss +5) 
                    #           +2 pour mage(mini boss + 1)



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

        self.tileset = 0
        self.tileset_x = 64
        self.tileset_y = 16

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
    
    def update_player_interaction(self):
        if (self.distance_to_player <= self.dmin_player_attack) and self.colldown_over:
            player.player.life -=1
            self.start_kill_colldown = True
            if debug.debug_mode == True:
                print(f"Player HIT by {self.__class__} n°:{self.index},\nremaining life={player.player.life}")
        
    
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
        if self.distance_to_player >= self.dmin_player_attack-2:
            self.x += (self.speed * self.dx_player / self.distance_to_player) * debug.time_speed
            self.y += (self.speed * self.dy_player / self.distance_to_player) * debug.time_speed

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

        if self.start_kill_colldown == True:
            self.kill_cooldown(0)

    def draw(self):
        pyxel.blt(self.x, self.y, self.tileset, self.tileset_x, self.tileset_y, self.width, self.height, colkey = 2)

poid_enemi_mage = 2
class Enemi_mage(Enemi):
    def __init__(self,coo_x,coo_y):
        super().__init__(coo_x,coo_y)

        self.base_speed = 0.3
        self.base_life = 2

        self.tileset = 0
        self.tileset_x = 128
        self.tileset_y = 16

        self.dmin_player_attack = 100

        self.time_kill_colldown = 5
    
    def update_player_interaction(self):
        if (self.distance_to_player <= self.dmin_player_attack) and self.colldown_over:
            list_projectile_global.append(Enemi_mage_projectile(self,self.x,self.y))
            mise_jour_liste_projectile()
            self.start_kill_colldown = True
            if debug.debug_mode == True:
                print(f"enemi : {self.__class__} shot projectile")
    
class Enemi_mage_projectile:
    def __init__(self,Enemi_mage_id,coo_x,coo_y):
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

        self.Enemi_mage_id = Enemi_mage_id

        self.dx = player.player.x - self.x
        self.dy = player.player.y - self.y
        self.distance = (self.dx**2 + self.dy**2) ** 0.5

    def move(self):
        if self.distance_to_player >= 1:
            self.x += (self.speed * self.dx / self.distance) * debug.time_speed
            self.y += (self.speed * self.dy / self.distance) * debug.time_speed

    def update_distance_to_player(self):
        self.dx_player = player.player.x - self.x
        self.dy_player = player.player.y - self.y

        self.distance_to_player = (self.dx_player**2 + self.dy_player**2) ** 0.5
    
    def update_player_interaction(self):
        if self.distance_to_player <= 4:
            player.player.life -=1
            if debug.debug_mode == True:
                print(f"Player HIT by {self.__class__} shoot by {self.Enemi_mage_id.__class__} index :{self.Enemi_mage_id.index},\nremaining life={player.player.life}")
                print(f"Projectile index : {self.index} going to be remove because it just touch player")
            list_projectile_global.remove(self)
    
    def autodestruction(self):
        if self.distance_to_player >= 200 and self in list_projectile_global:
            if debug.debug_mode == True:
                print(f"Projectile index : {self.index} going to be remove due to excessive distance to player:{self.distance_to_player}")
            list_projectile_global.remove(self)
       
    def update(self):
        self.update_distance_to_player()
        self.update_player_interaction()
        self.move()
        self.autodestruction()

    def draw(self):
        pyxel.blt(self.x, self.y, self.tileset, self.tileset_x, self.tileset_y, self.width, self.height, colkey = 2)



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

    if pyxel.btnp(pyxel.KEY_SPACE) and len(list_enemi_global)>0:
        list_enemi_global.pop()
        nb_enemi_global -= 1
        menu.game._score.update_killed_enemies_count()

def reset_enemi_list():
    global list_enemi_global, nb_enemi_global, list_projectile_global
    list_enemi_global = []
    list_projectile_global = []
    nb_enemi_global = 0