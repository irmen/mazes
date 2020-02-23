import time

from mazes.generators import *
from mazes.maze import Maze
from mazes.solvers import DepthFirstSolver, BreadthFirstSolver, dxdy


def ascii_maze_with_path(maze: Maze, path: str = "", wall: str = '#', space: str = ' ', walk: str = '*') -> str:
    result = [[wall for _ in range(maze.num_columns * 2 + 1)] for _ in range(maze.num_rows * 2 + 1)]
    for rowidx, row in enumerate(maze.cells):
        for colidx, cell in enumerate(row):
            if cell.open:
                result[1 + rowidx * 2][1 + colidx * 2] = space
            if 'n' in cell.doors:
                result[rowidx * 2][1 + colidx * 2] = space
            if 'e' in cell.doors:
                result[1 + rowidx * 2][2 + colidx * 2] = space
            # the south and west don't have to be drawn because the neighbor cells already takes care of these
    if path:
        x, y = (1, 1)
        result[y][x] = walk
        for direction in path:
            x += dxdy[direction][0]
            y += dxdy[direction][1]
            result[y][x] = walk
            x += dxdy[direction][0]
            y += dxdy[direction][1]
            result[y][x] = walk
    return "\n".join("".join(line) for line in result)


def ascii_maze_with_tags(maze: Maze, wall: str = '#', space: str = ' ', tagged: str = '*') -> str:
    result = [[wall for _ in range(maze.num_columns * 2 + 1)] for _ in range(maze.num_rows * 2 + 1)]
    for rowidx, row in enumerate(maze.cells):
        for colidx, cell in enumerate(row):
            char = tagged if cell.tag else space
            if cell.open:
                result[1 + rowidx * 2][1 + colidx * 2] = char
            if 'n' in cell.doors:
                result[rowidx * 2][1 + colidx * 2] = char
            if 'e' in cell.doors:
                result[1 + rowidx * 2][2 + colidx * 2] = char
            # the south and west don't have to be drawn because the neighbor cells already takes care of these
    return "\n".join("".join(line) for line in result)


if __name__ == "__main__":
    # print just the maze in one go:
    # maze_generator = DepthFirstGenerator(30, 12)
    # maze = maze_generator.generate()
    # print(ascii_maze(maze, "", wall='▒', space='·'))

    # maze_generator = HuntAndKillGenerator(30, 12)
    maze_generator = DepthFirstGenerator(35, 14)
    maze = Maze([[]])
    if maze_generator.suggested_iteration_size == 1:
        for maze in maze_generator.generate_iterative():
            print("\033[2J\033[H")  # clear screen
            print(ascii_maze_with_path(maze, "", wall='▒', space='·'))
            print()
            time.sleep(0.05)
    else:
        mazes = iter(maze_generator.generate_iterative())
        while True:
            try:
                for _ in range(maze_generator.suggested_iteration_size):
                    maze = next(mazes)
                print("\033[2J\033[H")  # clear screen
                print(ascii_maze_with_path(maze, "", wall='▒', space='·'))
                print()
                time.sleep(0.05)
            except StopIteration:
                break

    # solve maze using BFS and animate the searched paths
    bfs_solver = BreadthFirstSolver()
    path = ""
    for path in bfs_solver.solve_generator(maze):
        print("\033[2J\033[H")  # clear screen
        print(ascii_maze_with_tags(maze, wall='▒', space='·'))
        print()
        time.sleep(0.02)

    print("BFS final solution:\n  ", path or "<no solution found>")

    # solve maze using DFS and animate the searched paths
    # dfs_solver = DepthFirstSolver()
    # path = ""
    # for path in dfs_solver.solve_generator(maze):
    #     print("\033[2J\033[H")      # clear screen
    #     print(ascii_maze_with_path(maze, path, wall='▒', space='·'))
    #     print()
    #     time.sleep(0.02)
    #
    # print("DFS final solution:\n  ", path or "<no solution found>")

    # solve maze in one go using Depth First Search:
    dfs_solver = DepthFirstSolver()
    path, iterations = dfs_solver.solve(maze)
    print("\nDFS solution found in one go:\n  ", path or "<no solution found>")
    print("  this took", iterations, "iterations.")

    # solve maze in one go using Breadth First Search:
    bfs_solver = BreadthFirstSolver()
    path, iterations = bfs_solver.solve(maze)
    print("\nBFS solution found in one go:\n  ", path or "<no solution found>")
    print("  this took", iterations, "iterations.")
