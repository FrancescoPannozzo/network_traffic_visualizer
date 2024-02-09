import utils

ip_address = {
    "groupA": 10,
    "groupB": 0,
    "groupC": 0,
    "groupD": 0
}
IP_ADDRESS = "123.123.123."
# Last address group
ipLastGroup = 0

networkData = []

for i in range(0, 600):
    networkData.append({
      "switchName": f"switch{i}",
      "address": utils.ip_to_string(ip_address)
    })
    if i % 255 == 0 and i != 0:
        ip_address["groupC"] += 1
        ip_address["groupD"] = 0
    else:
        ip_address["groupD"] += 1

print("Switches created:")
for i in networkData:
    print(i)