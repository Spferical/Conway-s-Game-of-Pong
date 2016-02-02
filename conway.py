import numpy
import config
import copy
import libtcodpy as tcod


def lerp_colors(colors):
    final_color = tcod.white
    i = 0
    for color in colors:
        i += 1
        final_color = tcod.color_lerp(final_color, color, 1.0 / i)
    return final_color


class ConwaySim(object):
    """Stores a 2d array of tiles
    Simulates Conway's Game of Life"""
    def __init__(self, (width, height), color=False):
        self.width = width
        self.height = height
        self.color = color
        if self.color: dtype = object
        else: dtype = bool
        self.blank_tiles = numpy.array(
            [[False for y in range(self.height)]
             for x in range(self.width)],
            dtype=dtype)
        self.tiles = copy.deepcopy(self.blank_tiles)

    def __getitem__(self, x):
        return self.tiles[x]

    def __setitem__(self, key, value):
        self.tiles[key] = value

    @property
    def size(self):
        return (self.width, self.height)

    def is_out_of_bounds(self, (x, y)):
        if x < 0:
            return True
        if x > self.width - 1:
            return True
        if y < 0:
            return True
        if y > self.height - 1:
            return True
        return False

    def get_adjacent(self, (x, y)):
        cells = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not (dx == 0 and dy == 0):
                    if not self.is_out_of_bounds((x + dx, y + dy)):
                        if self.get_blocked((x + dx, y + dy)) == 1:
                            cells.append(self.tiles[x + dx, y + dy])
        return cells
    
    def get_num_adjacent(self, (x, y)):
        adjacent = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not (dx == 0 and dy == 0):
                    if self.get_blocked((x + dx, y + dy)):
                        adjacent += 1
        return adjacent

    def update(self):
        if self.color: self.update_color()
        else: self.update_colorless()

    def update_color(self):
        new_map = copy.deepcopy(self.blank_tiles)
        for x in range(self.width):
            for y in range(self.height):
                adjacent = self.get_adjacent((x, y))
                alive = len(adjacent) == 3 or \
                    (len(adjacent) == 2 and self[x, y])
                if alive:
                    final_color = lerp_colors(adjacent)
                    new_map[x, y] = final_color
        self.tiles = new_map
    
    def update_colorless(self):
        new_map = copy.deepcopy(self.blank_tiles)
        for x in range(self.width):
            for y in range(self.height):
                num_adjacent = self.get_num_adjacent((x, y))
                alive = num_adjacent == 3 or (num_adjacent == 2 and self[x, y])
                new_map[x, y] = alive
        self.tiles = new_map

    def get_blocked(self, (x, y)):
        if self.is_out_of_bounds((x, y)):
            return False
        return bool(self.tiles[x, y])
