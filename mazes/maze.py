class Cell:
    def __init__(self):
        self.carved = False
        self.doors = ""         # n, e, s, w  possible


class Maze:
    def __init__(self, cells) -> None:
        self.cells = cells
        self.rows = len(cells)
        self.columns = len(cells[0])

    def ascii(self, wall='#', space=' ') -> str:
        result = [[wall for _ in range(self.columns*2+1)] for _ in range(self.rows*2+1)]
        for rowidx, row in enumerate(self.cells):
            for colidx, cell in enumerate(row):
                if cell.carved:
                    result[1+rowidx*2][1+colidx*2] = space
                if 'n' in cell.doors:
                    result[rowidx*2][1+colidx*2] = space
                if 'e' in cell.doors:
                    result[1+rowidx*2][2+colidx*2] = space
                # the south and west don't have to be drawn because the neighbor cells already takes care of these
        return "\n".join("".join(line) for line in result)

    def draw_graphics(self, gui) -> None:
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                # note athat the south and west don't have to be drawn,
                # because the neighbor cells already takes care of these
                if 'n' not in cell.doors:
                    gui.line(x, y, x+1, y)
                if 'e' not in cell.doors:
                    gui.line(x+1, y, x+1, y+1)
        # make sure the maze's west and south borders are closed:
        gui.line(0, 0, 0, self.rows)
        gui.line(0, self.rows, self.columns, self.rows)
