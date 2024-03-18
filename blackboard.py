
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