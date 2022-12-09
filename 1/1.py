text = open("input").read()

current = 0
top_3 = [0,0,0]

for line in text.split("\n"):
    if line.strip() == "":
        top_3.append(current)
        top_3.sort(reverse=True)
        top_3.pop()
        current = 0
    else:
        current += int(line)

top_3.append(current)
top_3.sort(reverse=True)

print("Solution to 1:", top_3[0])
print("Solution to 2:", sum(top_3[:3]))
