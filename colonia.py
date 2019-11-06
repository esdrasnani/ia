import pants
import math
import random


#!/usr/bin/python3
import time
import math
import argparse
import sys
from datetime import timedelta
import numpy as np
from pants import World, Edge
from pants import Solver



nodes = [(1,4,3,4),(7,3,5,8)]

notas_recursos = [
        [8,	8,	6,	3,	9,	8],
        [10,1,	5,	10,	2,	9],
        [7,	3,	4,	1,	1,	6],
        [5,	4,	2,	3,	1,	7],
        [4,	5,	8,	1,	1,	7],
        [3,	7,	1,	1,	2,	5],
        [1,	1,	4,	1,	8,	1],
        [1,	9,	8,	8,	6,	2],
        [1,	1,	8,	6,	1,	9],
        [3,	1,	1,	1,	1,	2]]

projetos = [
        [0,	10, 1],
        [3,	9, 2],
        [4,	8, 1],
        [1,	7, 3],
        [2,	6, 3],
        [5,	1, 3],
        [1,	2, 2],
        [3,	3, 2],
        [2,	4, 3],
        [4,	5, 1]]


TEST_COORDS_33 = [[0.80,	0.67,	1.13,	3.43,	3.00,	24.00,	8.00,	6.00,	4.50,	1.80],
[1.00,	2.22,	0.25,	0.43,	2.50,	27.00,	1.00,	1.33,	3.75,	0.40],
[0.70,	0.22,	0.13,	1.29,	2.00,	18.00,	3.00,	0.67,	3.00,	0.20],
[0.50,	0.67,	0.13,	1.71,	1.00,	21.00,	4.00,	0.67,	1.50,	0.20],
[0.40,	0.22,	0.13,	2.14,	4.00,	21.00,	5.00,	0.67,	6.00,	0.20],
[0.30,	0.22,	0.25,	3.00,	0.00,	15.00,	7.00,	1.33,	0.00,	0.40],
[0.00,	0.22,	1.00,	0.43,	2.00,	3.00,	1.00,	5.33,	3.00,	1.60],
[0.00,	1.78,	0.75,	3.86,	4.00,	6.00,	9.00,	4.00,	6.00,	1.20],
[0.10,	1.33,	0.00,	0.43,	4.00,	27.00,	1.00,	0.00,	6.00,	0.00],
[0.30,	0.22,	0.00,	0.43,	0.50,	6.00,	1.00,	0.00,	0.75,	0.00]]

TEST_COORDS_33 = np.array(TEST_COORDS_33, dtype=np.float64)

TEST_COORDS_33 = TEST_COORDS_33.T
TEST_COORDS_33 = tuple(map(tuple, TEST_COORDS_33))

"""
# Real-world latitude longitude coordinates.
TEST_COORDS_33 = [
    (34.021150, -84.267249), (34.021342, -84.363437), (34.022585, -84.362150),
    (34.022718, -84.361903), (34.023101, -84.362980), (34.024302, -84.163820),
    (34.044915, -84.255772), (34.045483, -84.221723), (34.046006, -84.225258),
    (34.048194, -84.262126), (34.048312, -84.208885), (34.048679, -84.224917),
    (34.049510, -84.226327), (34.051529, -84.218865), (34.055487, -84.217882),
    (34.056326, -84.200580), (34.059412, -84.216757), (34.060164, -84.242514),
    (34.060461, -84.237402), (34.061281, -84.334798), (34.063814, -84.225499),
    (34.061468, -84.334830), (34.061518, -84.243566), (34.062461, -84.240155),
    (34.064489, -84.225060), (34.066471, -84.217717), (34.068455, -84.283782),
    (34.068647, -84.283569), (34.071628, -84.265784), (34.105840, -84.216670),
    (34.109645, -84.177031), (34.116852, -84.163971), (34.118162, -84.163304)
]
"""
# 45-45-90 triangle with unit length legs.
TEST_COORDS_3 = [
    (0, 0), (1, 0), (0, 1)
]

# Unit square with diagonals.
TEST_COORDS_4 = [
    (0, 0), (1, 0), (0, 1), (1, 1)
]

# Same as above except with additional node in center of left edge.
TEST_COORDS_5 = [
    (0, 0), (1, 0), (0, 1), (1, 1), (0, 0.5)
]


def dist(a, b):
    """Return the distance between two points represeted as a 2-tuple."""
    return math.sqrt((a[9] - b[9]) ** 2 + (a[8] - b[8]) ** 2 + (a[7] - b[7]) ** 2 + (a[6] - b[6]) ** 2 + (a[5] - b[5]) ** 2 + (a[4] - b[4]) ** 2 + (a[3] - b[3]) ** 2 + (a[2] - b[2]) ** 2 + (a[1] - b[1]) ** 2 + (a[0] - b[0]) ** 2)

