import tkinter
from typing import Set, Tuple
from mazes.maze import Maze, dxdy
from mazes.generators import *
from mazes.solvers import DepthFirstSolver, BreadthFirstSolver


class GuiWindow(tkinter.Tk):
    def __init__(self, columns: int, rows: int, scale: int = 14) -> None:
        super().__init__()
        self.scale = scale
        self.title("maze")
        self.geometry("{}x{}+400+200".format(columns*self.scale+self.scale, rows*self.scale+self.scale))
        self.canvas = tkinter.Canvas(self, bg='light gray')
        self.canvas.pack(fill=tkinter.BOTH, expand=True, padx=4, pady=4)
        self.drawn_tagged_cells: Set[Tuple[int, int]] = set()

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
        self.canvas.create_line(1+x1*self.scale, 1+y1*self.scale, 1+x2*self.scale, 1+y2*self.scale)

    def clear(self) -> None:
        self.canvas.delete(tkinter.ALL)
        self.drawn_tagged_cells.clear()

    def erase_path(self, path: str) -> None:
        self.canvas.delete("path")

    def draw_path(self, path: str, color: str = "teal") -> None:
        x, y = 0, 0
        self.canvas.create_rectangle(4+x*self.scale, 4+y*self.scale,
                                     self.scale-2+x*self.scale, self.scale-2+y*self.scale,
                                     fill=color, tags="path")
        for step in path:
            x += dxdy[step][0]
            y += dxdy[step][1]
            self.canvas.create_rectangle(4+x*self.scale, 4+y*self.scale,
                                         self.scale-2+x*self.scale, self.scale-2+y*self.scale,
                                         fill=color, tags="path")

    def draw_tagged_cells(self) -> None:
        colors = [f"#{c:02x}0000" for c in range(256)]

        def color(tag: int) -> str:
            return colors[tag % len(colors)]

        for y, row in enumerate(maze.cells):
            for x, cell in enumerate(row):
                if cell.tag and (x, y) not in self.drawn_tagged_cells:
                    self.drawn_tagged_cells.add((x, y))
                    self.canvas.create_rectangle(3+x*self.scale, 3+y*self.scale,
                                                 self.scale+x*self.scale, self.scale+y*self.scale,
                                                 fill=color(cell.tag), outline="", tags="path")


if __name__ == "__main__":
    width = 100
    height = 60
    # maze_generator = HuntAndKillGenerator(width, height)
    maze_generator = DepthFirstGenerator(width, height)
    mazes = maze_generator.generate_iterative()
    maze = Maze([[]])
    gui = GuiWindow(width, height, 10)

    def generate_maze():
        global maze
        try:
            for _ in range(maze_generator.suggested_iteration_size * 5):
                maze = next(mazes)
        except StopIteration:
            solve_maze()
        else:
            gui.draw_maze(maze)
            gui.after(10, generate_maze)

    def solve_maze():
        # solutions = DepthFirstSolver().solve_generator(maze)
        solutions = BreadthFirstSolver().solve_generator(maze)
        previous_path = ""

        def animate_solve_tags():
            nonlocal previous_path
            try:
                previous_path = next(solutions)
            except StopIteration:
                gui.draw_tagged_cells()
                gui.draw_path(previous_path, "yellow")   # previous_path contains the shortest path
            else:
                gui.draw_tagged_cells()
                gui.after(1, animate_solve_tags)

        # def animate_solve_paths():
        #     nonlocal previous_path
        #     try:
        #         path = next(solutions)
        #     except StopIteration:
        #         pass
        #     else:
        #         gui.erase_path(previous_path)
        #         gui.draw_path(path)
        #         previous_path = path
        #         gui.after(1, animate_solve)
        #
        # animate_solve_paths()

        animate_solve_tags()

    gui.after_idle(generate_maze)
    gui.mainloop()
