import random
import time
import tkinter


class Cell:
    def __init__(self):
        self.visited = False
        self.doors = set()


class Maze:
    def __init__(self, cells):
        self.cells = cells
        self.rows = len(cells)
        self.columns = len(cells[0])

    def ascii(self):
        result = [['#' for _ in range(self.columns*2+1)] for _ in range(self.rows*2+1)]
        for rowidx, row in enumerate(self.cells):
            for colidx, cell in enumerate(row):
                if cell.visited:
                    result[1+rowidx*2][1+colidx*2] = ' '
                if 'n' in cell.doors:
                    result[rowidx*2][1+colidx*2] = ' '
                if 'e' in cell.doors:
                    result[1+rowidx*2][2+colidx*2] = ' '
                if 's' in cell.doors:
                    result[2+rowidx*2][1+colidx*2] = ' '
                if 'w' in cell.doors:
                    result[1+rowidx*2][colidx*2] = ' '
        return "\n".join("".join(line) for line in result)

    def graphics(self):
        gui = GuiWindow(self.columns, self.rows)
        gui.canvas.delete(tkinter.ALL)
        for rowidx, row in enumerate(self.cells):
            for colidx, cell in enumerate(row):
                x, y = colidx*gui.SCALE+1, rowidx*gui.SCALE+1
                if 'n' not in cell.doors:
                    gui.canvas.create_line(x, y, x+gui.SCALE, y)
                if 'e' not in cell.doors:
                    gui.canvas.create_line(x+gui.SCALE, y, x+gui.SCALE, y+gui.SCALE)
                if 's' not in cell.doors:
                    gui.canvas.create_line(x, y+gui.SCALE, x+gui.SCALE, y+gui.SCALE)
                if 'w' not in cell.doors:
                    gui.canvas.create_line(x, y, x, y+gui.SCALE)

        gui.mainloop()


class GuiWindow(tkinter.Tk):
    SCALE = 6

    def __init__(self, columns, rows):
        super().__init__()
        self.title("maze")
        self.geometry("{}x{}".format(columns*self.SCALE+self.SCALE, rows*self.SCALE+self.SCALE))
        self.canvas = tkinter.Canvas(self, bg='light gray')
        self.canvas.pack(fill=tkinter.BOTH, expand=True)


class HuntAndKillMazeGenerator:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.cells = [[Cell() for _ in range(columns)] for _ in range(rows)]

    def generate(self):
        start_col = 0
        start_row = 0
        while start_col >= 0:
            self.carve(start_col, start_row)
            start_col, start_row = self.find_unvisited()
            print(" ", start_row, end="          \r", flush=True)
            #print("\033[2J\033[;H")  # clear screen
            #print(Maze(self.cells).ascii())
            #time.sleep(0.01)
        return Maze(self.cells)

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


if __name__ == "__main__":
    width = 200
    height = 150
    print("Generating maze of {}x{} cells...".format(width, height))
    gen = HuntAndKillMazeGenerator(width, height)
    maze = gen.generate()
    print("\ndone!")
    maze.graphics()
    # print(maze.ascii())
