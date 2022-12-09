#!/bin/env python3
import sys
import numpy as np
from util import *
# This challenge has been brought to you with numpy magic
chain = [np.array((0,0)) for _ in range(10)] 
dir_lookup = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
T_Positions = {(0,0)}
Last_Postions = {(0,0)}

for l in sys.stdin:
    l = l.strip()
    if l == "": continue
    
    direction, amount = dir_lookup[first(l)], int(second(l))

    for _ in range(amount):
        chain[0] += direction
        for i in range(1, len(chain)):
            diff = chain[i-1] - chain[i]
            # If any diff in one direction is 2, drag the chain
            if sum(abs(diff) == 2):
                chain[i] += np.sign(diff)
            
                
                
        T_Positions.add(tuple(chain[1]))
        Last_Postions.add(tuple(chain[-1]))
    # Good luck!

task1 = len(T_Positions)
task2 = len(Last_Postions)
print("Task1:", task1)
print("Task2:" , task2)