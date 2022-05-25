import appgamekit as agk

TILE_SIZE = 32
HORIZONTAL_MOVE_SPEED = 6
VERTICAL_ACCELERATION = 1.05
MAX_SPEED = 10
MAX_OBSTACLES = 6
SPAWN_RANGE = (10, 40)
DEMON_SPEED = 1

follow_player = False
player_start_y = 0
player_speed = 1
player_dead = False
player_score = 0

spawn_counter = 20


def clamp(value, min_value, max_value):
    return min_value if value < min_value else max_value if value > max_value else value


def create_player():
    image_id = agk.load_image("ghost.png")
    sprite = agk.create_sprite(image_id)
    agk.set_sprite_animation(sprite, 32, 64, 12)
    agk.play_sprite(sprite, 5, True, 1, 3)
    agk.set_sprite_size(sprite, TILE_SIZE, TILE_SIZE * 2)
    agk.set_sprite_offset(sprite, agk.get_sprite_width(sprite) / 2, agk.get_sprite_height(sprite))
    agk.set_sprite_position_by_offset(sprite, TILE_SIZE * 2.5, agk.get_virtual_height() - TILE_SIZE)
    agk.set_sprite_shape_box(sprite, -8, -48, 8, -10, 0)
    agk.set_sprite_visible(sprite, False)
    agk.set_sprite_active(sprite, False)
    return sprite


def create_death():
    image_id = agk.load_image("Platformer Shooter 2D Shotgun 7 Actions/death_spritesheet.png")
    sprite = agk.create_sprite(image_id)
    agk.set_sprite_animation(sprite, 138, 138, 6)
    agk.play_sprite(sprite, 3, False)
    agk.set_sprite_size(sprite, 138, 138)
    agk.set_sprite_scale(sprite, 0.5, 0.5)
    agk.set_sprite_offset(sprite, agk.get_sprite_width(sprite) / 2, agk.get_sprite_height(sprite))
    agk.set_sprite_position_by_offset(sprite, TILE_SIZE * 2.5, agk.get_virtual_height() - TILE_SIZE + 2)
    return sprite


def create_ground():
    image_id = agk.create_image_color(0, 192, 0, 255)
    sprite = agk.create_sprite(image_id)
    agk.set_sprite_size(sprite, agk.get_virtual_width(), TILE_SIZE)
    agk.set_sprite_position(sprite, 0, agk.get_virtual_height() - agk.get_sprite_height(sprite))
    return sprite


def create_obstacle():
    image_id = agk.load_image("LPC Imp 2/red/attack - vanilla.png")
    sprite = agk.create_sprite(image_id)
    agk.set_sprite_animation(sprite, 64, 64, 16)
    agk.play_sprite(sprite, 10, True, 9, 12)
    agk.set_sprite_size(sprite, TILE_SIZE * 2, TILE_SIZE * 2)
    agk.set_sprite_offset(sprite, agk.get_sprite_width(sprite) / 2, agk.get_sprite_height(sprite) / 2)
    agk.set_sprite_shape_box(sprite, -14, -16, 14, 14, 0)
    agk.set_sprite_visible(sprite, False)
    return sprite


def update_player(player):
    global follow_player, player_start_y
    movex = 0
    if agk.get_raw_key_state(agk.KEY_LEFT):
        movex -= 1
    if agk.get_raw_key_state(agk.KEY_RIGHT):
        movex += 1
    x = agk.get_sprite_x_by_offset(player)
    x += movex * HORIZONTAL_MOVE_SPEED
    x = clamp(x, TILE_SIZE, agk.get_virtual_width() - TILE_SIZE)
    y = agk.get_sprite_y_by_offset(player)
    global player_speed
    y += player_speed
    player_speed *= VERTICAL_ACCELERATION
    if y > agk.get_sprite_y(ground):
        y = agk.get_sprite_y(ground)
        follow_player = True
        player_start_y = agk.get_sprite_y_by_offset(player)
        player_speed = -1
    player_speed = clamp(player_speed, -MAX_SPEED, MAX_SPEED)
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
        spawnx = clamp(spawnx, TILE_SIZE, agk.get_virtual_width() - TILE_SIZE)
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
    # Chase the player.
    player_x = agk.get_sprite_x_by_offset(player)
    this_x = agk.get_sprite_x_by_offset(obstacle)
    if player_x < this_x:
        agk.set_sprite_position_by_offset(obstacle, this_x - DEMON_SPEED, agk.get_sprite_y_by_offset(obstacle))
    elif player_x > this_x:
        agk.set_sprite_position_by_offset(obstacle, this_x + DEMON_SPEED, agk.get_sprite_y_by_offset(obstacle))
    # Check collision with player.
    if agk.get_sprite_collision(obstacle, player):
        global player_dead
        player_dead = True


with agk.Application(width=1024, height=768, app_name="Ascension"):
    agk.set_virtual_resolution(320, 240)
    agk.set_clear_color(0, 200, 200)
    agk.set_sync_rate(30, 0)
    agk.set_default_min_filter(agk.FILTER_NEAREST)
    agk.set_default_mag_filter(agk.FILTER_NEAREST)
    debug_on = False
    death_animation = create_death()
    player = create_player()
    ground = create_ground()
    obstacles = [create_obstacle() for _ in range(4)]
    while True:
        if agk.get_raw_key_state(agk.KEY_LEFT_CTRL) or agk.get_raw_key_state(agk.KEY_RIGHT_CTRL):
            if agk.get_raw_key_pressed(agk.KEY_D):  # debug mode.
                agk.set_physics_debug_off() if debug_on else agk.set_physics_debug_on()
                debug_on = not debug_on
        agk.print_value(f"{agk.screen_fps():.1f}")
        agk.print_value(f"speed: {player_speed:.1f}")
        agk.print_value(f"Score: {player_score}")
        if agk.get_sprite_current_frame(death_animation) == 6:
            agk.set_sprite_visible(player, True)
            agk.set_sprite_active(player, True)
        if not player_dead:
            if agk.get_sprite_active(player):
                update_player(player)
                if follow_player:
                    for obstacle in obstacles:
                        update_obstacle(obstacle)
                    if spawn_counter > 0:
                        spawn_counter -= 1
        else:
            agk.print_value("GAME OVER!")
        agk.sync()
        if agk.get_raw_key_pressed(agk.KEY_ESCAPE):
            break
