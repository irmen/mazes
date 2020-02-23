from abc import ABC, abstractmethod
from typing import Generator, Set, Tuple
from mazes.maze import Maze, dxdy

# TODO: store the path information in the cells in the maze (pointing back to the previous cell) rather than adding it onto huge strings


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze) -> Tuple[str, int]:
        pass

    @abstractmethod
    def solve_generator(self, maze) -> Generator[str, None, None]:
        pass


class BreadthFirstSolver(MazeSolver):
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


class DepthFirstSolver(MazeSolver):
    def solve(self, maze: Maze) -> Tuple[str, int]:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # search strategy is depth-first.
        discovered: Set[Tuple[int, int]] = set()
        stack = [(0, 0, "")]
        iterations = 0
        while stack:
            x, y, path = stack.pop()
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                return path, iterations
            discovered.add((x, y))
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    stack.append((new_x, new_y, path+direction))
            iterations += 1
        return "", iterations

    def solve_generator(self, maze) -> Generator[str, None, None]:
        # Assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # Iteratively look until a solution is found while returning
        # all the intermediate paths being followed.
        # The last path returned is the solution.
        discovered: Set[Tuple[int, int]] = set()
        stack = [(0, 0, "")]
        while stack:
            x, y, path = stack.pop()
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
                    stack.append((new_x, new_y, path+direction))
