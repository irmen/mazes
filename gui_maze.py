import tkinter
from mazes.maze import Maze
from mazes.generators import HuntAndKill


class GuiWindow(tkinter.Tk):
    SCALE = 12

    def __init__(self, columns: int, rows: int) -> None:
        super().__init__()
        self.title("maze")
        self.geometry("{}x{}+400+200".format(columns*self.SCALE+self.SCALE, rows*self.SCALE+self.SCALE))
        self.canvas = tkinter.Canvas(self, bg='light gray')
        self.canvas.pack(fill=tkinter.BOTH, expand=True, padx=4, pady=4)

    def draw_maze(self, maze: Maze) -> None:
        self.clear()     # don't redraw everything every frame but just keep removing walls progressively?
        for y, row in enumerate(maze.cells):
            for x, cell in enumerate(row):
                # note that the south and west don't have to be drawn,
                # because the neighbor cells already takes care of these
                if 'n' not in cell.doors:
                    self.line(x, y, x+1, y)
                if 'e' not in cell.doors:
                    self.line(x+1, y, x+1, y+1)
        # make sure the maze's west and south borders are closed:
        self.line(0, 0, 0, maze.num_rows)
        self.line(0, maze.num_rows, maze.num_columns, maze.num_rows)

    def line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.canvas.create_line(1+x1*self.SCALE, 1+y1*self.SCALE, 1+x2*self.SCALE, 1+y2*self.SCALE)

    def clear(self) -> None:
        self.canvas.delete(tkinter.ALL)


if __name__ == "__main__":
    width = 80
    height = 60
    maze_generator = HuntAndKill(width, height)
    mazes = maze_generator.generate()
    gui = GuiWindow(width, height)

    def generate_maze():
        try:
            maze = next(mazes)
        except StopIteration:
            pass
        else:
            gui.draw_maze(maze)
            gui.after(10, generate_maze)

    gui.after_idle(generate_maze)
    gui.mainloop()
