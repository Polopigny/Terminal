import pyxel
import debug
import enemi


class VagueManager:
    """
    Gère les vagues d'ennemis (spawn, vague, progression de la difficulté).
    """

    def __init__(self):

        self.time_seconds = 0
        self.can_spawn = False

        self.difficulty = 4
        self.enemies_added_per_wave = 2

        self.is_wave_ready = False
        self.wave_interval = 5
        self.wave_interval_base = 20
        self.last_wave_time = 0
        self.remaining_time_until_wave = 0
        self.current_wave = 0

        self.target_enemy_count = 0

        self.base_enemy_count = 10
        self.start_delay_over = False
        self.start_delay_duration = 5

    def update_time(self):
        """
        Incrémente le temps toutes les secondes (30 frames Pyxel).
        """
        if pyxel.frame_count % 30 == 0:
            self.time_seconds += 1
            if debug.debug_mode:
                print(f"time (sec) = {self.time_seconds}")

    def handle_start_delay(self):
        """
        Gère le délai initial avant le début des vagues.
        """
        if self.start_delay_over == False:
            self.target_enemy_count = self.base_enemy_count
        if self.time_seconds == self.start_delay_duration:
            self.can_spawn = True
            self.start_delay_over = True
            self.last_wave_time = self.time_seconds
            self.wave_interval = self.wave_interval_base

    def update_wave_state(self):
        """
        Vérifie si une nouvelle vague doit commencer.
        """
        if self.start_delay_over:
            if self.is_wave_ready:
                self.last_wave_time = self.time_seconds
                self.is_wave_ready = False
            elif self.time_seconds >= self.last_wave_time + self.wave_interval:
                self.is_wave_ready = True
                self.current_wave += 1

    def calculate_enemy_spawn_goal(self):
        """
        Détermine combien d'ennemis doivent apparaître pour cette vague.
        """
        if self.is_wave_ready:
            min_enemies = self.base_enemy_count + self.enemies_added_per_wave
            max_enemies = self.base_enemy_count + self.difficulty * self.enemies_added_per_wave * self.current_wave
            self.target_enemy_count = pyxel.rndi(min_enemies, max_enemies)
            if debug.debug_mode:
                print(f"Max enemies to spawn this wave: {max_enemies}")

    def spawn_enemies(self):
        """
        Crée des ennemis tant que le quota de la vague n'est pas atteint.
        """
        if self.can_spawn:
            while enemi.nb_enemi_global < self.target_enemy_count:
                enemi.creation()

    def update_wave_timer_draw(self):
        """
        Met à jour le temps restant avant la prochaine vague (pour affichage).
        """
        self.remaining_time_until_wave = self.last_wave_time + self.wave_interval - self.time_seconds

    def draw_progress_bar(self):
        """
        Affiche une barre de progression pour le compte à rebours de vague.
        """
        x = enemi.player.player.x - 50
        y = enemi.player.player.y - 118
        width = 100
        height = 7

        # fond + texte
        pyxel.rect(x, y, width, height, pyxel.COLOR_PEACH)
        pyxel.text(x + 10, y + 10, "time till next round", pyxel.COLOR_WHITE)

        # barre rouge qui diminue
        progress_width = self.remaining_time_until_wave * 100 / self.wave_interval
        pyxel.rect(x, y, progress_width, height, pyxel.COLOR_RED)

        # compte à rebours
        pyxel.text(x + 48, y + 1, str(self.remaining_time_until_wave), pyxel.COLOR_BLACK)

    def update(self):
        """
        Mise à jour principale (appelée à chaque frame).
        """
        self.update_time()
        self.handle_start_delay()
        self.update_wave_state()
        self.calculate_enemy_spawn_goal()
        self.spawn_enemies()
        self.update_wave_timer_draw()

    def draw(self):
        """
        Affiche les informations de débogage et la barre de vague.
        """
        x = enemi.player.player.x - 118
        y = enemi.player.player.y + 118

        if debug.debug_mode:
            pyxel.text(x, y - 30, f"time to next wave = {self.remaining_time_until_wave}", pyxel.COLOR_WHITE)
            pyxel.text(x, y - 20, f"time = {self.time_seconds}", pyxel.COLOR_WHITE)
            pyxel.text(x, y - 10, f"wave = {self.current_wave}", pyxel.COLOR_WHITE)
            pyxel.text(x, y, f"enemies to spawn = {self.target_enemy_count}", pyxel.COLOR_WHITE)

        self.draw_progress_bar()
    
    def reset(self):
        self.time_seconds = 0
        self.can_spawn = False

        self.difficulty = 4
        self.enemies_added_per_wave = 2

        self.is_wave_ready = False
        self.wave_interval = 5
        self.wave_interval_base = 20
        self.last_wave_time = 0
        self.remaining_time_until_wave = 0
        self.current_wave = 0

        self.target_enemy_count = 0

        self.base_enemy_count = 10
        self.start_delay_over = False
        self.start_delay_duration = 5


VagueManager_var = VagueManager()
