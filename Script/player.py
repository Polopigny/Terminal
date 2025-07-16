import pyxel
import debug
import time_game

class Player:
    def __init__(self):
        self.x = 256 // 2
        self.y = 256 // 2

        self.base_speed = 1
        self.debug_speed = 4
        self.speed = self.base_speed

        self.base_life = 3
        self.life = self.base_life

        self.width = 16
        self.height = 16
        self.color = pyxel.COLOR_RED

        self.debug_text = ""
        self.debug_text_x = 0
        self.debug_text_y = 0

        self.attack_range = 30
        self.weapon = "sword" # "bombe" "arc"

        self.sword_distance2player=15
        self.is_right=True

        self.tileset = 0
        self.tileset_x_base = 0
        self.tileset_x = self.tileset_x_base
        self.tileset_y_base = 16
        self.tileset_y = self.tileset_y_base
        self.tileset_x_kill = 80
        self.tileset_y_kill = 32

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
    


    def update_debug_info(self):
        self.debug_text_x = self.x - 12
        self.debug_text_y = self.y - 8
        self.debug_text = f"{int(self.x)}, {int(self.y)}"

    def update_camera_and_window(self):
        debug.windowX = self.x
        debug.windowY = self.y

    def update(self):
        self.move()
        self.scale = 1
        self.anim_mouvement = False
        self.move()
        self.update_camera_and_window()
        if debug.debug_mode:
            self.update_debug_info()
        self.animation_mouvement()
        self.animation_kill()

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


    def draw(self):
        pyxel.blt(self.x, self.y, self.tileset, self.tileset_x, self.tileset_y, self.width * self.side, self.height, colkey = 2, scale=self.scale)
        

        if pyxel.btn(pyxel.KEY_SPACE):
            if self.is_right:
                pyxel.blt(self.x+self.sword_distance2player, self.y, 0, 0, 64, 16, 16, colkey=2)
            else : pyxel.blt(self.x-self.sword_distance2player, self.y, 0, 0, 64, 16, 16, colkey=2)



        pyxel.text(self.x+88, self.y - 118, f"live = {self.life}", pyxel.COLOR_WHITE)

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
