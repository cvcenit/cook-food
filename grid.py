from utils import TILE_SIDE_LENGTH, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET
import pyxel

class Tile:
    def __init__(self, row, col, isPath: bool, isTunnel: bool = False):
        self._row = row
        self._col = col
        self._isPath = isPath
        self._isTunnel = isTunnel

    @property
    def is_path(self) -> bool:
        return self._isPath
    
    def screen_position(self) -> tuple[float, float]:
        x = GAMEPLAY_X_OFFSET + self._col * TILE_SIDE_LENGTH
        y = GAMEPLAY_Y_OFFSET + self._row * TILE_SIDE_LENGTH
        return x, y

    def draw(self):
        x, y = self.screen_position()
        ix, iy = x + (TILE_SIDE_LENGTH / 2), y + (TILE_SIDE_LENGTH / 2)

        if self._isTunnel:
            sx, sy = 32, 32
        elif self._isPath:
            sx, sy = 0, 32
        else:
            sx, sy = 0, 0

        pyxel.blt(
            ix - 16, iy - 16,  # center the sprite
            2,               # image bank 0
            sx, sy,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent color (black)
            scale=TILE_SIDE_LENGTH/32
        )

    def draw_rock(self):
        x, y = self.screen_position()
        ix, iy = x + (TILE_SIDE_LENGTH / 2), y + (TILE_SIDE_LENGTH / 2)

        pyxel.blt(
            ix - 16, iy - 16,  # center the sprite
            2,               # image bank 0
            0, 0,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent color (black)
            scale=TILE_SIDE_LENGTH/32
        )
        pyxel.blt(
            ix - 16, iy - 16,  # center the sprite
            2,               # image bank 0
            64, 0,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent color (black)
            scale=TILE_SIDE_LENGTH/32
        )
        


class Grid:
    def __init__(self, rows: int, cols: int, path: list[tuple[int, int]], tunnels = None):
        set_path = set(path)
        set_tunnel = set(tunnels or [])
        self._tiles = [[Tile(r, c, isPath=(r, c) in set_path, isTunnel=(r, c) in set_tunnel) for c in range(cols)] for r in range(rows)]

    def draw(self):
        for row in self._tiles:
            for tile in row:
                if tile._row == 0 or tile._row == len(self._tiles) - 1:
                    tile.draw_rock()
                    continue
                tile.draw()

