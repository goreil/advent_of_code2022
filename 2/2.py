import sys
ROCK, PAPER, SCISSORS = 1, 2, 3
valueof = {"X": ROCK, "Y": PAPER, "Z" : SCISSORS, "A": ROCK, "B" : PAPER, "C" : SCISSORS}
beats = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}

def round_points(opponent, player):
    if opponent == player:
        return 3
    elif beats[player] == opponent:
        return 6
    else:
        return 0

task1 = 0
task2 = 0
for l in sys.stdin:
    if l.strip() == "":
        continue
    a,b = l.split()
    # Task 1
    task1 += valueof[b]
    task1 += round_points(valueof[a], valueof[b])
    
    # Task 2
    if b == "X": # need to lose
        c = beats[valueof[a]]
    elif b == "Y":
        c = valueof[a]
    elif b == "Z":
        c = beats[beats[valueof[a]]]

    task2 += c
    task2 += round_points(valueof[a], c)

print("Task1: ", task1)
print("Task2: ", task2)