from mazes.gui import GuiWindow
from mazes.generators import HuntAndKill


if __name__ == "__main__":
    width = 80
    height = 60
    maze_generator = HuntAndKill(width, height)
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
