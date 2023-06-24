#!/bin/env python3
import sys
from util import *

task1 = 0
task2 = 0

X_Values = [0, 1] # Added 0 for proper indexing
for l in sys.stdin:
    l = l.strip()
    if l == "": continue
    if first(l) == "noop":
        X_Values.append(X_Values[-1])
    else:
        X_last = X_Values[-1]
        X_Values += [X_last, X_last + int(second(l))]

task1 = sum([i * x for i,x in enumerate(X_Values)][20::40])
output = []
for i, x in enumerate(X_Values[1:]):

    if i % 40 in (x-1, x, x+1):
        o = "#"
    else:
        o = " "
    output.append(o)
    if i in range(39,241,40):
        output.append("\n")

task2 = "".join(output)
print("Task1: ", task1)
print("Task2:\n")
print(task2)