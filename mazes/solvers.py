from typing import Generator, Set, Tuple
from mazes.maze import Maze, dxdy


class DepthFirstSolver:
    def solve(self, maze: Maze) -> str:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # this routine recursively looks until a solution is found and returns that.
        discovered = set()

        def dfs(x: int, y: int, path: str) -> str:
            if x == maze.num_columns-1 and y == maze.num_rows-1:
                return path
            discovered.add((x, y))
            doors = maze.cells[y][x].doors
            for direction in "nesw":
                if direction in doors:
                    dp = dxdy[direction]
                    new_posx = x + dp[0]
                    new_posy = y + dp[1]
                    if (new_posx, new_posy) not in discovered:
                        solution = dfs(new_posx, new_posy, path+direction)
                        if solution:
                            return solution
            return ""

        return dfs(0, 0, "")

    def solve_iterative(self, maze) -> Generator[str, None, None]:
        # assume start cell is at (0, 0) in the top left,
        # and the exit cell is in the lower right at (numcols-1, numrows-1).
        # this routine iteratively looks until a solution is found and returns
        # all the intermediate paths it is following.
        discovered: Set[Tuple[int, int]] = set()
        stack = [("", 0, 0)]
        while stack:
            path, x, y = stack.pop()
            if (x, y) not in discovered:
                yield path
                if x == maze.num_columns-1 and y == maze.num_rows-1:
                    return
                discovered.add((x, y))
                doors = maze.cells[y][x].doors
                for direction in "nesw":
                    if direction in doors:
                        dp = dxdy[direction]
                        new_posx = x + dp[0]
                        new_posy = y + dp[1]
                        stack.append((path+direction, new_posx, new_posy))
        if len(stack) == 0:
            yield ""        # no solution found
