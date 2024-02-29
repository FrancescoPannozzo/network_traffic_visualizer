""" This is a sketch script """

# tesst aspect ratio
import math
import random

side = math.sqrt(144)

rows = math.ceil(side * 3/4)
cols = int(side * 4/3)

print("rows, cols:", rows, cols)

print("-------------")
# The arcs representing the links connecting the switches (nodes)
links = []
# The link ID counter
switch_number = 5
link_cap = 10
link_id = 1

for i in range(1, switch_number + 1):
    adiacenti_possibili = [s for s in range(1, switch_number+1) if s != i]
    print(f"----- adiacenti possibili per nodo {i}:{adiacenti_possibili}, tot:", len(adiacenti_possibili))
    n_adiacenti = random.randint(1, len(adiacenti_possibili))
    print(f"----- nodo {i} avrà {n_adiacenti} adiacenti")
    for _ in range(1, n_adiacenti+1):
        scelto = random.choice(adiacenti_possibili)
        if sorted([i, scelto]) not in links:
            links.append(sorted([i, scelto]))
        adiacenti_possibili.remove(scelto)


print("..............")
print(sorted(links))
valore = 5
print(type(valore) == "class 'int'")

""" 0: {'hexValue': '#05ff00'}
1: {'hexValue': '#0aff00'}
2: {'hexValue': '#0fff00'}
3: {'hexValue': '#14ff00'}
4: {'hexValue': '#19ff00'}
5: {'hexValue': '#1eff00'}
6: {'hexValue': '#23ff00'}
7: {'hexValue': '#28ff00'}
8: {'hexValue': '#2dff00'}
9: {'hexValue': '#32ff00'}
10: {'hexValue': '#37ff00'}
11: {'hexValue': '#3cff00'}
12: {'hexValue': '#41ff00'}
13: {'hexValue': '#46ff00'}
14: {'hexValue': '#4bff00'}
15: {'hexValue': '#50ff00'}
16: {'hexValue': '#55ff00'}
17: {'hexValue': '#5aff00'}
18: {'hexValue': '#5fff00'}
19: {'hexValue': '#64ff00'}
20: {'hexValue': '#69ff00'}
21: {'hexValue': '#6eff00'}
22: {'hexValue': '#73ff00'}
23: {'hexValue': '#78ff00'}
24: {'hexValue': '#7dff00'}
25: {'hexValue': '#82ff00'}
26: {'hexValue': '#87ff00'}
27: {'hexValue': '#8cff00'}
28: {'hexValue': '#91ff00'}
29: {'hexValue': '#96ff00'}
30: {'hexValue': '#9bff00'}
31: {'hexValue': '#a0ff00'}
32: {'hexValue': '#a5ff00'}
33: {'hexValue': '#aaff00'}
34: {'hexValue': '#afff00'}
35: {'hexValue': '#b4ff00'}
36: {'hexValue': '#b9ff00'}
37: {'hexValue': '#beff00'}
38: {'hexValue': '#c3ff00'}
39: {'hexValue': '#c8ff00'}
40: {'hexValue': '#cdff00'}
41: {'hexValue': '#d2ff00'}
42: {'hexValue': '#d7ff00'}
43: {'hexValue': '#dcff00'}
44: {'hexValue': '#e1ff00'}
45: {'hexValue': '#e6ff00'}
46: {'hexValue': '#ebff00'}
47: {'hexValue': '#f0ff00'}
48: {'hexValue': '#f5ff00'}
49: {'hexValue': '#faff00'}
50: {'hexValue': '#ffff00'}
51: {'hexValue': '#fffa00'}
52: {'hexValue': '#fff500'}
53: {'hexValue': '#fff000'}
54: {'hexValue': '#ffeb00'}
55: {'hexValue': '#ffe600'}
56: {'hexValue': '#ffe100'}
57: {'hexValue': '#ffdc00'}
58: {'hexValue': '#ffd700'}
59: {'hexValue': '#ffd200'}
60: {'hexValue': '#ffcd00'}
61: {'hexValue': '#ffc800'}
62: {'hexValue': '#ffc300'}
63: {'hexValue': '#ffbe00'}
64: {'hexValue': '#ffb900'}
65: {'hexValue': '#ffb400'}
66: {'hexValue': '#ffaf00'}
67: {'hexValue': '#ffaa00'}
68: {'hexValue': '#ffa500'}
69: {'hexValue': '#ffa000'}
70: {'hexValue': '#ff9b00'}
71: {'hexValue': '#ff9600'}
72: {'hexValue': '#ff9100'}
73: {'hexValue': '#ff8c00'}
74: {'hexValue': '#ff8700'}
75: {'hexValue': '#ff8200'}
76: {'hexValue': '#ff7d00'}
77: {'hexValue': '#ff7800'}
78: {'hexValue': '#ff7300'}
79: {'hexValue': '#ff6e00'}
80: {'hexValue': '#ff6900'}
81: {'hexValue': '#ff6400'}
82: {'hexValue': '#ff5f00'}
83: {'hexValue': '#ff5a00'}
84: {'hexValue': '#ff5500'}
85: {'hexValue': '#ff5000'}
86: {'hexValue': '#ff4b00'}
87: {'hexValue': '#ff4600'}
88: {'hexValue': '#ff4100'}
89: {'hexValue': '#ff3c00'}
90: {'hexValue': '#ff3700'}
91: {'hexValue': '#ff3200'}
92: {'hexValue': '#ff2d00'}
93: {'hexValue': '#ff2800'}
94: {'hexValue': '#ff2300'}
95: {'hexValue': '#ff1e00'}
96: {'hexValue': '#ff1900'}
97: {'hexValue': '#ff1400'}
98: {'hexValue': '#ff0f00'}
99: {'hexValue': '#ff0a00'}
100: {'hexValue': '#ff0500'} """