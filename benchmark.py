import time
import random

from mazes.generators import *
from mazes.solvers import *

random.seed(12345)

for generator_class in [HuntAndKillGenerator, DepthFirstGenerator]:
    print("starting", generator_class.__name__)
    start = time.time()
    maze_gen = generator_class(1000, 1000)
    maze_gen.generate()
    print("  generation took", time.time() - start)


maze = DepthFirstGenerator(600, 600).generate()

for solver_class in [BreadthFirstSolver, DepthFirstSolver]:
    print("solving using", solver_class.__name__)
    solver = solver_class()
    start = time.time()
    solution, iterations = solver.solve(maze)
    print("  solution found, length:", len(solution), "iterations:", iterations)
    print("  solving took", time.time()-start)
    start = time.time()
    for iterations, solution in enumerate(solver.solve_generator(maze)):
        pass
    print("  solution found, length:", len(solution), "iterations:", iterations)
    print("  solving using generator took", time.time()-start)
