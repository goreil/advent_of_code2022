import sys

# Advent of Code

#     A
#    AAA
#   AAAAA
#  AAAAAAA
#   O # X
#     # 
#
# Year: 2022
# Day: 15
# Name: Beacon Exclusion Zone
 

def distance(a, b):
    """
    returns the manhattan distance between :a and :b
    :a and :b should both be pairs of integers
    """
    # |a.x - b.x| + |a.y - b.y|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_easy(data):
    """
    Solve the easy puzzle of day 15 of AoC 2022 for given (parsed) input.
    """
    # The idea is to "walk" from the center of each sensor to the y-coordinate we are intersted in (straight up or down).
    # If we cannot reach this y-position from the sensor, before we walk further than the distance to its beacon, we can ignore this sensor.
    # If we reach the y-position, we have some amount of manhattan distance left, that we can walk straight left or right (or we have zero left, but then just a single x-coordinate for the y-coordinate is covered by this sensor).
    # We can get the segment of x-coordinates that are covered, as the segment [sensor_x - remaining_distance, sensor_x + remaining_distance] (Both bounds included).
    # When we have computed all of these line segments, we need to ignore points that are on multiple segments. Thus, the length of the union of these segments is (almost) the result.
    # Now one thing we have to be careful with is that there may be beacons with the y position we are interested in. For each (unique) such beacon, we must subtract one from the result.
    
    # we get the sensors (position, manhattan distance) and the beacons (set of positions)
    sensors, beacons = data
    
    # y-coordinate to check
    y = 2000000
    
    # list of one-dimensional line segments (start, end)
    lines = list()
      
    # iterate over all sensors
    for pos,radius in sensors:
        # calculate remaining distance for interesting y coordinate
        delta = radius - abs(pos[1] - y)
        # if we cannot even reach the y-coordinate from this sensor (because the beacon is too close), this sensor is not interesting
        if delta < 0:
            continue
        # add the line segment of x-coordinates covered by this sensor on the interesting y-coordinate
        lines.append((pos[0] - delta, pos[0] + delta))
    
    # sort the line segments. This makes it easier to deal with the overlap of multiple segments
    lines.sort()
    
    # start and end of the current line segment
    start, end = lines[0]
    # length of the first line segment
    length = end - start + 1
    # iterate over remaining line segments
    for new_start, new_end in lines[1:]:
        # if next segment is fully contained in last segment, look at the next immediately
        if end >= new_end:
            continue
        # if segment overlaps with last segment, adjust start of segment to be right after end of last segment
        if end >= new_start:
            new_start += (end - new_start) + 1
        # add length of segment to total length
        length += new_end - new_start + 1
        # make sure to use the segments bounds for overlap checking with the next segment
        start, end = new_start, new_end
    
    # return the total length minus the amount of beacons on the intersting y position
    return length - len(set(bx for bx,by in beacons if by == y))
    
    
class DiagonalLine:
    """
    Represents a two-dimensional diagonal line.
    The line consists of two points (x1, y1) and (x2, y2) where x1 <= x2 and x2 - x1 = abs(y2 - y1).
    Since we only have to deal with such lines, intersecting them is pretty easy (though my code for intersecting is not nice ...)
    """
    
    def __init__(self, x1, y1, x2, y2):
        # if the values are passed in the wrong order (we want x1 <= x2), switch them around
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        # x coordinate of first point
        self.x1 = x1
        # y coordinate of first point
        self.y1 = y1
        # x coordinate of second point
        self.x2 = x2
        # y coordinate of second point
        self.y2 = y2
        
    def is_ascending(self):
        """
        checks whether the y coordinates are increasing when walking from :x1 to :x2 on the line
        """
        return self.y2 > self.y1
        
    def contains(self, x, y):
        """
        checks whether the point (:x, :y) is on this line
        """
        # the :x coordinate must be between :x1 and :x2. :y must be between :y1 and :y2, but we don't know whether :y1 or :y2 is bigger
        return self.x1 <= x <= self.x2 and (self.y1 <= y <= self.y2 or self.y2 <= y <= self.y1)
        
    def get_intersection(self, line):
        """
        returns the intersection point of this line with another line.
        If the lines are parallel (even if they are overlapping), or do not intersect, None is returned
        """
        
        # make sure one of the lines is a downward diagonal and one is an upward diagonal.
        # Otherwise, they do not intersect
        if self.is_ascending() != line.is_ascending():
        
            # dirty hack: we want to only consider the case where self is ascending and line is descending
            if not self.is_ascending():
                return line.get_intersection(self)
                
           
            # self is ascending, line is decending
            
            # calculate (m + n, m - n), where the intersection point S = (x1 - m, y1 - m).
            a, b = (self.x1 - line.x1, self.y1 - line.y1)
            # (m + n) + (m - n) = 2m
            #    a    +    b    = 2m
            # --> m = ( a + b ) // 2
            m = (a + b) // 2
            # calculate coordinates of intersection point
            s_x, s_y = (self.x1 - m, self.y1 - m)
            
            # check whether the intersection point is on the diagonal.
            # This is required since we calculate the intersection point for diagonals of infinite length.
            # However, our diagonals are limited in length and may not intersect.
            if self.contains(s_x, s_y):
                # The point is on a diagonal (this also gurantees it is on the other diagonal), so we can return it
                return (s_x, s_y)
        
        # Lines do not intersect, so no point is returned
        return None

        
