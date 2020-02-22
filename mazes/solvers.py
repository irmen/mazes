from typing import Generator, Set, Tuple
from mazes.maze import Maze, dxdy


class BreadthFirstSolver:
    def solve_generator(self, maze) -> Generator[str, None, None]:
        # Assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # The last path returned is the solution.
        paths = {(0, 0, "")}
        discovered: Set[Tuple[int, int]] = set()
        while paths:
            x, y, path = paths.pop()
            maze.cells[y][x].tag = len(path)
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                yield path
                return
            discovered.add((x, y))
            yield path
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    paths.add((new_x, new_y, path + direction))
        yield ""  # no solution found

    def solve(self, maze) -> Tuple[str, int]:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # search strategy is breadth-first.
        paths = {(0, 0, "")}
        discovered: Set[Tuple[int, int]] = set()
        iterations = 0
        while paths:
            x, y, path = paths.pop()
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                return path, iterations
            discovered.add((x, y))
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    paths.add((new_x, new_y, path + direction))
            iterations += 1
        return "", iterations


class DepthFirstSolver:
    def solve(self, maze: Maze) -> Tuple[str, int]:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # search strategy is depth-first.
        discovered: Set[Tuple[int, int]] = set()
        stack = [("", 0, 0)]
        iterations = 0
        while stack:
            path, x, y = stack.pop()
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                return path, iterations
            discovered.add((x, y))
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    stack.append((path+direction, new_x, new_y))
            iterations += 1
        return "", iterations

    def solve_generator(self, maze) -> Generator[str, None, None]:
        # Assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # Iteratively look until a solution is found while returning
        # all the intermediate paths being followed.
        # The last path returned is the solution.
        discovered: Set[Tuple[int, int]] = set()
        stack = [("", 0, 0)]
        while stack:
            path, x, y = stack.pop()
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                yield path
                return
            discovered.add((x, y))
            yield path
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    stack.append((path+direction, new_x, new_y))
        yield ""  # no solution found
