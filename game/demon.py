import appgamekit as agk
import game.config as _config
import game.session as _session
from .utils import clamp

SPAWN_RANGE = (10, 40)


class Demon:
    _IMAGE_ID = 0
    SPEED = 1
    SPAWN_SOUND = 0

    def __init__(self):
        self.sprite_id = self._create_demon_sprite()
        if not Demon.SPAWN_SOUND:
            Demon.SPAWN_SOUND = agk.load_sound("demon-spawn.wav")
        self._player = None

    def set_player(self, value):
        self._player = value

    @property
    def position(self):
        return agk.get_sprite_x_by_offset(self.sprite_id), agk.get_sprite_y_by_offset(self.sprite_id)

    @position.setter
    def position(self, xy):
        agk.set_sprite_position_by_offset(self.sprite_id, *xy)

    @property
    def active(self):
        return agk.get_sprite_active(self.sprite_id)

    @classmethod
    def _create_demon_sprite(cls):
        # Only load the image once.
        if not cls._IMAGE_ID:
            cls._IMAGE_ID = agk.load_image("LPC Imp 2/red/attack - vanilla.png")
        sprite_id = agk.create_sprite(cls._IMAGE_ID)
        agk.set_sprite_animation(sprite_id, 64, 64, 16)
        agk.play_sprite(sprite_id, 10, True, 9, 12)
        agk.set_sprite_size(sprite_id, _config.TILE_SIZE * 2, _config.TILE_SIZE * 2)
        agk.set_sprite_offset(sprite_id, agk.get_sprite_width(sprite_id) / 2, agk.get_sprite_height(sprite_id) / 2)
        agk.set_sprite_shape_box(sprite_id, -14, -16, 14, 14, 0)
        agk.set_sprite_visible(sprite_id, False)
        agk.set_sprite_active(sprite_id, False)
        return sprite_id

    def update(self):
        if not self.active:
            return
        if not self._player.active:
            return
        self.chase_player()
        self.attack_player()
        self.check_deactivate()

    def check_deactivate(self):
        # Did it go off the bottom?
        y = agk.get_sprite_y(self.sprite_id)
        if y > agk.get_view_offset_y() + agk.get_virtual_height():
            self.deactivate()

    def chase_player(self):
        # Chase the player.
        player_x = self._player.position[0]
        this_x = agk.get_sprite_x_by_offset(self.sprite_id)
        if player_x < this_x:
            agk.set_sprite_position_by_offset(self.sprite_id, this_x - self.SPEED, agk.get_sprite_y_by_offset(self.sprite_id))
        elif player_x > this_x:
            agk.set_sprite_position_by_offset(self.sprite_id, this_x + self.SPEED, agk.get_sprite_y_by_offset(self.sprite_id))

    def attack_player(self):
        # Check collision with player.
        if agk.get_sprite_collision(self.sprite_id, self._player.sprite_id):
            self._player.die()

    def spawn(self):
        spawnx = self._player.position[0]
        spawnx += agk.random(0, _config.TILE_SIZE * 4) - _config.TILE_SIZE * 2
        spawnx = clamp(spawnx, _config.TILE_SIZE, agk.get_virtual_width() - _config.TILE_SIZE)
        self.position = spawnx, agk.get_view_offset_y() - _config.TILE_SIZE * 3
        agk.set_sprite_visible(self.sprite_id, True)
        agk.set_sprite_active(self.sprite_id, True)
        agk.play_sound(Demon.SPAWN_SOUND, 50)

    def deactivate(self):
        agk.set_sprite_visible(self.sprite_id, False)
        agk.set_sprite_active(self.sprite_id, False)
        _session.score += 1

