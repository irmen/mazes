import time
from mazes.generators import *
from mazes.solvers import *


for generator_class in [HuntAndKillGenerator, DepthFirstGenerator]:
    print("starting", generator_class.__name__)
    start = time.time()
    maze_gen = generator_class(1000, 1000)
    maze_gen.generate()
    print("  generation took", time.time()-start)


maze = DepthFirstGenerator(500, 500).generate()

for solver_class in [BreadthFirstSolver, DepthFirstSolver]:
    print("solving using", solver_class.__name__)
    solver = solver_class()
    start = time.time()
    solver.solve(maze)
    print("  solving took", time.time()-start)
