"""
Level data lives here as plain 2D grids, so redesigning or adding a level is
just editing/adding one of the grids below (or calling the same builder
helpers with different coordinates).

Legend: '#' solid block   '.' empty space   'P' player spawn   'E' enemy spawn
"""

from objects import GameObject, Transform
from physics.colliders.collider import Collider
from physics.physics_material import PhysicsMaterial

from .constants import CELL, COLS, ROWS


def _blank():
    return [["."] * COLS for _ in range(ROWS)]


def _border(grid):
    for col in range(COLS):
        grid[0][col] = "#"
        grid[ROWS - 1][col] = "#"
    for row in range(ROWS):
        grid[row][0] = "#"
        grid[row][COLS - 1] = "#"
    return grid


def _hline(grid, row, col_start, length):
    for i in range(length):
        grid[row][col_start + i] = "#"


def _put(grid, row, col, ch):
    grid[row][col] = ch


def _rows(grid):
    return ["".join(row) for row in grid]


def _level_one():
    grid = _border(_blank())
    _hline(grid, 3, 5, 8)
    _hline(grid, 3, 17, 5)
    _hline(grid, 8, 9, 6)
    _put(grid, 2, 7, "E")
    _put(grid, 7, 11, "E")
    _put(grid, 13, 21, "E")
    _put(grid, 13, 1, "P")
    return _rows(grid)


def _level_two():
    grid = _border(_blank())
    _hline(grid, 5, 10, 4)
    _hline(grid, 9, 4, 6)
    _hline(grid, 9, 15, 6)
    _put(grid, 4, 11, "E")
    _put(grid, 8, 6, "E")
    _put(grid, 8, 17, "E")
    _put(grid, 13, 20, "E")
    _put(grid, 13, 1, "P")
    return _rows(grid)


def _level_three():
    grid = _border(_blank())
    _hline(grid, 6, 3, 5)
    _hline(grid, 6, 15, 5)
    _hline(grid, 10, 9, 7)
    _put(grid, 5, 5, "E")
    _put(grid, 5, 17, "E")
    _put(grid, 9, 12, "E")
    _put(grid, 13, 3, "E")
    _put(grid, 13, 21, "E")
    _put(grid, 13, 1, "P")
    return _rows(grid)


LEVELS = [_level_one(), _level_two(), _level_three()]


def build_level(display, grid, id_gen):
    """Parses a level grid into wall GameObjects, the player spawn point,
    and a list of enemy spawn points."""
    wall_material = PhysicsMaterial(restitution=0.1, friction=0.6)
    platforms = []
    player_spawn = (CELL, CELL)
    enemy_spawns = []

    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == "#":
                start = c
                while c < len(row) and row[c] == "#":
                    c += 1
                run_len = c - start
                go = GameObject(display, id_gen("wall"),
                                 Transform((start * CELL, r * CELL), (run_len * CELL, CELL)),
                                 (90, 90, 100))
                go.collider = Collider(go, wall_material)
                platforms.append(go)
                continue
            if ch == "P":
                player_spawn = (c * CELL, r * CELL)
            elif ch == "E":
                enemy_spawns.append((c * CELL, r * CELL))
            c += 1

    return platforms, player_spawn, enemy_spawns
