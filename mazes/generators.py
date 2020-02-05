import random
from typing import Generator, Tuple, List
from .maze import Cell, Maze


class HuntAndKill:
    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.cells = [[Cell() for _ in range(columns)] for _ in range(rows)]
        self._previous_start_row = 0

    def generate(self) -> Generator[Maze, None, None]:
        # first a few random start routes, to make the maze more 'well-formed'
        for _ in range(int((self.columns*self.rows)**0.4)):
            start_col = random.randrange(0, self.columns)
            start_row = random.randrange(0, self.rows)
            self.carve(start_col, start_row)
            yield Maze(self.cells)
        start_col = 0
        start_row = 0
        while start_col >= 0:
            self.carve(start_col, start_row)
            start_col, start_row = self.find_next_unvisited()
            yield Maze(self.cells)

    opposite_direction = {
        "n": "s",
        "e": "w",
        "s": "n",
        "w": "e",
    }

    def find_next_unvisited(self) -> Tuple[int, int]:
        for row in range(self._previous_start_row, self.rows):
            rowcells = self.cells[row]
            for column, cell in enumerate(rowcells):
                if not cell.open:
                    # check if we have an open neighbor, if so carve a path to that and continue with this cell
                    neighbors = self.neighbors(column, row)
                    open_neighbors = [(direction, cell) for direction, cell in neighbors if cell.open]
                    if open_neighbors:
                        direction, neighbor = random.choice(open_neighbors)
                        cell.doors += direction
                        neighbor.doors += self.opposite_direction[direction]
                        self._previous_start_row = row
                        return column, row
        return -1, -1

    def neighbors(self, column: int, row: int) -> List[Tuple[str, Cell]]:
        n = []
        if row > 0:
            n.append(("n", self.cells[row-1][column]))
        if column < self.columns-1:
            n.append(("e", self.cells[row][column+1]))
        if row < self.rows-1:
            n.append(("s", self.cells[row+1][column]))
        if column > 0:
            n.append(("w", self.cells[row][column-1]))
        return n

    def carve(self, column: int, row: int) -> None:
        while True:
            cell = self.cells[row][column]
            cell.open = True
            neighbors = self.neighbors(column, row)
            if all(cell.open for _, cell in neighbors):
                return
            while True:
                direction, next_cell = random.choice(neighbors)
                next_col, next_row = column, row
                if direction == "n":
                    next_row -= 1
                elif direction == "e":
                    next_col += 1
                elif direction == "s":
                    next_row += 1
                elif direction == "w":
                    next_col -= 1
                if not next_cell.open:
                    break
            cell.doors += direction
            next_cell.doors += self.opposite_direction[direction]
            column = next_col
            row = next_row
