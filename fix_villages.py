import nbt
import math

villageFile = nbt.nbt.NBTFile("villages_boxcraft.dat")

allDoors = villageFile["data"]["Villages"].tags[0]["Doors"]  # Get all doors

zAllCoords = [d['Z'].value for d in allDoors]  # Gather z coordinates of doors
zCoords = sorted(list(dict.fromkeys(zAllCoords)))  # Remove duplicates and sort

newVillages = {}

for door in allDoors:
    i = zCoords.index(door['Z'].value)

    if not newVillages.get(i):  # Create array if empty
        newVillages[i] = []

    newVillages[i].append(door)

print(newVillages)

nbtDoors = nbt.nbt.TAG_List(name="Doors", type=nbt.nbt.TAG_Compound)
nbtDoors.tags.append(newVillages[0][0])

nbtVillage = nbt.nbt.TAG_Compound()
nbtVillage.tags.append(nbtDoors)

exportedVillages = nbt.nbt.TAG_List(name="Villages", type=nbt.nbt.TAG_Compound)
exportedVillages.tags.append(nbtVillage)

exportedVillageFile = nbt.nbt.NBTFile("villages_boxcraft.dat")
exportedVillageFile["data"]["Villages"] = exportedVillages
exportedVillageFile.write_file("villages_boxcraft_fixed.dat")
