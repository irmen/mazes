import time

from mazes.generators import *
from mazes.solvers import *

maze = DepthFirstGenerator(20, 10).generate()

for solver_class in [BreadthFirstSolver, DepthFirstSolver]:
    print("solving using", solver_class.__name__)
    solver = solver_class()
    start = time.time()
    solution, iterations = solver.solve(maze)
    print("  solving took", time.time() - start, " iterations:", iterations)
    print("  solution:", solution)
