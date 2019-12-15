from mazes.generators import HuntAndKill


if __name__ == "__main__":
    maze_generator = HuntAndKill(60, 20)

    for maze in maze_generator.generate():
        pass

    print(maze.ascii(wall='▒', space='·'))
