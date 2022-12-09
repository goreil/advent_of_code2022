#!/bin/env python3
import re
import sys
def ints(s):
    return [int(x) for x in re.findall(r'(\d+)', s)]

task1 = 0
task2 = 0
forest = []
for l in sys.stdin:
    l = l.strip()
    l = list(map(int,list(l)))
    forest.append(l)

visible = [[False for x in row] for row in forest]
# From left
for i in range(len(visible)):
    visible[i][0] = True
    cur_max = forest[i][0]
    for j in range(1, len(visible[i])):
        if forest[i][j] > cur_max:
            cur_max = forest[i][j]
            visible[i][j] = True
    

# From right 
for i in range(len(visible)):
    visible[i][-1] = True
    cur_max = forest[i][-1]
    for j in range(len(visible[i]) - 1, -1, -1):
        if forest[i][j] > cur_max:
            cur_max = forest[i][j]
            visible[i][j] = True


# From up
for i in range(len(visible[0])):
    visible[0][i] = True
    cur_max = forest[0][i]
    for j in range(1, len(visible[0])):
        if forest[j][i] > cur_max:
            cur_max = forest[j][i]
            visible[j][i] = True

# From right 
for i in range(len(visible[0])):
    visible[-1][i] = True
    cur_max = forest[-1][i]
    for j in range(len(visible[0]) - 1, -1, -1):
        if forest[j][i] > cur_max:
            cur_max = forest[j][i]
            visible[j][i] = True

# Part 2
for i in range(1, len(forest) - 1):
    for j in range(1, len(forest[i]) -1):
        start_tree = forest[i][j]
        # left
        left = forest[i][:j][::-1]
        right = forest[i][j+1:]
        up = [forest[x][j] for x in range(i-1, -1, -1)]
        down = [forest[x][j] for x in range(i+1, len(forest))]
        sol = 1
        
        for row in (left,right,up,down):
            count = 0
            for x in row:
                count += 1
                if x >= start_tree:
                    break
            sol *= count
        #print(i,j, sol)
        task2 = max(task2, sol)

task1 = sum(sum(visible, []))
print("Task1: ", task1)
print("Task2:" , task2)