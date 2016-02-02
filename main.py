#!/usr/bin/python
import libtcodpy as tcod
import ui
from config import SCREEN_SIZE, MAX_FPS, GAME_TITLE


tcod.console_set_custom_font('arial12x12.png',
                             tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

w, h = SCREEN_SIZE
tcod.console_init_root(w, h, GAME_TITLE, False)

tcod.sys_set_fps(MAX_FPS)


if __name__ == '__main__':
    ui.handle_main_menu()
