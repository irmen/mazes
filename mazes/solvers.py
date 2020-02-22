from typing import Generator, Set, Tuple
from mazes.maze import Maze, dxdy

# class BreadthFirstSolver:
#     def solve(self, maze: Maze) -> str:
#         # assume start cell is at (0, 0) in the top left,
#         # and the exit cell is in the lower right at (numcols-1, numrows-1).
#         # this routine recursively looks until a solution is found and returns that.
#         # search strategy is breadth-first.
#         discovered = set()
#
#         def bfs(paths: Set[str]) -> str:
#
#             if x == maze.num_columns-1 and y == maze.num_rows-1:
#                 return path
#             discovered.add((x, y))


class DepthFirstSolver:
    def solve(self, maze: Maze) -> str:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # search strategy is depth-first.
        discovered: Set[Tuple[int, int]] = set()
        stack = [("", 0, 0)]
        while stack:
            path, x, y = stack.pop()
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                return path
            discovered.add((x, y))
            doors = maze.cells[y][x].doors
            for direction in [d for d in "nesw" if d in doors]:
                dp = dxdy[direction]
                new_posx = x + dp[0]
                new_posy = y + dp[1]
                if (new_posx, new_posy) not in discovered:
                    stack.append((path+direction, new_posx, new_posy))
        return ""

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
                dp = dxdy[direction]
                new_posx = x + dp[0]
                new_posy = y + dp[1]
                if (new_posx, new_posy) not in discovered:
                    stack.append((path+direction, new_posx, new_posy))
        yield ""  # no solution found
