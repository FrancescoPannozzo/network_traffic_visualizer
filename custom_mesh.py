import math


SWITCH_NUMBER = 4
side = math.sqrt(SWITCH_NUMBER)

rows = math.ceil(side * (3/4))
cols = int(side * (4/3))

print("rows, cols:", rows, cols)


#SIDE = math.ceil(math.sqrt(SWITCH_NUMBER))
switches = [[0 for _ in range(cols)] for _ in range(rows)]
links = []
switch_cont = 1

for r in range(0, rows):
    for c in range(0, cols):
        switches[r][c] = switch_cont
        switch_cont += 1
        if c > 0:
            links.append((switches[r][c-1], switches[r][c]))
        if r > 0:
            links.append((switches[r-1][c], switches[r][c]))


print("Switches")
for r in range(0, rows):
    print(switches[r])

print("Links:")
print(links)