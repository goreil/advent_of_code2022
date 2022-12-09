import sys

for l in sys.stdin:
    for i in range(len(l)):
        if len(set(l[i:i+4])) == 4:
            print(i+4)
        if len(set(l[i:i+14])) == 14:
            print(i+14)
            break