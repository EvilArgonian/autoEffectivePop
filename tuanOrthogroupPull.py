import os
import sys

species = sys.argv[1]
muscleInFolder = os.path.join("temp/", species, "muscle_input")
outFile = os.path.join("AgroRhizoTemp", species + ".txt")

if not os.path.exists(muscleInFolder):
    print("Species muscle input folder not found!")
    exit(1)

noLocationCount = 0
allHeaderCount = 0
orthogroupCount = 0

with open(outFile, "w") as o:
    for file in os.listdir(muscleInFolder):
        orthogroupCount += 1
        with open(os.path.join(muscleInFolder, file), "r") as orthogroupFile:
            for line in orthogroupFile.readlines():
                if line.startswith(">"):
                    allHeaderCount += 1
                    o.write(str(file) + "\t" + line.strip() + "\n")
                    if "location" not in line:
                        noLocationCount += 1
                        print(str(noLocationCount) + " - " + line.split()[1] + " did not contain a location.")

print("Out of " + str(allHeaderCount) + " headers in " + str(orthogroupCount) + " orthogroups, " + str(noLocationCount) + " contained no location.")
