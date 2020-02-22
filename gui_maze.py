import tkinter
from mazes.maze import Maze, dxdy
from mazes.generators import *
from mazes.solvers import DepthFirstSolver, BreadthFirstSolver


class GuiWindow(tkinter.Tk):
    SCALE = 14

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

    def erase_path(self, path: str) -> None:
        self.canvas.delete("path")

    def draw_path(self, path: str, color: str = "teal") -> None:
        x, y = 0, 0
        self.canvas.create_rectangle(4+x*self.SCALE, 4+y*self.SCALE,
                                     (self.SCALE-3)+x*self.SCALE, (self.SCALE-3)+y*self.SCALE,
                                     fill=color, tags="path")
        for step in path:
            x += dxdy[step][0]
            y += dxdy[step][1]
            self.canvas.create_rectangle(4+x*self.SCALE, 4+y*self.SCALE,
                                         (self.SCALE-3)+x*self.SCALE, (self.SCALE-3)+y*self.SCALE,
                                         fill=color, tags="path")


if __name__ == "__main__":
    width = 50
    height = 40
    # maze_generator = HuntAndKillGenerator(width, height)
    maze_generator = DepthFirstGenerator(width, height)
    mazes = maze_generator.generate_iterative()
    maze = Maze([[]])
    gui = GuiWindow(width, height)

    def generate_maze():
        global maze
        try:
            for _ in range(maze_generator.suggested_iteration_size):
                maze = next(mazes)
        except StopIteration:
            solve_maze()
        else:
            gui.draw_maze(maze)
            gui.after(10, generate_maze)

    def solve_maze():
        # solutions = DepthFirstSolver().solve_generator(maze)
        solutions = BreadthFirstSolver().solve_generator(maze)
        previous_solution = (Maze([[]]), "")

        def animate_solve():
            nonlocal previous_solution
            try:
                solution = next(solutions)
            except StopIteration:
                pass
            else:
                gui.erase_path(previous_solution)
                gui.draw_path(solution)
                previous_solution = solution
                gui.after(2, animate_solve)

        animate_solve()

    gui.after_idle(generate_maze)
    gui.mainloop()
