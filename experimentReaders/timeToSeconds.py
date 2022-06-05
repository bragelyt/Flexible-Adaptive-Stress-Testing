

time = {
    "0": "0:02:07.677811",
    "1": "4:04:13.352554",
    "2": "1:05:22.421683",
    "3": "1:43:43.844253",
    "4": "1:09:11.750092",
    "5": "3:09:14.458763"
}

for name in time:
    long = time[name]
    longList = long.split(".")[0]
    longList = longList.split(":")
    seconds = int(longList[0])*3600+int(longList[1])*60+int(longList[2])
    print(name, seconds)
    print(name, round(1000*seconds/1000000, 3))