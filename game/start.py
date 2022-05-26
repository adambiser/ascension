import appgamekit as agk
import game.session as session
from .player import Player
from .ground import Ground
from .spawner import Spawner


class Title:
    def __init__(self):
        self.text_id = self._create_text()
        self.visible = False

    @staticmethod
    def _create_text():
        text_id = agk.create_text("Ascension\nBy Fascimania (Adam Biser)\n"
                                  "For GameDev.tv Game Jam 2022\n\n"
                                  "Use the left and right arrow keys to\n"
                                  "guide your ghost into the heavens.\n"
                                  "Avoid the demons!\n\n"
                                  "See credits.txt for credits.")
        agk.set_text_alignment(text_id, agk.ALIGN_CENTER)
        agk.set_text_x(text_id, agk.get_virtual_width() / 2)
        agk.set_text_y(text_id, agk.get_virtual_height() / 2 - 90)
        agk.set_text_size(text_id, 20)
        agk.fix_text_to_screen(text_id, True)
        return text_id

    @property
    def visible(self):
        return agk.get_text_visible(self.text_id)

    @visible.setter
    def visible(self, value):
        agk.set_text_visible(self.text_id, value)


class GameOver:
    def __init__(self):
        self.text_id = self._create_text()
        self.visible = False

    @staticmethod
    def _create_text():
        text_id = agk.create_text("Game Over!")
        agk.set_text_alignment(text_id, agk.ALIGN_CENTER)
        agk.set_text_x(text_id, agk.get_virtual_width() / 2)
        agk.set_text_y(text_id, agk.get_virtual_height() / 2 - 10)
        agk.set_text_size(text_id, 20)
        agk.fix_text_to_screen(text_id, True)
        return text_id

    @property
    def visible(self):
        return agk.get_text_visible(self.text_id)

    @visible.setter
    def visible(self, value):
        agk.set_text_visible(self.text_id, value)


with agk.Application(width=1024, height=768, app_name="Ascension"):
    agk.set_virtual_resolution(320, 240)
    agk.set_clear_color(0, 200, 200)
    agk.set_sync_rate(30, 0)
    agk.set_default_min_filter(agk.FILTER_NEAREST)
    agk.set_default_mag_filter(agk.FILTER_NEAREST)
    agk.use_new_default_fonts(True)
    debug_on = False
    ground = Ground()
    player = Player()
    demons = Spawner()
    demons.set_player(player)
    session.reset()
    gameover = GameOver()
    # Show the title screen.
    title = Title()
    title.visible = Title
    while True:
        agk.sync()
        if agk.get_raw_key_pressed(agk.get_raw_last_key()):
            break
        if agk.get_raw_mouse_left_pressed():
            break
    # Start game loop
    title.visible = False
    player.play_death_animation()
    while True:
        if agk.get_raw_key_state(agk.KEY_LEFT_CTRL) or agk.get_raw_key_state(agk.KEY_RIGHT_CTRL):
            if agk.get_raw_key_pressed(agk.KEY_D):  # debug mode.
                agk.set_physics_debug_off() if debug_on else agk.set_physics_debug_on()
                debug_on = not debug_on
        # agk.print_value(f"{agk.screen_fps():.1f}")
        # agk.print_value(f"speed: {player.speed:.1f}")
        agk.print_value(f"Score: {session.score}")
        if session.active:
            player.update()
            demons.update()
        else:
            gameover.visible = True
        agk.sync()
        if agk.get_raw_key_pressed(agk.KEY_ESCAPE):
            break
