import appgamekit as agk
import game.config as _config


class Ground:
    def __init__(self):
        self.sprite_id = self._create_ground_sprite()

    @staticmethod
    def _create_ground_sprite():
        image_id = agk.create_image_color(0, 192, 0, 255)
        sprite_id = agk.create_sprite(image_id)
        agk.set_sprite_size(sprite_id, agk.get_virtual_width(), _config.TILE_SIZE)
        agk.set_sprite_position(sprite_id, 0, agk.get_virtual_height() - agk.get_sprite_height(sprite_id))
        return sprite_id
