import sys
import os

from scripts.algorithms.perlin import *

project_dir = os.path.dirname(os.path.abspath(__file__))

current_path = os.path.dirname(__file__)
scripts_path = os.path.join(current_path, "scripts")
algorithms_path = os.path.join(scripts_path, "algorithms")
perlin_path = os.path.join(algorithms_path, "perlin.py")

MAP_1 = 'map.txt'
MAP_2 = 'map2.txt'