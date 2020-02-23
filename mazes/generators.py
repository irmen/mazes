import random
from abc import ABC, abstractmethod
from typing import Generator, Tuple, List

from .maze import Cell, Maze, dxdy, opposite_direction

__all__ = ["DepthFirstGenerator", "HuntAndKillGenerator"]


# TODO make more generators, see https://www.jamisbuck.org/mazes/


class MazeGenerator(ABC):
    @abstractmethod
    def generate(self) -> Maze:
        pass

    @abstractmethod
    def generate_iterative(self) -> Generator[Maze, None, None]:
        pass


class DepthFirstGenerator(MazeGenerator):
    """
    Recursive Depth-first based approach of making the paths.
    Mazes usually consist of long paths with fairly low branching.
    Requires a stack to keep track of where it's been.
    """
    suggested_iteration_size = 20

    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.cells = [[Cell() for _ in range(columns)] for _ in range(rows)]

    def generate(self) -> Maze:
        maze = Maze([[]])
        for maze in self.generate_iterative():
            pass
        return maze

    def generate_iterative(self) -> Generator[Maze, None, None]:
        stack = []
        self.cells[0][0].open = True
        stack.append((0, 0))
        while stack:
            yield Maze(self.cells)
            column, row = stack.pop()
            unvisited_neighbors = [(direction, cell)
                                   for direction, cell in self.neighbors(column, row) if not cell.open]
            if unvisited_neighbors:
                stack.append((column, row))
                direction, neighbor = random.choice(unvisited_neighbors)
                self.cells[row][column].doors += direction
                neighbor.doors += opposite_direction[direction]
                neighbor.open = True
                next_col = column + dxdy[direction][0]
                next_row = row + dxdy[direction][1]
                stack.append((next_col, next_row))

    def neighbors(self, column: int, row: int) -> List[Tuple[str, Cell]]:
        n = []
        if row > 0:
            n.append(("n", self.cells[row - 1][column]))
        if column < self.columns - 1:
            n.append(("e", self.cells[row][column + 1]))
        if row < self.rows - 1:
            n.append(("s", self.cells[row + 1][column]))
        if column > 0:
            n.append(("w", self.cells[row][column - 1]))
        return n


class HuntAndKillGenerator(MazeGenerator):
    """
    Similar to a depth-first based approach of making the paths,
    this generator does not require a stack. It can create huge mazes
    without risking a stack overflow or memory issue.

    It has the problem though that the mazes it generates now
    tend to have the solution path running across the top right and
    then down, instead of being more well formed/spread out.
    For smaller mazes this is less noticeable though. (say 20x20 or less)
    """

    suggested_iteration_size = 1

    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.cells = [[Cell() for _ in range(columns)] for _ in range(rows)]
        self._previous_row_hunted = 0

    def generate(self) -> Maze:
        maze = Maze([[]])
        for maze in self.generate_iterative():
            pass
        return maze

    def generate_iterative(self) -> Generator[Maze, None, None]:
        # because the maze is constructed from top to bottom,
        # the solution tends to be in the top and right part of the maze.
        col = self.columns - 1
        row = 0  # must start at first row
        while col >= 0:
            yield Maze(self.cells)
            self.carve(col, row)
            col, row = self.find_next_unvisited()
        yield Maze(self.cells)

    def find_next_unvisited(self) -> Tuple[int, int]:
        for row in range(self._previous_row_hunted, self.rows):
            rowcells = self.cells[row]
            for column, cell in enumerate(rowcells):
                if not cell.open:
                    accessible_neighbors = [(direction, n)
                                            for direction, n in self.neighbors(column, row) if n.open]
                    if accessible_neighbors:
                        # carve a path to one of our open neighbors
                        direction, neighbor = random.choice(accessible_neighbors)
                        cell.doors += direction
                        neighbor.doors += opposite_direction[direction]
                        self._previous_row_hunted = row
                        return column, row
        return -1, -1

    def neighbors(self, column: int, row: int) -> List[Tuple[str, Cell]]:
        n = []
        if row > 0:
            n.append(("n", self.cells[row - 1][column]))
        if column < self.columns - 1:
            n.append(("e", self.cells[row][column + 1]))
        if row < self.rows - 1:
            n.append(("s", self.cells[row + 1][column]))
        if column > 0:
            n.append(("w", self.cells[row][column - 1]))
        return n

    def carve(self, column: int, row: int) -> None:
        while True:
            cell = self.cells[row][column]
            assert not cell.open
            cell.open = True
            neighbors = self.neighbors(column, row)
            unvisited_neighbors = [(direction, cell) for direction, cell in neighbors if not cell.open]
            if not unvisited_neighbors:
                return
            direction, next_cell = random.choice(unvisited_neighbors)
            cell.doors += direction
            next_cell.doors += opposite_direction[direction]
            dx, dy = dxdy[direction]
            column += dx
            row += dy
