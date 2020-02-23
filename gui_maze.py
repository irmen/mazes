import tkinter
import colorsys
from typing import Set, Tuple
from mazes.maze import Maze, dxdy
from mazes.generators import *
from mazes.solvers import DepthFirstSolver, BreadthFirstSolver


class GuiWindow(tkinter.Tk):
    def __init__(self, columns: int, rows: int, scale: int = 14) -> None:
        super().__init__()
        self.columns = columns
        self.rows = rows
        self.scale = scale
        self.title("maze")
        self.geometry("+400+200")
        self.canvas = tkinter.Canvas(self, bg='light gray', width=columns*self.scale+1, height=rows*self.scale+1)
        bf = tkinter.Frame(self)
        b1 = tkinter.Button(bf, text="Depth First Search", command=self.search_dfs)
        b2 = tkinter.Button(bf, text="Breadth First Search", command=self.search_bfs)
        b1.pack(side=tkinter.LEFT)
        b2.pack(side=tkinter.LEFT)
        bf.pack()
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

    def draw_tagged_cells(self, maze: Maze) -> None:
        colors = []
        for hue in range(256):
            rf, gf, bf = colorsys.hsv_to_rgb(hue/256, 1, 0.99999)
            r = int(rf*256)
            g = int(gf*256)
            b = int(bf*256)
            colors.append(f"#{r:02x}{g:02x}{b:02x}")

        def color(tag: int) -> str:
            return colors[tag % len(colors)]

        for y, row in enumerate(maze.cells):
            for x, cell in enumerate(row):
                if cell.tag and (x, y) not in self.drawn_tagged_cells:
                    self.drawn_tagged_cells.add((x, y))
                    self.canvas.create_rectangle(3+x*self.scale, 3+y*self.scale,
                                                 self.scale+x*self.scale, self.scale+y*self.scale,
                                                 fill=color(cell.tag), outline="", tags="path")

    def search_bfs(self):
        self.clear()

        def solve_maze(maze: Maze) -> None:
            solutions = BreadthFirstSolver().solve_generator(maze)
            previous_path = ""

            def animate_solve_tags():
                nonlocal previous_path
                more = True
                try:
                    previous_path = next(solutions)
                except StopIteration:
                    more = False
                self.draw_tagged_cells(maze)
                if more:
                    self.after(1, animate_solve_tags)
                else:
                    self.draw_path(previous_path, "black")   # previous_path contains the shortest path

            animate_solve_tags()

        self.generate_maze(solve_maze)

    def search_dfs(self):
        self.clear()

        def solve_maze(maze: Maze) -> None:
            solutions = DepthFirstSolver().solve_generator(maze)
            previous_path = ""

            def animate_solve_paths():
                nonlocal previous_path
                more = True
                path = ""
                try:
                    for _ in range(10):
                        path = next(solutions)
                        if not path:
                            break
                except StopIteration:
                    more = False
                self.erase_path(previous_path)
                self.draw_path(path)
                previous_path = path
                if more:
                    gui.after(2, animate_solve_paths)

            animate_solve_paths()

        self.generate_maze(solve_maze)

    def generate_maze(self, solver) -> None:
        # maze_generator = HuntAndKillGenerator(self.columns, self.rows)
        maze_generator = DepthFirstGenerator(self.columns, self.rows)
        mazes = maze_generator.generate_iterative()

        def generate():
            maze = Maze([[]])
            try:
                for _ in range(maze_generator.suggested_iteration_size * 5):
                    maze = next(mazes)
            except StopIteration:
                solver(maze)
            else:
                self.draw_maze(maze)
                self.after(10, generate)

        generate()


if __name__ == "__main__":
    gui = GuiWindow(100, 60, 10)
    gui.mainloop()
