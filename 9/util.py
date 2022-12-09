import re
def ints(s):
    return [int(x) for x in re.findall(r'(\d+)', s)]

def first(s, sep = " "):
    return s.split(sep)[0]

def second(s, sep = " "):
    return s.split(sep)[1]