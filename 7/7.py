#!/bin/env python3
import re
import sys
def ints(s):
    return [int(x) for x in re.findall(r'(\d+)', s)]

class Tree():
    def __init__(self, name):
        self.name = name
        self.child_values = []
        self.child_trees = []
    
    def size(self):
        return sum(self.child_values) + sum([ct.size() for ct in self.child_trees])
    
    def __str__(self):
        return self.name + "\nChildValues:" + str(self.child_values) + "\nChildTrees: " + str(self.child_trees)

task1 = 0
task2 = 0
main_dir = Tree("/")
current = main_dir

last_dirs = []
for l in sys.stdin:
    
    l = l.strip()
    if l == "$ cd /":
        continue
    # Commands
    if l[0] == "$":
        command =  l.split(" ")[1]
        if command == "ls":
            continue
        if command == "cd":
            dir = l.split(" ")[2]
            if dir == "..":
                current = last_dirs.pop()
            else:
                last_dirs.append(current)
                new_dir = Tree(dir)
                current.child_trees.append(new_dir)
                current = new_dir
       
    # ls output
    else:
        if len(ints(l)) > 0:
            current.child_values.append(ints(l)[0])

# BFS for tree
target = 30000000
current_unused = 70000000 - main_dir.size()
diff = target - current_unused
best = main_dir.size()

to_visit = [main_dir]
while len(to_visit) > 0:
    current = to_visit.pop()
    to_visit += current.child_trees

    # task 1
    if (current.size() < 100000):
        task1 += current.size()
    
    if (current.size() >= diff and current.size() < best):
        best = current.size()

task2 = best
print("Task1: ", task1)
#print(main_dir.size())
#print(diff)
print("Task2:" , task2)