
import datetime

from utils import utils

data = utils.file_loader("./data/setup")

start_time = data["startSimTime"]

hours = start_time.strftime('%H')
minutes = start_time.strftime('%M')
seconds = start_time.strftime('%S.%f')[:-3]

print(hours, minutes, seconds)

hours = int(start_time.strftime('%H'))
minutes = int(start_time.strftime('%M'))
seconds = float(start_time.strftime('%S.%f')[:-3])

print(hours, minutes, seconds)
colors = utils.traffic_colors_gen(0, 255, 255)

for _, color in colors.items():
    print(color)

{'hexValue': '#05ffff'}
{'hexValue': '#0affff'}
{'hexValue': '#0fffff'}
{'hexValue': '#14ffff'}
{'hexValue': '#19ffff'}
{'hexValue': '#1effff'}
{'hexValue': '#23ffff'}
{'hexValue': '#28ffff'}
{'hexValue': '#2dffff'}
{'hexValue': '#32ffff'}
{'hexValue': '#37ffff'}
{'hexValue': '#3cffff'}
{'hexValue': '#41ffff'}
{'hexValue': '#46ffff'}
{'hexValue': '#4bffff'}
{'hexValue': '#50ffff'}
{'hexValue': '#55ffff'}
{'hexValue': '#5affff'}
{'hexValue': '#5fffff'}
{'hexValue': '#64ffff'}
{'hexValue': '#69ffff'}
{'hexValue': '#6effff'}
{'hexValue': '#73ffff'}
{'hexValue': '#78ffff'}
{'hexValue': '#7dffff'}
{'hexValue': '#82ffff'}
{'hexValue': '#87ffff'}
{'hexValue': '#8cffff'}
{'hexValue': '#91ffff'}
{'hexValue': '#96ffff'}
{'hexValue': '#9bffff'}
{'hexValue': '#a0ffff'}
{'hexValue': '#a5ffff'}
{'hexValue': '#aaffff'}
{'hexValue': '#afffff'}
{'hexValue': '#b4ffff'}
{'hexValue': '#b9ffff'}
{'hexValue': '#beffff'}
{'hexValue': '#c3ffff'}
{'hexValue': '#c8ffff'}
{'hexValue': '#cdffff'}
{'hexValue': '#d2ffff'}
{'hexValue': '#d7ffff'}
{'hexValue': '#dcffff'}
{'hexValue': '#e1ffff'}
{'hexValue': '#e6ffff'}
{'hexValue': '#ebffff'}
{'hexValue': '#f0ffff'}
{'hexValue': '#f5ffff'}
{'hexValue': '#faffff'}
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
{'hexValue': '#ff05ff'}