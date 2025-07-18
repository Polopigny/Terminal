import pyxel
import debug
import time_game
class Player:
    def __init__(self):
        self.x = 256 // 2
        self.y = 256 // 2
        self.base_speed = 2
        self.debug_speed = 4
        self.speed = self.base_speed
        self.base_life = 3
        self.life = self.base_life
        self.invincibility = False
        self.width = 16
        self.height = 16
        self.color = pyxel.COLOR_RED

        self.debug_text = ""
        self.debug_text_x = 0
        self.debug_text_y = 0

        self.attack_range = 40
        self.weapon = "sword" # "bombe" "arc"
        self.is_right=True

        self.tileset = 0
        self.tileset_x_base = 0
        self.tileset_x = self.tileset_x_base
        self.tileset_y_base = 16
        self.tileset_y = self.tileset_y_base
        self.tileset_x_kill = 80
        self.tileset_y_kill = 32
        self.tileset_x_life = 112
        self.tileset_y_life = 48

        self.anim_mouvement = False
        self.anim_i = 0
        self.anim_old_time = 0
        self.anim_speed = 2  # en frames
        self.nb_frame_for_anim = 4

        self.anim_kill = False
        self.nb_scale_kill = 0.5
        self.anim_kill_speed = 5
        self.anim_kill_old_time = 0

        self.side = 1

        self.hit_counter = 0

        self.dx_enemi = 0 #mise à jour dans l'enemi
        self.dy_enemi = 0 #mise à jour dans l'enemi
        self.distance_enemi = 0
        self.rotation_item = 0      
        self.item_x = 0
        self.item_y = 0
        self.item_tileset = 0
        self.item_tileset_x = 0
        self.item_tileset_y = 64
        self.item_scale = 1
        self.anim_attack = False
        self.anim_attack_speed = 2
        self.anim_attack_old_time = 0
        self.sword_distance2player_base = 15
        self.sword_distance2player = self.sword_distance2player_base    

    def move(self):
        self.speed = self.debug_speed if debug.debug_mode else self.base_speed

        if pyxel.btn(pyxel.KEY_UP) and self.y>18:
            self.y -= self.speed * time_game.time_speed
            self.anim_mouvement = True
        if pyxel.btn(pyxel.KEY_DOWN) and self.y<734:
            self.y += self.speed * time_game.time_speed
            self.anim_mouvement = True
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x<734:
            self.x += self.speed * time_game.time_speed
            self.is_right=True
            self.side = 1
            self.anim_mouvement = True
        if pyxel.btn(pyxel.KEY_LEFT) and self.x>18:
            self.x -= self.speed * time_game.time_speed
            self.is_right=False
            self.side = -1
            self.anim_mouvement = True
    
    def invincibility_update(self):
        if self.invincibility == True:
            self.life = self.base_life

    def update_debug_info(self):
        self.debug_text_x = self.x - 12
        self.debug_text_y = self.y - 8
        self.debug_text = f"{int(self.x)}, {int(self.y)}"

    def update_camera_and_window(self):
        debug.windowX = self.x
        debug.windowY = self.y

    def update(self):
        self.invincibility_update()
        self.scale = 1
        self.anim_mouvement = False
        self.move()
        self.attack()
        self.animation_attack()
        self.update_camera_and_window()
        if debug.debug_mode:
            self.update_debug_info()
        self.animation_mouvement()
        self.animation_kill()  

    def attack(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            self.anim_attack_old_time = pyxel.frame_count
            self.anim_attack = True

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
            if self.anim_kill_old_time + self.anim_kill_speed >= pyxel.frame_count:
                self.tileset_x = self.tileset_x_kill
                self.tileset_y = self.tileset_y_kill
                self.scale =self.scale + self.nb_scale_kill
            else:
                self.anim_kill = False
                self.tileset_x = self.tileset_x_base
                self.tileset_y = self.tileset_y_base

    def animation_attack(self):
        if self.anim_attack:
            self.distance_enemi = (self.dx_enemi**2 + self.dy_enemi**2) ** 0.5
            
            if self.distance_enemi > self.attack_range + 20:
                
                if self.anim_attack_old_time + self.anim_attack_speed >= pyxel.frame_count:
                    self.side
                    angle = pyxel.atan2(0,self.side)
                    self.item_x = self.x + self.sword_distance2player * pyxel.cos(angle)
                    self.item_y = self.y + self.sword_distance2player * pyxel.sin(angle)
                    self.rotation_item = angle
                else:
                    self.anim_attack = False

            else:
                #1/ trouver l'angle de rotation de l'item
                angle = pyxel.atan2(self.dy_enemi, self.dx_enemi * self.side)
                #2/ positionement de l'épée par rapport au joueur
                self.item_x = self.x + self.sword_distance2player * pyxel.cos(angle)
                self.item_y = self.y + self.sword_distance2player * pyxel.sin(angle)
                self.rotation_item = angle
                
                if self.anim_attack_old_time + self.anim_attack_speed >= pyxel.frame_count:
                    if self.sword_distance2player <= self.attack_range - self.sword_distance2player:
                        self.sword_distance2player += self.anim_attack_speed
                        
                else:
                    self.anim_attack = False
                    self.sword_distance2player = self.sword_distance2player_base
            
            
    def draw_life(self):
        x = 15
        for i in range(self.life):
            pyxel.blt(self.x + 70 + x * i, self.y - 122, self.tileset, self.tileset_x_life, self.tileset_y_life, self.width, self.height, colkey = 2, scale=1)
        if debug.debug_mode == True:
            pyxel.text(self.x + 100, self.y -110, f"life:{self.life}",pyxel.COLOR_WHITE)
    
    def draw(self):
        pyxel.blt(self.x, self.y, self.tileset, self.tileset_x, self.tileset_y, self.width * self.side, self.height, colkey = 2, scale=self.scale)
        
        if self.anim_attack == True:
            pyxel.blt(self.item_x, self.item_y, self.item_tileset, self.item_tileset_x, self.item_tileset_y, 16, 16 * self.side, colkey=2, scale=self.item_scale, rotate=self.rotation_item)

        self.draw_life()        
                
        if debug.debug_mode:
            pyxel.text(self.debug_text_x, self.debug_text_y, self.debug_text, pyxel.COLOR_WHITE)
            
    def reset(self):
        self.x = 256 // 2
        self.y = 256 // 2
        self.debug_speed = 4
        self.speed = self.base_speed
        self.life = self.base_life
        self.width = 16
        self.height = 16
        self.color = pyxel.COLOR_RED
        self.debug_text = ""
        self.debug_text_x = 0
        self.debug_text_y = 0
        
player = Player()