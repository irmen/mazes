import random
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
                # the south and west don't have to be drawn because the neighbor cell already takes care of it
                # if 's' in cell.doors:
                #     result[2+rowidx*2][1+colidx*2] = ' '
                # if 'w' in cell.doors:
                #     result[1+rowidx*2][colidx*2] = ' '
        return "\n".join("".join(line) for line in result)

    def draw_graphics(self, gui):
        gui.clear()
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if 'n' not in cell.doors:
                    gui.line(x, y, x+1, y)
                if 'e' not in cell.doors:
                    gui.line(x+1, y, x+1, y+1)
                # the south and west don't have to be drawn because the neighbor cell already takes care of it
                # if 's' not in cell.doors:
                #     gui.line(x, y+1, x+1, y+1)
                # if 'w' not in cell.doors:
                #     gui.line(x, y, x, y+1)
        # make sure west and south borders are drawn
        gui.line(0, 0, 0, self.rows)
        gui.line(0, self.rows, self.columns, self.rows)


class GuiWindow(tkinter.Tk):
    SCALE = 12

    def __init__(self, columns, rows):
        super().__init__()
        self.title("maze")
        self.geometry("{}x{}".format(columns*self.SCALE+self.SCALE, rows*self.SCALE+self.SCALE))
        self.canvas = tkinter.Canvas(self, bg='light gray')
        self.canvas.pack(fill=tkinter.BOTH, expand=True, padx=4, pady=4)

    def line(self, x1, y1, x2, y2):
        self.canvas.create_line(1+x1*self.SCALE, 1+y1*self.SCALE, 1+x2*self.SCALE, 1+y2*self.SCALE)

    def clear(self):
        self.canvas.delete(tkinter.ALL)


class HuntAndKillMazeGenerator:
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


if __name__ == "__main__":
    width = 80
    height = 60
    maze_generator = HuntAndKillMazeGenerator(width, height)
    mazes = maze_generator.generate()
    gui = GuiWindow(width, height)

    def generate_maze():
        try:
            _ = next(mazes)
            maze = next(mazes)
        except StopIteration:
            pass
        else:
            maze.draw_graphics(gui)
            # print("NEXT MAZE\n", maze.ascii())
            gui.after(10, generate_maze)

    gui.after_idle(generate_maze)
    gui.mainloop()
