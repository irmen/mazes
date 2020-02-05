import time
from mazes.maze import Maze
from mazes.generators import HuntAndKill
from mazes.runners import DepthFirst, DxDy


def ascii_maze(maze: Maze, solution: str = "", wall: str = '#', space: str = ' ', walk: str = '*') -> str:
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
    if solution:
        x, y = (1, 1)
        result[y][x] = walk
        for direction in solution:
            x += DxDy[direction][0]
            y += DxDy[direction][1]
            result[y][x] = walk
            x += DxDy[direction][0]
            y += DxDy[direction][1]
            result[y][x] = walk
    return "\n".join("".join(line) for line in result)


if __name__ == "__main__":
    # print just the maze in one go:
    # maze_generator = HuntAndKill(30, 12)
    # maze = maze_generator.generate()
    # print(ascii_maze(maze, "", wall='▒', space='·'))

    # solve maze in one go using Depth First Search:
    # solver = DepthFirst()
    # solution = solver.solve(maze)
    # print(ascii_maze(maze, solution, wall='▒', space='·'))

    maze_generator = HuntAndKill(30, 12)
    maze = Maze([[]])
    for maze in maze_generator.generate_iterative():
        print("\033[2J\033[H")      # clear screen
        print(ascii_maze(maze, "", wall='▒', space='·'))
        print()
        time.sleep(0.05)

    # solve maze using DFS and animate the searched paths
    solver = DepthFirst()
    steps = ""
    for steps in solver.solve_iterative(maze):
        print("\033[2J\033[H")      # clear screen
        print(ascii_maze(maze, steps, wall='▒', space='·'))
        print()
        time.sleep(0.02)

    print("final solution:", steps)
