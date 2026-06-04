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
        ix, iy = int(x), int(y)
        ts = int(TILE_SIDE_LENGTH)  # 90

        if self._isTunnel:
            pyxel.rect(ix, iy, ts, ts, 5)
            sx, sy = 32, 32
        elif self._isPath:
            pyxel.rect(ix, iy, ts, ts, 3)
            sx, sy = 0, 32
        else:
            pyxel.rect(ix, iy, ts, ts, 8)
            sx, sy = 0, 0

        for dy in range(0, ts, 32):
            for dx in range(0, ts, 32):
                pyxel.blt(ix + dx, iy + dy, 2, sx, sy, 32, 32, 0)


class Grid:
    def __init__(self, rows: int, cols: int, path: list[tuple[int, int]], tunnels = None):
        set_path = set(path)
        set_tunnel = set(tunnels or [])
        self._tiles = [[Tile(r, c, isPath=(r, c) in set_path, isTunnel=(r, c) in set_tunnel) for c in range(cols)] for r in range(rows)]

    def draw(self):
        for row in self._tiles:
            for tile in row:
                if tile._row == 0 or tile._row == len(self._tiles) - 1:
                    continue
                tile.draw()

