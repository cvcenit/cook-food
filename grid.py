from utils import TILE_SIDE_LENGTH, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET
import pyxel

class Tile:
    def __init__(self, row, col, isPath: bool):
        self._row = row
        self._col = col
        self._isPath = isPath

    @property
    def is_path(self) -> bool:
        return self._isPath
    
    def screen_position(self) -> tuple[float, float]:
        x = GAMEPLAY_X_OFFSET + self._col * TILE_SIDE_LENGTH
        y = GAMEPLAY_Y_OFFSET + self._row * TILE_SIDE_LENGTH
        return x, y
    
    def draw(self):
        x, y = self.screen_position()
        color = 3 if self._isPath else 8 # 3 (green), 8 (red)
        pyxel.rect(x, y, TILE_SIDE_LENGTH, TILE_SIDE_LENGTH, color)
        # pyxel.rectb(x, y, TILE_SIDE_LENGTH, TILE_SIDE_LENGTH, 1)

class Grid:
    def __init__(self, rows: int, cols: int, path: list[tuple[int, int]]):
        set_path = set(path)
        self._tiles = [[Tile(r, c, isPath=(r, c) in set_path) for c in range(cols)] for r in range(rows)]

    def draw(self):
        for row in self._tiles:
            for tile in row:
                if tile._row == 0 or tile._row == len(self._tiles) - 1:
                    continue
                tile.draw()

