import libtcodpy as tcod


def get_key(key):
    if key.vk == tcod.KEY_CHAR:
        return chr(key.c)
    else:
        return key.vk