def solve_hard(data):
    """
    solve the hard puzzle of day 15 of AoC 2022 for given (parsed) input.
    """
    # To solve this puzzle, the idea is to convert the outline of each sensor into diagonals.
    # Then we calculate the intersection of each diagonal with each other diagonal (corners between two connected sensor outlines will also be considered intersections).
    # With these intersections, we can find points, that have four intersections directly around them.
    # The point we are looking for is neccesarily such a point:
    #  Imagine a polygon where we join all the areas covered by sensors. 
    #  This polygon has a single hole, which is the point we are looking for.
    #  This single hole is surrounded by four corners.
    #  To get corners during polygon conbination, there must either be a corner initially (which we treat as intersection), or two lines must intersect (which we also treat as intersection)
    # When we have found such a point, we make sure that it is really not in range for any of the sensors (as this condition is necessary, but not sufficient).
    
    # all lines making up the outlines of sensor areas
    lines = list()
    
    # we get the sensors (position, manhattan distance) and the beacons (set of positions)
    sensors, beacons = data
    
    # iterate over all sensors
    for pos, radius in sensors:
        # the outline of the sensors is a square (rotated 45°)
        # we just add lines from each edge to the next:
        # 
        #      1+2
        #     1   2
        #   1       2
        #  1+4     2+3
        #   4       3
        #     4   3
        #      3+4
        #
        # left to top (1)
        lines.append(DiagonalLine(pos[0] - radius, pos[1], pos[0], pos[1] - radius))
        # top to right (2)
        lines.append(DiagonalLine(pos[0], pos[1] - radius, pos[0] + radius, pos[1]))
        # right to bottom (3)
        lines.append(DiagonalLine(pos[0] + radius, pos[1], pos[0], pos[1] + radius))
        # bottom to left (4)
        lines.append(DiagonalLine(pos[0], pos[1] + radius, pos[0] - radius, pos[1]))
    
    # set of all intersections (between any of the lines).
    # We use a set since these intersections may not be unique.
    # Also, we want to check in O(1), whether a point is an intersection or not.
    intersections = set()
    
    # iterate over all pairs of lines (each pair is only encountered one, reflexive pairs are not iterated over)
    for i in range(len(lines)):
        line1 = lines[i]
        for j in range(i, len(lines)):
            line2 = lines[j]
            # check whether these two lines intersect
            if intersection := line1.get_intersection(line2):
                # if they do, add their intersection to the set of intersections
                intersections.add(intersection)
    
    # iterate over all intersection points
    for x,y in intersections:
        # since the point we are looking for is surrounded by intersections from all sides, we can just assume it is the point to the right of :x :y
        rx = x + 1
        ry = y
        # check whether the point is surrounded by intersections on all other sides (left, bottom, top)
        if ((rx - 1, ry) in intersections) and ((rx, ry + 1) in intersections) and ((rx, ry - 1) in intersections):
            # iterate over all sensors
            for pos, dist in sensors:
                # if the point is in reach of some sensor, it is not the point we are looking for
                if distance(pos, (rx, ry)) <= dist:
                    break
            else:
                # if the loop was exited (by break), the point is indeed not covered by any sensor. Thus, we can calculate the thingy and return it.
                return rx * 4000000 + ry
    
    
def parse_input(raw_data):
    """
    convert input of the day into format usable by the program.
    """
    # list with all sensors
    sensors = []
    # set of all beacon positions
    beacons = set()
    # iterate over all non-empty lines
    for line in [l for l in raw_data.split("\n") if l]:
        # split input at "="
        sp = line.split("=")
        # extract sensor position
        sensor = (int(sp[1].split(",")[0]), int(sp[2].split(":")[0]))
        # extract beacon position
        beacon = (int(sp[3].split(",")[0]), int(sp[4]))
        
        # create Sensor and add it to :sensors
        sensors.append((sensor, distance(sensor, beacon)))
        # add coordinates of beacon to :beacons
        beacons.add(beacon)
    
    # return the list of sensors and beacon positions
    return sensors, beacons
    
    
if __name__ == "__main__":
    """
    solve easy and hard challenge with input from file 'day15.txt'.
    """
    input_path = sys.argv[1] if len(sys.argv) > 1 else "day15.txt"
    with open(input_path, "r") as f:
        raw_data = f.read()
    # input is parsed twice so that modifications done by the solution for the easy challenge
    #  don't propagate to the input for the hard challenge
    print("Easy: " + repr(solve_easy(parse_input(raw_data))))
    print("Hard: " + repr(solve_hard(parse_input(raw_data))))
