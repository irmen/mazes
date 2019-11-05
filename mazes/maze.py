class Cell:
    def __init__(self):
        self.visited = False
        self.doors = set()


class Maze:
    def __init__(self, cells):
        self.cells = cells
        self.rows = len(cells)
        self.columns = len(cells[0])

    def ascii(self, wall='#', space=' '):
        result = [[wall for _ in range(self.columns*2+1)] for _ in range(self.rows*2+1)]
        for rowidx, row in enumerate(self.cells):
            for colidx, cell in enumerate(row):
                if cell.visited:
                    result[1+rowidx*2][1+colidx*2] = space
                if 'n' in cell.doors:
                    result[rowidx*2][1+colidx*2] = space
                if 'e' in cell.doors:
                    result[1+rowidx*2][2+colidx*2] = space
                # the south and west don't have to be drawn because the neighbor cell already takes care of it
                # if 's' in cell.doors:
                #     result[2+rowidx*2][1+colidx*2] = space
                # if 'w' in cell.doors:
                #     result[1+rowidx*2][colidx*2] = space
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

