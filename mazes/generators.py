import random
from .maze import Cell, Maze


class HuntAndKill:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.cells = [[Cell() for _ in range(columns)] for _ in range(rows)]

    def generate(self):
        # first a few random start positions
        for _ in range(int((self.columns*self.rows)**0.4)):
            start_col = random.randrange(0, self.columns)
            start_row = random.randrange(0, self.rows)
            self.carve(start_col, start_row)
            yield Maze(self.cells)
        start_col = 0
        start_row = 0
        while start_col >= 0:
            self.carve(start_col, start_row)
            start_col, start_row = self.find_unvisited()
            yield Maze(self.cells)

    def find_unvisited(self):
        for rowidx, row in enumerate(self.cells):
            for column, cell in enumerate(row):
                if not cell.visited:
                    # check if we have a visited neighbor, if so carve a path and continue with this cell
                    _, _, neighbor = self.travel(column, rowidx, "n")
                    if not(neighbor is cell) and neighbor.visited:
                        cell.doors.add("n")
                        neighbor.doors.add("s")
                        return column, rowidx
                    _, _, neighbor = self.travel(column, rowidx, "e")
                    if not(neighbor is cell) and neighbor.visited:
                        cell.doors.add("e")
                        neighbor.doors.add("w")
                        return column, rowidx
                    _, _, neighbor = self.travel(column, rowidx, "s")
                    if not(neighbor is cell) and neighbor.visited:
                        cell.doors.add("s")
                        neighbor.doors.add("n")
                        return column, rowidx
                    _, _, neighbor = self.travel(column, rowidx, "w")
                    if not(neighbor is cell) and neighbor.visited:
                        cell.doors.add("w")
                        neighbor.doors.add("e")
                        return column, rowidx
        return -1, -1

    dxdy = {
        "n": (0, -1),
        "e": (1, 0),
        "s": (0, 1),
        "w": (-1, 0)
    }
    opposite_direction = {
        "n": "s",
        "e": "w",
        "s": "n",
        "w": "e",
    }

    def travel(self, column, row, direction):
        dx, dy = self.dxdy[direction]
        column = max(min(column + dx, self.columns-1), 0)
        row = max(min(row + dy, self.rows-1), 0)
        return column, row, self.cells[row][column]

    def carve(self, column, row):
        while True:
            cell = self.cells[row][column]
            cell.visited = True
            _, _, cell_n = self.travel(column, row, "n")
            _, _, cell_e = self.travel(column, row, "e")
            _, _, cell_s = self.travel(column, row, "s")
            _, _, cell_w = self.travel(column, row, "w")
            if cell_n.visited and cell_e.visited and cell_s.visited and cell_w.visited:
                return
            while True:
                direction = random.choice("nesw")
                next_col, next_row, next_cell = self.travel(column, row, direction)
                if not next_cell.visited:
                    break
            cell.doors.add(direction)
            next_cell.doors.add(self.opposite_direction[direction])
            column = next_col
            row = next_row
