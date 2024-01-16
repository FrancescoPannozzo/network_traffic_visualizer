connectedTo = ["s1", "s2"]

switch = {
  "connectedTo": connectedTo
}

print(switch)
print(type(switch["connectedTo"]))

data = [[],[]]
data[0].append({"endpoints": ["link1", "link2"],
             "linkcap": 10})
data[0].append({"endpoints": ["link1", "link3"],
             "linkcap": 20}
             )

data[1].append({"name": "switch1",
                "address": "123.123.123.123"})

data[1].append({"name": "switch2",
                "address": "123.123.123.124"}
              )

for i in data:
  print(i)