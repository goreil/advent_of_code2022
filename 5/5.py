import sys
import re
from copy import deepcopy
crates = [[]] * 9
boxes = None
nr_crates = 9

state = "CRATES"
for l in sys.stdin:
    # Get crates
    if state == "CRATES":
        c = list(l[1::4]) # Get the contents
        for i, ele in enumerate(c):
            if ele == "1":
                state = "MOVE"
                nr_crates = int(l.strip()[-1]) # Only works with 1 digit number
                boxes = deepcopy(crates)
                break
            if ele == " ":
                continue
            crates[i] = [ele] + crates[i]

    elif state == "MOVE":
        if l.strip() == "":
            continue
        amount, src, dest = map(int, re.findall("(\d+)", l)) # Get numbers from line
        src, dest = src - 1, dest - 1 # correct indexing
        new_boxes = []
        for _ in range(amount):
            crates[dest].append(crates[src].pop())
            new_boxes = [boxes[src].pop()] + new_boxes

        boxes[dest] += new_boxes

    #print(crates)
    #print(boxes)

task1 = []
task2 = []
for i in range(nr_crates):
    task1.append(crates[i].pop())
    task2.append(boxes[i].pop())

print("".join(task1))
print("".join(task2))
