import nbt
import math

importVillageFile = nbt.nbt.NBTFile("villages_boxcraft.dat")
importCorruptVillage = importVillageFile["data"]["Villages"].tags[0]

# Get all doors
allDoors = importCorruptVillage["Doors"]

zAllCoords = [d['Z'].value for d in allDoors]  # Gather z coordinates of doors
zCoords = sorted(list(dict.fromkeys(zAllCoords)))  # Remove duplicates and sort

# print(zCoords)

newVillages = {}

for door in allDoors:
    i = zCoords.index(door['Z'].value)

    if not newVillages.get(i):  # Create array if empty
        newVillages[i] = []

    newVillages[i].append(door)

# print(newVillages)

exportedVillages = nbt.nbt.TAG_List(name="Villages", type=nbt.nbt.TAG_Compound)

for villageIndex in newVillages:  # z-coord-sorted village list
    villageArrangedDoors = []

    tmpVillage = newVillages[villageIndex].copy()
    tmpVillage.sort(key=lambda x: x['X'].value)

    villageUpper = tmpVillage[:11]
    villageLower = tmpVillage[11:]

    nbtDoors = nbt.nbt.TAG_List(name="Doors", type=nbt.nbt.TAG_Compound)

    # arrange village doors
    for i, door in enumerate(newVillages[villageIndex]):
        if i % 2 == 0:
            minVal = max(villageUpper, key=lambda x: x['X'].value)
            villageArrangedDoors.append(minVal)
            villageUpper.remove(minVal)
        else:
            maxVal = min(villageLower, key=lambda x: x['X'].value)
            villageArrangedDoors.append(maxVal)
            villageLower.remove(maxVal)

    nbtDoors.tags.extend(villageArrangedDoors)

    nbtVillage = nbt.nbt.TAG_Compound()
    nbtVillage.tags.append(nbtDoors)
    nbtVillage.tags.append(nbt.nbt.TAG_List(
        name="Players", type=nbt.nbt.TAG_Compound))

    doorsXvals = [door['X'].value for door in villageArrangedDoors]
    doorsYvals = [door['Y'].value for door in villageArrangedDoors]
    doorsZvals = [door['Z'].value for door in villageArrangedDoors]

    # calculate ACX,ACY,ACZ
    nbtVillage.tags.extend([
        nbt.nbt.TAG_Int(name="ACX", value=sum(doorsXvals)),
        nbt.nbt.TAG_Int(name="ACY", value=sum(doorsYvals)),
        nbt.nbt.TAG_Int(name="ACZ", value=sum(doorsZvals))
    ])

    # calculate CX,CY,CZ
    nbtVillage.tags.extend([
        nbt.nbt.TAG_Int(name="CX", value=sum(doorsXvals) // len(doorsXvals)),
        nbt.nbt.TAG_Int(name="CY", value=sum(doorsYvals) // len(doorsYvals)),
        nbt.nbt.TAG_Int(name="CZ", value=sum(doorsZvals) // len(doorsZvals))
    ])

    # add other attributes
    nbtVillage.tags.extend([
        nbt.nbt.TAG_Int(name="Golems", value=0),  # reset saved golems
        nbt.nbt.TAG_Int(name="MTick", value=0),
        nbt.nbt.TAG_Int(
            name="PopSize", value=importCorruptVillage["PopSize"].value),
        nbt.nbt.TAG_Int(
            name="Radius", value=importCorruptVillage["Radius"].value),
        nbt.nbt.TAG_Int(
            name="Stable", value=importCorruptVillage["Stable"].value),
        nbt.nbt.TAG_Int(
            name="Tick", value=importCorruptVillage["Tick"].value)

    ])

    exportedVillages.tags.append(nbtVillage)


exportedVillageFile = nbt.nbt.NBTFile("villages_boxcraft.dat")
exportedVillageFile["data"]["Villages"] = exportedVillages
exportedVillageFile.write_file("villages_boxcraft_fixed.dat")
