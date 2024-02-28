import math

SWITCH_NUMBER = 9
SIDE = math.ceil(math.sqrt(SWITCH_NUMBER))
switches = [[0 for _ in range(SIDE)] for _ in range(SIDE)]
links = []
switch_cont = 1

for r in range(0, SIDE):
    for c in range(0, SIDE):
        switches[r][c] = switch_cont
        switch_cont += 1
        if c > 0:
            links.append((switches[r][c-1], switches[r][c]))
        if r > 0:
            links.append((switches[r-1][c], switches[r][c]))


print("Switches")
for r in range(0, SIDE):
    print(switches[r])

print("Links:")
print(links)