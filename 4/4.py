import sys

count = 0
task2 = 0
for line in sys.stdin:
    a, b = [x.split("-") for x in line.split(",")]
    a0, a1, b0, b1 = [int(x) for x in sum([a,b], [])]
    #print(a0,a1,b0,b1)
    count += ((a0 <= b0) and (a1 >= b1)) or ((b0 <= a0) and (b1 >= a1))

    # Task2
    task2 += not ((a1 < b0) or (b1 < a0))
    #print(a,b, task2)

print("Task1:", count)
print("Task2:", task2)
