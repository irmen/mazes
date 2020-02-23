from abc import ABC, abstractmethod
from typing import Generator, Set, Tuple, Mapping
from mazes.maze import Maze, dxdy

# TODO: store the path information in the cells in the maze (pointing back to the previous cell) rather than adding it onto huge strings


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze) -> Tuple[str, int]:
        pass

    @abstractmethod
    def solve_generator(self, maze) -> Generator[str, None, None]:
        pass

    def _walkback(self, previous_links: Mapping[Tuple[int, int], Tuple[int, int]], x: int, y: int) -> str:
        # determines the solution path by 'walking back' to the start point (and reversing that path)
        path = ""
        while True:
            px, py = previous_links[(x, y)]
            if py < y:
                path += "s"
            elif py > y:
                path += "n"
            elif px < x:
                path += "e"
            elif px > x:
                path += "w"
            else:
                return path[::-1]
            x, y = px, py


class BreadthFirstSolver(MazeSolver):
    def solve(self, maze) -> Tuple[str, int]:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # search strategy is breadth-first.
        paths = [(0, 0, "")]
        discovered = {(0, 0)}
        iterations = 0
        while paths:
            x, y, path = paths.pop(0)
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                return path, iterations
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    paths.append((new_x, new_y, path + direction))
                    discovered.add((new_x, new_y))
            iterations += 1
        return "", iterations

    def solve_generator(self, maze) -> Generator[str, None, None]:
        # Assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # The last path returned is the solution.
        paths = [(0, 0, "")]
        discovered = {(0, 0)}
        while paths:
            x, y, path = paths.pop(0)
            maze.cells[y][x].tag = len(path)
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                yield path
                return
            yield path
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    paths.append((new_x, new_y, path + direction))
                    discovered.add((new_x, new_y))


class DepthFirstSolver(MazeSolver):
    def solve(self, maze: Maze) -> Tuple[str, int]:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # search strategy is depth-first.
        discovered = {(0, 0): (0, 0)}       # remembers its path-previous node as well
        stack = [(0, 0)]
        iterations = 0
        while stack:
            x, y = stack.pop()
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                return self._walkback(discovered, x, y), iterations
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    stack.append((new_x, new_y))
                    discovered[(new_x, new_y)] = (x, y)
            iterations += 1
        return "", iterations

    def solve_generator(self, maze) -> Generator[str, None, None]:
        # Assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # Iteratively look until a solution is found while returning
        # All the intermediate paths being followed. Because of this,
        # it's not very useful to attempt to optimize out the intermediate path strings.
        # The last path returned is the solution.
        discovered = {(0, 0)}
        stack = [(0, 0, "")]
        while stack:
            x, y, path = stack.pop()
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                yield path
                return
            yield path
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dx, dy = dxdy[direction]
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in discovered:
                    stack.append((new_x, new_y, path+direction))
                    discovered.add((new_x, new_y))
