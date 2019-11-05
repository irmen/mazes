import time
from mazes.generators import HuntAndKill


if __name__ == "__main__":
    maze_generator = HuntAndKill(60, 20)

    for maze in maze_generator.generate():
        pass

    #print("\x1b[2J\x1b[H")
    print(maze.ascii(wall='▒', space='·'))
