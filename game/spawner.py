import appgamekit as agk
from .demon import Demon

SPAWN_RANGE = (10, 40)


class Spawner:
    MAX_DEMONS = 10

    def __init__(self):
        self.demons = [Demon() for _ in range(self.MAX_DEMONS)]
        self._counter = 20
        self._player = None

    def set_player(self, player):
        self._player = player
        for demon in self.demons:
            demon.set_player(player)

    def update(self):
        if not self._player.active:
            return
        if not self._counter:
            demon = next((d for d in self.demons if not d.active), None)
            if demon:
                demon.spawn()
                # Spawn more quickly as the player ascends.
                view_y = int(-agk.get_view_offset_y() // 200)
                spawn_range = list(SPAWN_RANGE)
                # spawn_range[0] -= view_y
                spawn_range[1] -= view_y
                if 0 < spawn_range[0] < spawn_range[1]:
                    self._counter = agk.random(*SPAWN_RANGE)
                else:
                    self._counter = 5
        for demon in self.demons:
            demon.update()
        if self._counter > 0:
            self._counter -= 1
