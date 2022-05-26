import appgamekit as _agk
import game.config as _config
import game.session as _session
from .utils import clamp


HORIZONTAL_MOVE_SPEED = 6
VERTICAL_ACCELERATION = 1.05
MAX_SPEED = 10


class Player:
    def __init__(self):
        self.speed = -1.0
        self.is_alive = True
        self.sprite_id = self._create_ghost_sprite()
        self.death_animation_sprite = self._create_death_animation_sprite()
        _agk.set_view_offset(0, 0)
        _agk.set_clear_color(0, 200, 200)
        self._start_y = self.position[1]

    @staticmethod
    def _create_ghost_sprite():
        image_id = _agk.load_image("ghost.png")
        sprite_id = _agk.create_sprite(image_id)
        _agk.set_sprite_animation(sprite_id, 32, 64, 12)
        _agk.play_sprite(sprite_id, 5, True, 1, 3)
        _agk.set_sprite_size(sprite_id, _config.TILE_SIZE, _config.TILE_SIZE * 2)
        _agk.set_sprite_offset(sprite_id, _agk.get_sprite_width(sprite_id) / 2, _agk.get_sprite_height(sprite_id))
        _agk.set_sprite_position_by_offset(sprite_id,
                                           _config.TILE_SIZE * 2.5,
                                           _agk.get_virtual_height() - _config.TILE_SIZE)
        _agk.set_sprite_shape_box(sprite_id, -8, -48, 8, -10, 0)
        _agk.set_sprite_visible(sprite_id, False)
        _agk.set_sprite_active(sprite_id, False)
        return sprite_id

    @staticmethod
    def _create_death_animation_sprite():
        image_id = _agk.load_image("Platformer Shooter 2D Shotgun 7 Actions/death_spritesheet.png")
        sprite_id = _agk.create_sprite(image_id)
        _agk.set_sprite_animation(sprite_id, 138, 138, 6)
        _agk.set_sprite_size(sprite_id, 138, 138)
        _agk.set_sprite_scale(sprite_id, 0.5, 0.5)
        _agk.set_sprite_offset(sprite_id, _agk.get_sprite_width(sprite_id) / 2, _agk.get_sprite_height(sprite_id))
        _agk.set_sprite_position_by_offset(sprite_id,
                                           _config.TILE_SIZE * 2.5,
                                           _agk.get_virtual_height() - _config.TILE_SIZE + 2)
        _agk.set_sprite_visible(sprite_id, False)
        _agk.set_sprite_active(sprite_id, False)
        return sprite_id

    @property
    def position(self):
        return _agk.get_sprite_x_by_offset(self.sprite_id), _agk.get_sprite_y_by_offset(self.sprite_id)

    @position.setter
    def position(self, xy):
        _agk.set_sprite_position_by_offset(self.sprite_id, *xy)

    @property
    def active(self):
        return _agk.get_sprite_active(self.sprite_id)

    def play_death_animation(self):
        _agk.set_sprite_visible(self.death_animation_sprite, True)
        _agk.set_sprite_active(self.death_animation_sprite, True)
        _agk.play_sprite(self.death_animation_sprite, 3, False)

    def update(self):
        if _agk.get_sprite_current_frame(self.death_animation_sprite) == 6:
            _agk.set_sprite_visible(self.sprite_id, True)
            _agk.set_sprite_active(self.sprite_id, True)
        if not _agk.get_sprite_active(self.sprite_id):
            return
        self.move_horizontally()
        self.move_vertically()
        self.move_camera()

    def move_horizontally(self):
        movex = 0
        if _agk.get_raw_key_state(_agk.KEY_LEFT):
            movex -= 1
        if _agk.get_raw_key_state(_agk.KEY_RIGHT):
            movex += 1
        x, y = self.position
        x += movex * HORIZONTAL_MOVE_SPEED
        x = clamp(x, _config.TILE_SIZE, _agk.get_virtual_width() - _config.TILE_SIZE)
        self.position = x, y

    def move_vertically(self):
        x, y = self.position
        y += self.speed
        self.speed *= VERTICAL_ACCELERATION
        self.speed = clamp(self.speed, -MAX_SPEED, MAX_SPEED)
        self.position = x, y

    def move_camera(self):
        viewy = _agk.get_sprite_y_by_offset(self.sprite_id) - self._start_y
        _agk.set_view_offset(0, viewy)
        # Fly into space.
        sky_color = 200 - int(-viewy // 50)
        if sky_color < 0:
            sky_color = 0
        _agk.set_clear_color(0, sky_color, sky_color)

    def die(self):
        self.is_alive = False
        _session.active = False
