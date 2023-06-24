#!/bin/env python3
import sys
from util import *

out = set()
beacons = set()
target_y = 2000000
for l in sys.stdin:
    l = l.strip()
    # Enter code here:
    x, y, w, h = ints(l)
    # Add beacons:
    if h == target_y:
        beacons.add(w)
    m_dist = abs(w-x) + abs(h-y)

    # Skip sensor if distance is too large
    if abs(target_y - y) > m_dist:
        continue

    # get range of x values
    leeway = m_dist - abs(target_y - y)
    x_left, x_right = (x-leeway, x+leeway)
    for i in range(x_left, x_right+1):
        out.add(i)

#print(out)
# print lenght of out with beacons removed
print(len(out.difference(beacons)))