from mazes.maze import Maze
from mazes.generators import HuntAndKill


def ascii_maze(maze: Maze, wall: str = '#', space: str = ' ') -> str:
    result = [[wall for _ in range(maze.num_columns * 2 + 1)] for _ in range(maze.num_rows * 2 + 1)]
    for rowidx, row in enumerate(maze.cells):
        for colidx, cell in enumerate(row):
            if cell.open:
                result[1+rowidx*2][1+colidx*2] = space
            if 'n' in cell.doors:
                result[rowidx*2][1+colidx*2] = space
            if 'e' in cell.doors:
                result[1+rowidx*2][2+colidx*2] = space
            # the south and west don't have to be drawn because the neighbor cells already takes care of these
    return "\n".join("".join(line) for line in result)


if __name__ == "__main__":
    maze_generator = HuntAndKill(60, 20)

    for maze in maze_generator.generate():
        pass

    print(ascii_maze(maze, wall='▒', space='·'))
