from utils import utils

data = utils.file_loader("./data/custom_graph_freehand")

print(type(data["data"]["linkCap"]))