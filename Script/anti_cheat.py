import debug
from enemyVagueManager import VagueManager_var
from player import player
import time_game

cheat = False

game_start_check = False

scene = "menu"


def debug_cheat():
    global cheat
    if debug.debug_mode == True:
        cheat = True
        print(f"player as cheat : {time_game.time_game_seconds_x} (sc) whit the use of debug mod : {debug.debug_mode}, cheat :  {cheat}")

def player_cheat_one_time():
    global cheat
    if game_start_check == False:
        if player.base_life != player.life:
            cheat = True
            print(f"player as cheat : {time_game.time_game_seconds_x} (sc) whit the use of life change : {player.life}, cheat :  {cheat}")
        if player.base_speed != player.speed:
            cheat = True
            print(f"player as cheat : {time_game.time_game_seconds_x} (sc) whit the use of speed change: {player.speed}, cheat :  {cheat}")

def player_cheat():
    global cheat
    if player.invincibility == True:
        cheat = True
        print(f"player as cheat : {time_game.time_game_seconds_x} (sc) whit the use of invincibility : {player.invincibility}, cheat :  {cheat}")

def Vague_cheat_one_time():
    global cheat
    if game_start_check == False:
        if VagueManager_var.current_wave_base != VagueManager_var.current_wave:
            cheat = True
            print(f"player as cheat : {time_game.time_game_seconds_x} (sc) whit the use of vague change : {VagueManager_var.current_wave}, cheat :  {cheat}")

def game_start_check_update():
    global game_start_check
    if scene == "game":
        if game_start_check == False:
            game_start_check = True


def cheat_update():
    game_start_check_update()
    player_cheat()
    debug_cheat()
    player_cheat_one_time()
    Vague_cheat_one_time()
    print(cheat)

def reset():
    global cheat, game_start_check
    cheat = False
    game_start_check = False