import pyxel
import debug

time_speed = 1
fps = 30

time_game_seconds = 0
time_game_seconds_x = 0
time_game_min = 0
time_game_frame = 0
time_game_x = 0

runtime_seconds = 0
runtime_seconds_x = 0
runtime_min = 0
runtime_frame = 0
runtime_x = 0

def update_time_game():
    global time_game_min,time_game_frame,time_game_seconds,time_game_seconds_x,time_game_x,time_speed
    """
    Incrémente le temps (in game) toutes les secondes (fps frames Pyxel).
    """
    time_game_frame += time_speed
    time_game_x += time_speed

    if time_game_x >= fps:
            time_game_x -= fps
            time_game_seconds += 1
            time_game_seconds_x += 1  
            if debug.debug_mode == True:
             print(f"time game (sec) = {time_game_seconds}, vitesse jeu = {time_speed}")
    if time_game_seconds_x >= 60:
         time_game_seconds_x -= 60
         time_game_min += 1
         if debug.debug_mode == True:
            print(f"time game(min) = {time_game_min}")

def update_runtime():
    global runtime_min,runtime_frame,runtime_seconds,runtime_seconds_x,runtime_x,time_speed
    """
    Incrémente le temps (depuis le début) toutes les secondes (fps frames Pyxel).
    """
    if debug.time_speed != 1:
        time_speed = debug.time_speed

    runtime_frame += time_speed
    runtime_x += time_speed

    if runtime_x >= fps:
            runtime_x -= fps
            runtime_seconds += 1
            runtime_seconds_x += 1  
            if debug.debug_mode == True:
                print(f"runtime (sec) = {runtime_seconds}, vitesse jeu = {time_speed}")
    if runtime_seconds_x >= 60:
         runtime_seconds_x -= 60
         runtime_min += 1
         if debug.debug_mode == True:
            print(f"runtime (min) = {runtime_min}")

def reset_game_time():
    global time_game_min,time_game_frame,time_game_seconds,time_game_seconds_x,time_x

    time_game_seconds = 0
    time_game_seconds_x = 0
    time_game_min = 0
    time_game_frame = 0
    time_x = 0

def reset_global_time():
    global runtime_min,runtime_frame,runtime_seconds,runtime_seconds_x,runtime_x

    runtime_seconds = 0
    runtime_seconds_x = 0
    runtime_min = 0
    runtime_frame = 0
    runtime_x = 0

def reset_game_speed():
    global time_speed

    time_speed = 1
     

def update():
     update_runtime()
