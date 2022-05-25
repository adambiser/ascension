import appgamekit as agk

TILE_SIZE = 16
HORIZONTAL_MOVE_SPEED = 6
VERTICAL_ACCELERATION = 1.05
MAX_SPEED = 10
MAX_OBSTACLES = 6
SPAWN_RANGE = (10, 40)

follow_player = False
player_start_y = 0
player_speed = 1
player_dead = False
player_score = 0

spawn_counter = 20


def create_player():
    image_id = agk.create_image_color(255, 255, 255, 255)
    sprite = agk.create_sprite(image_id)
    agk.set_sprite_size(sprite, TILE_SIZE, TILE_SIZE * 2)
    agk.set_sprite_offset(sprite, agk.get_sprite_width(sprite) / 2, agk.get_sprite_height(sprite))
    agk.set_sprite_position_by_offset(sprite, TILE_SIZE * 2.5, agk.get_virtual_height() - TILE_SIZE * 4)
    return sprite


def create_ground():
    image_id = agk.create_image_color(0, 192, 0, 255)
    sprite = agk.create_sprite(image_id)
    agk.set_sprite_size(sprite, agk.get_virtual_width(), TILE_SIZE)
    agk.set_sprite_position(sprite, 0, agk.get_virtual_height() - agk.get_sprite_height(sprite))
    return sprite


def create_obstacle():
    image_id = agk.create_image_color(255, 0, 0, 255)
    sprite = agk.create_sprite(image_id)
    agk.set_sprite_size(sprite, TILE_SIZE * 2, TILE_SIZE * 2)
    agk.set_sprite_offset(sprite, agk.get_sprite_width(player) / 2, agk.get_sprite_height(player) / 2)
    agk.set_sprite_visible(sprite, False)
    return sprite


def update_player(player):
    global follow_player, player_start_y
    movex = 0
    if agk.get_raw_key_state(agk.KEY_LEFT):
        movex -= 1
    if agk.get_raw_key_state(agk.KEY_RIGHT):
        movex += 1
    # if movex:
    x = agk.get_sprite_x_by_offset(player)
    x += movex * HORIZONTAL_MOVE_SPEED
    # todo clamp
    if x < TILE_SIZE:
        x = TILE_SIZE
    if x > agk.get_virtual_width() - TILE_SIZE:
        x = agk.get_virtual_width() - TILE_SIZE
    y = agk.get_sprite_y_by_offset(player)
    global player_speed
    y += player_speed
    player_speed *= VERTICAL_ACCELERATION
    if y > agk.get_sprite_y(ground):
        y = agk.get_sprite_y(ground)
        follow_player = True
        player_start_y = agk.get_sprite_y_by_offset(player)
        player_speed = -1
    # Todo clamp()
    if player_speed < -MAX_SPEED:
        player_speed = -MAX_SPEED
    elif player_speed > MAX_SPEED:
        player_speed = MAX_SPEED
    agk.set_sprite_position_by_offset(player, x, y)
    if follow_player:
        viewy = agk.get_sprite_y_by_offset(player) - player_start_y
        agk.set_view_offset(0, viewy)
        # Fly above the atmosphere.
        sky_color = 200 - int(-viewy // 50)
        if sky_color < 0:
            sky_color = 0
        agk.set_clear_color(0, sky_color, sky_color)


def update_obstacle(obstacle):
    # Spawn if needed.
    if not agk.get_sprite_visible(obstacle):
        global spawn_counter
        if spawn_counter:
            return
        spawn_counter = agk.random(*SPAWN_RANGE)
        agk.set_sprite_visible(obstacle, True)
        spawnx = agk.get_sprite_x_by_offset(player)
        spawnx += agk.random(0, TILE_SIZE * 4) - TILE_SIZE * 2
        # todo clamp
        if spawnx < TILE_SIZE:
            spawnx = TILE_SIZE
        if spawnx > agk.get_virtual_width() - TILE_SIZE:
            spawnx = agk.get_virtual_width() - TILE_SIZE
        agk.set_sprite_position_by_offset(obstacle,
                                          spawnx,
                                          agk.get_view_offset_y() - TILE_SIZE * 3)
    # Did it go off the bottom?
    y = agk.get_sprite_y(obstacle)
    if y > agk.get_view_offset_y() + agk.get_virtual_height():
        agk.set_sprite_visible(obstacle, False)
        global player_score
        player_score += 1
        return
    # TODO Move toward the player.
    # Check collision with player.
    if agk.get_sprite_collision(obstacle, player):
        global player_dead
        player_dead = True


with agk.Application(width=1024, height=768, app_name="Ascension"):
    agk.set_virtual_resolution(320, 240)
    agk.set_clear_color(0, 200, 200)
    agk.set_sync_rate(30, 0)
    player = create_player()
    ground = create_ground()
    obstacles = [create_obstacle() for _ in range(4)]
    while True:
        agk.print_value(f"{agk.screen_fps():.1f}")
        agk.print_value(f"speed: {player_speed:.1f}")
        agk.print_value(f"Score: {player_score}")
        if not player_dead:
            update_player(player)
            if follow_player:
                for obstacle in obstacles:
                    update_obstacle(obstacle)
                if spawn_counter > 0:
                    spawn_counter -= 1
        else:
            agk.print_value("You failed!")
        agk.sync()
        if agk.get_raw_key_pressed(agk.KEY_ESCAPE):
            break
