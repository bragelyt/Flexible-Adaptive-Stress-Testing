

inputLayers = []
hiddenLayers = []
outputLayers = []

for i in range(7):
    inputLayers.append("2i"+str(i))

for h in range(8):
    hiddenLayers.append("2h"+str(h))

for o in range(1):
    outputLayers.append("2o"+str(o))


print("%-------------------")
for i in inputLayers:
    for h in hiddenLayers:
        print(f"    \draw[gray]({i}) -- ({h})" + "{};")

print("%-------------------")
for h in hiddenLayers:
    for o in outputLayers:
        print(f"    \draw[gray]({h}) -- ({o})" + "{};")
        
print("%-------------------")