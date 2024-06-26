
from utils import graphic_visualizer_utils
from datetime import datetime

#colors = graphic_visualizer_utils.traffic_colors_gen_colorblind()

#for _, color in colors.items():
#    print(color)

timestamp1 = "2024-03-22 12:30:00"
print(len(timestamp1))
timestamp2 = "2024-03-22 12:30:00.100000"

print(datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S"))
print(datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f"))

i = 2.1
print(round(i))
i = 2.2
print(round(i))
i = 2.5
print(round(i))
i = 2.6
print(round(i))
i = 2.9
print(round(i))

d = {}
d[1] = {"nome": "Francesco", "cognome":"pan"}
d["pan"] = {"nome": "Francescooooo", "cognome":"paaan"}
d[("A", "B")] = {"nome": "Fra", "cognome":"Pa"}
d[("A", "B")] = {"nome": "F", "cognome":"P"}
d[("B", "A")] = {"nome": "FFF", "cognome":"PPP"}
d[{"C", "D"}] = {"nome": "ccc", "cognome":"ddd"}

print(d)

""" 
{'hexValue': '#fafffa'}
{'hexValue': '#f5fff5'}
{'hexValue': '#f0fff0'}
{'hexValue': '#ebffeb'}
{'hexValue': '#e6ffe6'}
{'hexValue': '#e1ffe1'}
{'hexValue': '#dcffdc'}
{'hexValue': '#d7ffd7'}
{'hexValue': '#d2ffd2'}
{'hexValue': '#cdffcd'}
{'hexValue': '#c8ffc8'}
{'hexValue': '#c3ffc3'}
{'hexValue': '#beffbe'}
{'hexValue': '#b9ffb9'}
{'hexValue': '#b4ffb4'}
{'hexValue': '#afffaf'}
{'hexValue': '#aaffaa'}
{'hexValue': '#a5ffa5'}
{'hexValue': '#a0ffa0'}
{'hexValue': '#9bff9b'}
{'hexValue': '#96ff96'}
{'hexValue': '#91ff91'}
{'hexValue': '#8cff8c'}
{'hexValue': '#87ff87'}
{'hexValue': '#82ff82'}
{'hexValue': '#7dff7d'}
{'hexValue': '#78ff78'}
{'hexValue': '#73ff73'}
{'hexValue': '#6eff6e'}
{'hexValue': '#69ff69'}
{'hexValue': '#64ff64'}
{'hexValue': '#5fff5f'}
{'hexValue': '#5aff5a'}
{'hexValue': '#55ff55'}
{'hexValue': '#50ff50'}
{'hexValue': '#4bff4b'}
{'hexValue': '#46ff46'}
{'hexValue': '#41ff41'}
{'hexValue': '#3cff3c'}
{'hexValue': '#37ff37'}
{'hexValue': '#32ff32'}
{'hexValue': '#2dff2d'}
{'hexValue': '#28ff28'}
{'hexValue': '#23ff23'}
{'hexValue': '#1eff1e'}
{'hexValue': '#19ff19'}
{'hexValue': '#14ff14'}
{'hexValue': '#0fff0f'}
{'hexValue': '#0aff0a'}
{'hexValue': '#05ff05'}
{'hexValue': '#00ff00'}
{'hexValue': '#05fa05'}
{'hexValue': '#0af50a'}
{'hexValue': '#0ff00f'}
{'hexValue': '#14eb14'}
{'hexValue': '#19e619'}
{'hexValue': '#1ee11e'}
{'hexValue': '#23dc23'}
{'hexValue': '#28d728'}
{'hexValue': '#2dd22d'}
{'hexValue': '#32cd32'}
{'hexValue': '#37c837'}
{'hexValue': '#3cc33c'}
{'hexValue': '#41be41'}
{'hexValue': '#46b946'}
{'hexValue': '#4bb44b'}
{'hexValue': '#50af50'}
{'hexValue': '#55aa55'}
{'hexValue': '#5aa55a'}
{'hexValue': '#5fa05f'}
{'hexValue': '#649b64'}
{'hexValue': '#699669'}
{'hexValue': '#6e916e'}
{'hexValue': '#738c73'}
{'hexValue': '#788778'}
{'hexValue': '#7d827d'}
{'hexValue': '#827d82'}
{'hexValue': '#877887'}
{'hexValue': '#8c738c'}
{'hexValue': '#916e91'}
{'hexValue': '#966996'}
{'hexValue': '#9b649b'}
{'hexValue': '#a05fa0'}
{'hexValue': '#a55aa5'}
{'hexValue': '#aa55aa'}
{'hexValue': '#af50af'}
{'hexValue': '#b44bb4'}
{'hexValue': '#b946b9'}
{'hexValue': '#be41be'}
{'hexValue': '#c33cc3'}
{'hexValue': '#c837c8'}
{'hexValue': '#cd32cd'}
{'hexValue': '#d22dd2'}
{'hexValue': '#d728d7'}
{'hexValue': '#dc23dc'}
{'hexValue': '#e11ee1'}
{'hexValue': '#e619e6'}
{'hexValue': '#eb14eb'}
{'hexValue': '#f00ff0'}
{'hexValue': '#f50af5'}
{'hexValue': '#fa05fa'} """


""" {'hexValue': '#05ff05'}
{'hexValue': '#0aff0a'}
{'hexValue': '#0fff0f'}
{'hexValue': '#14ff14'}
{'hexValue': '#19ff19'}
{'hexValue': '#1eff1e'}
{'hexValue': '#23ff23'}
{'hexValue': '#28ff28'}
{'hexValue': '#2dff2d'}
{'hexValue': '#32ff32'}
{'hexValue': '#37ff37'}
{'hexValue': '#3cff3c'}
{'hexValue': '#41ff41'}
{'hexValue': '#46ff46'}
{'hexValue': '#4bff4b'}
{'hexValue': '#50ff50'}
{'hexValue': '#55ff55'}
{'hexValue': '#5aff5a'}
{'hexValue': '#5fff5f'}
{'hexValue': '#64ff64'}
{'hexValue': '#69ff69'}
{'hexValue': '#6eff6e'}
{'hexValue': '#73ff73'}
{'hexValue': '#78ff78'}
{'hexValue': '#7dff7d'}
{'hexValue': '#82ff82'}
{'hexValue': '#87ff87'}
{'hexValue': '#8cff8c'}
{'hexValue': '#91ff91'}
{'hexValue': '#96ff96'}
{'hexValue': '#9bff9b'}
{'hexValue': '#a0ffa0'}
{'hexValue': '#a5ffa5'}
{'hexValue': '#aaffaa'}
{'hexValue': '#afffaf'}
{'hexValue': '#b4ffb4'}
{'hexValue': '#b9ffb9'}
{'hexValue': '#beffbe'}
{'hexValue': '#c3ffc3'}
{'hexValue': '#c8ffc8'}
{'hexValue': '#cdffcd'}
{'hexValue': '#d2ffd2'}
{'hexValue': '#d7ffd7'}
{'hexValue': '#dcffdc'}
{'hexValue': '#e1ffe1'}
{'hexValue': '#e6ffe6'}
{'hexValue': '#ebffeb'}
{'hexValue': '#f0fff0'}
{'hexValue': '#f5fff5'}
{'hexValue': '#fafffa'}
{'hexValue': '#ffffff'}
{'hexValue': '#fffaff'}
{'hexValue': '#fff5ff'}
{'hexValue': '#fff0ff'}
{'hexValue': '#ffebff'}
{'hexValue': '#ffe6ff'}
{'hexValue': '#ffe1ff'}
{'hexValue': '#ffdcff'}
{'hexValue': '#ffd7ff'}
{'hexValue': '#ffd2ff'}
{'hexValue': '#ffcdff'}
{'hexValue': '#ffc8ff'}
{'hexValue': '#ffc3ff'}
{'hexValue': '#ffbeff'}
{'hexValue': '#ffb9ff'}
{'hexValue': '#ffb4ff'}
{'hexValue': '#ffafff'}
{'hexValue': '#ffaaff'}
{'hexValue': '#ffa5ff'}
{'hexValue': '#ffa0ff'}
{'hexValue': '#ff9bff'}
{'hexValue': '#ff96ff'}
{'hexValue': '#ff91ff'}
{'hexValue': '#ff8cff'}
{'hexValue': '#ff87ff'}
{'hexValue': '#ff82ff'}
{'hexValue': '#ff7dff'}
{'hexValue': '#ff78ff'}
{'hexValue': '#ff73ff'}
{'hexValue': '#ff6eff'}
{'hexValue': '#ff69ff'}
{'hexValue': '#ff64ff'}
{'hexValue': '#ff5fff'}
{'hexValue': '#ff5aff'}
{'hexValue': '#ff55ff'}
{'hexValue': '#ff50ff'}
{'hexValue': '#ff4bff'}
{'hexValue': '#ff46ff'}
{'hexValue': '#ff41ff'}
{'hexValue': '#ff3cff'}
{'hexValue': '#ff37ff'}
{'hexValue': '#ff32ff'}
{'hexValue': '#ff2dff'}
{'hexValue': '#ff28ff'}
{'hexValue': '#ff23ff'}
{'hexValue': '#ff1eff'}
{'hexValue': '#ff19ff'}
{'hexValue': '#ff14ff'}
{'hexValue': '#ff0fff'}
{'hexValue': '#ff0aff'}
{'hexValue': '#ff05ff'} """