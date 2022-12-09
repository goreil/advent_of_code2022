import sys

def get_priority(item):

    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27

task_1 = 0
task_2 = 0
group = []
for l in sys.stdin:
    # For task 1
    l = l.strip()
    mid = len(l)//2
    a, b = l[:mid], l[mid:]
    #print(a, b)
    duplicate = set(a).intersection(set(b)).pop()
    
    task_1 += get_priority(duplicate)

    # For task 2
    group.append(l)
    if len(group) == 3:
        a,b,c = group
        group = []
        duplicate = set(a).intersection(set(b)).intersection(set(c)).pop()
        task_2 += get_priority(duplicate)

print(task_1)
print(task_2)

