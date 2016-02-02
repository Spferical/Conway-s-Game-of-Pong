import libtcodpy as tcod
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIZE, CONWAY_SPEED,\
    MAX_FPS, PLAYER_COLORS, GAME_TITLE, CONWAY_SIZE, PADDLE_SIZE, VERSION
import game
import copy
import util

controls = [
    ['w', 's'],
    [tcod.KEY_UP, tcod.KEY_DOWN],
    ['t', 'g'],
    ['i', 'k'],
]

number_keys = [tcod.KEY_0, tcod.KEY_1, tcod.KEY_2, tcod.KEY_3, tcod.KEY_4,
               tcod.KEY_5, tcod.KEY_6, tcod.KEY_7, tcod.KEY_8, tcod.KEY_9]


def whole_number_menu(var, title, min_var=None):
    """A menu to change the value of a whole number x"""
    w, h = SCREEN_WIDTH, SCREEN_HEIGHT
    window = tcod.console_new(w, h)
    key = tcod.console_check_for_keypress()
    while not key.vk in (tcod.KEY_ENTER, tcod.KEY_ESCAPE):
        tcod.console_clear(window)
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2
        tcod.console_set_default_foreground(window, tcod.yellow)
        tcod.console_set_alignment(window, tcod.CENTER)
        tcod.console_print(window, x, y, title)
        tcod.console_set_default_foreground(window, tcod.white)
        tcod.console_print(window, x, y + 2, str(var))

        tcod.console_set_default_foreground(window, tcod.grey)
        tcod.console_print(window, x, y + 4, 'Use arrows or number keys')
        tcod.console_print(window, x, y + 5,
                           'Press Enter or Escape to return')
        tcod.console_blit(window, 0, 0, w, h, 0, 0, 0, 1.0, 1.0)
        tcod.console_flush()

        key = tcod.console_wait_for_keypress(True)

        if key.pressed:

            if key.vk == tcod.KEY_LEFT:
                var = max(var - 1, 0)
            elif key.vk == tcod.KEY_BACKSPACE:
                string_var = str(var)[:-1]
                if string_var == '':
                    var = 0
                else:
                    var = int(string_var)
            elif key.vk in number_keys:
                str_number = str(number_keys.index(key.vk))
                var = int(str(var) + str_number)
            elif key.vk == tcod.KEY_RIGHT:
                var += 1
    if min_var is None or var >= min_var:
        return var
    else:
        return whole_number_menu(var, title, min_var)


def handle_main_menu():
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, False)
    # the player controls to send to the Game class
    # 'ai' = controlled by an ai
    player_controls = [controls[0],
                       'ai',
                       ]

    conway_speed = CONWAY_SPEED
    map_width, map_height = CONWAY_SIZE
    max_fps = MAX_FPS
    color = False
    paddle_size = PADDLE_SIZE
    seamless = True

    while not tcod.console_is_window_closed():
        tcod.console_clear(0)
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_set_alignment(0, tcod.CENTER)
        tcod.console_print(0, SCREEN_WIDTH / 2, 2,
                           'Conway\'s Game of Pong')
        tcod.console_set_default_foreground(0, tcod.grey)
        tcod.console_print(0, SCREEN_WIDTH / 2, 3,
                           'by Spferical (Spferical@gmail.com)')
        tcod.console_print(0, SCREEN_WIDTH / 2, 4,
                           'Version %s' % VERSION)
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_set_alignment(0, tcod.LEFT)
        tcod.console_print(0, 2, 6, '(a) Play')
        tcod.console_print(0, 2, 7, '(b) Exit')
        player_keys = ['c', 'd']
        y = 8
        x = 2
        playernum = -1
        for c in player_controls:
            y += 1
            playernum += 1
            k = player_keys[playernum]
            if c:
                tcod.console_set_default_foreground(
                    0, PLAYER_COLORS[playernum])
            else:
                tcod.console_set_default_foreground(0, tcod.grey)
            if c and not c == 'ai':
                if c == [tcod.KEY_UP, tcod.KEY_DOWN]:
                    str_controls = '[arrow keys]'
                else:
                    str_controls = str(c)
                text = '(' + k + ') ' + str(playernum +
                                            1) + ' Player ' + str_controls
            elif c == 'ai':
                text = '(' + k + ') ' + str(playernum + 1) + ' CPU'
            else:
                text = '(' + k + ') ' + str(playernum + 1) + ' Not Playing'
            tcod.console_print(0, x, y, text)

        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_print(0, 2, 13,
                           '(e) Paddle size: ' + str(paddle_size))
        tcod.console_print(0, 2, 14,
                           '(f) Conway speed: ' + str(conway_speed))
        tcod.console_print(0, 2, 16,
                           '(g) Map width: ' + str(map_width))
        tcod.console_print(0, 2, 17,
                           '(h) Map height: ' + str(map_height))
        tcod.console_print(0, 2, 19,
                           '(i) FPS: ' + str(max_fps))
        tcod.console_print(0, 2, 20, '(j) Fancy color effect (laggy): ' + \
                           str(color))
        tcod.console_print(0, 2, 21, '(k) Game reset after every score: ' + \
                           str(not seamless))

        tcod.console_flush()

        raw_key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
        key = util.get_key(raw_key)
        if key == 'a':
            g = game.Game(player_controls, conway_speed,
                          (map_width, map_height), max_fps, color, paddle_size,
                          seamless)
            g.run()
            #to clean up after Game
            tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                                   GAME_TITLE, False)
        elif key == 'b':
            break
        elif key in player_keys:
            p = player_keys.index(key)
            c = player_controls[p]
            if not c:
                player_controls[p] = controls[p]
            elif c == 'ai':
                player_controls[p] = None
            else:
                player_controls[p] = 'ai'
        elif key == 'e':
            paddle_size = whole_number_menu(
                paddle_size, 'The paddles will be how many blocks big?')
        elif key == 'f':
            conway_speed = whole_number_menu(
                conway_speed, 'The Life simulation will update every how many frames?')
        elif key == 'g':
            map_width = whole_number_menu(
                map_width, 'How wide should the map be?', min_var=1)
        elif key == 'h':
            map_height = whole_number_menu(
                map_height, 'How tall should the map be?', min_var=1)
        elif key == 'i':
            max_fps = whole_number_menu(
                max_fps, 'How many frames per second should the game ' + \
                        'run at?\n (0 = no limit)')
        elif key == 'j':
            color = not color
        elif key == 'k':
            seamless = not seamless
        elif key == tcod.KEY_ESCAPE:
            break