def run_demo(nodes, *args, **kwargs):
    print(kwargs)
    world = World(nodes, dist)
    solver = Solver(**kwargs)

    solver_setting_report_format = "\n".join([
        "Solver settings:",
        "limit={w.limit}",
        "rho={w.rho}, Q={w.q}",
        "alpha={w.alpha}, beta={w.beta}",
        "elite={w.elite}"
        ])

    print(solver_setting_report_format.format(w=solver))
    
    columns = "{!s:<25}\t{:<25}"
    divider = "-" * (25 + 25)
    header = columns.format("Time Elapsed", "Distance")
    columns = columns.replace('<', '>', 1)
    
    print()
    print(header)
    print(divider)
    
    fastest = None
    start_time = time.time()
    for i, ant in enumerate(solver.solutions(world)):
        fastest = ant
        fastest_time = timedelta(seconds=(time.time() - start_time))
        print(columns.format(fastest_time, ant.distance))
    total_time = timedelta(seconds=(time.time() - start_time))
    
    print(divider)
    print("Best solution:")
    for i, n in zip(fastest.visited, fastest.tour):
        print("  {:>8} = {}".format(i, n))
    
    print("Solution length: {}".format(fastest.distance))
    print("Found at {} out of {} seconds.".format(fastest_time, total_time))
    

if __name__ == '__main__':
    epilog = "\n".join([
        'For best results:',
        '  * 0.5 <= A <= 1',
        '  * 1.0 <= B <= 5',
        '  * A < B',
        '  * L >= 2000',
        '  * N > 1',
        '',
        ('For more information, please visit '
            'https://github.com/rhgrant10/Pants.')
        ])
    
    parser = argparse.ArgumentParser(
        description='Script that demos the ACO-Pants package.',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    
    parser.add_argument(
        '-V', '--version', 
        action='version',
        version='%(prog)s 0.5.1',
        )
    parser.add_argument(
        '-a', '--alpha', 
        type=float, default=1,
        help='relative importance placed on pheromones; default=%(default)s',
        metavar='A'
        )
    parser.add_argument(
        '-b', '--beta', 
        type=float, default=1,
        help='relative importance placed on distances; default=%(default)s',
        metavar='B'
        )
    parser.add_argument(
        '-l', '--limit', 
        type=int, default=1000,
        help='number of iterations to perform; default=%(default)s',
        metavar='L'
        )
    parser.add_argument(
        '-p', '--rho', 
        type=float, default=0.8,
        help=('ratio of evaporated pheromone (0 <= P <= 1); '
            'default=%(default)s'),
        metavar='P'
        )
    parser.add_argument(
        '-e', '--elite', 
        type=float, default=0.5,
        help='ratio of elite ant\'s pheromone; default=%(default)s',
            metavar='E'
        )
    parser.add_argument(
        '-q', '--Q', 
        type=float, default=1,
        help=('total pheromone capacity of each ant (Q > 0); '
            'default=%(default)s'),
        metavar='Q'
        )
    parser.add_argument(
        '-t', '--t0', 
        type=float, default=0.01,
        help=('initial amount of pheromone on every edge (T > 0); '
            'default=%(default)s'),
        metavar='T'
        )
    parser.add_argument(
        '-c', '--count', dest='ant_count',
        type=int, default=10, 
        help=('number of ants used in each iteration (N > 0); '
            'default=%(default)s'),
        metavar='N'
        )
    parser.add_argument(
        '-d', '--dataset', 
        type=int, default=33, choices=[3, 4, 5, 33],
        help='specify a particular set of demo data; default=%(default)s',
        metavar='D'
        )
        
    args = parser.parse_args()
    
    nodes = {
        3: TEST_COORDS_3,
        4: TEST_COORDS_4,
        5: TEST_COORDS_5,
        33: TEST_COORDS_33
    }[args.dataset]

    run_demo(nodes, **args.__dict__)


'''
nodes = []
for _ in range(20):
  x = random.uniform(-10, 10)
  y = random.uniform(-10, 10)
  nodes.append((x, y))

def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))


world = pants.World(nodes, euclidean)
solver = pants.Solver()
    
solution = solver.solve(world)
#solutions = solver.solutions(world)

print(solution.distance)
print(solution.tour)    # Nodes visited in order
print(solution.path)    # Edges taken in order
        # or
best = float("inf")
for solution in solutions:
  assert solution.distance < best
  best = solution.distance
'''