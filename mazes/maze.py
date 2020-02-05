from typing import List


DxDy = {
    "n": (0, -1),
    "e": (1, 0),
    "s": (0, 1),
    "w": (-1, 0)
}


class Cell:
    def __init__(self) -> None:
        self.open = False
        self.doors = ""         # n, e, s, w  possible


class Maze:
    def __init__(self, cells: List[List[Cell]]) -> None:
        self.cells = cells
        self.num_rows = len(cells)
        self.num_columns = len(cells[0])
