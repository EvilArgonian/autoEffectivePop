import sys
import os

inFile = sys.argv[1]
indexFile = sys.argv[2]
errorFile = sys.argv[3]

if not os.path.exists(inFile):
    print("No translatable files for given input: " + inFile)
    sys.exit()

seenList = []
conflictList = []

with open(indexFile, "w") as ind:
    conflicts = 0
    with open(inFile, "r") as inp:
        geneName = ""
        lineIndex = -1
        countSeq = 0
        for line in inp.readlines():
            lineIndex = lineIndex + 1
            line = line.strip()
            if line.startswith(">"):
                countSeq += 1
                geneName = ((line.split(" ")[0])[1:]).strip()
                if geneName in seenList:
                    conflicts += 1
                    conflictList.append(geneName + "\t" + lineIndex + "\t" + line)
                else:
                    seenList.append(geneName)
                ind.write(geneName + "\t#---#\t" + str(lineIndex) + "\n")  # Rigorously specific delimitation applied

if conflicts > 0:
    with open(errorFile, "w") as e:
        e.write("Formatted Gene Name\tLine Index\tFull Gene Header")
        for conflict in conflictList:
            e.write(conflict)
    e.close()

ind.close()
inp.close()

print("Completed indexing of " + inFile + " with " + str(conflicts) + " conflicts in " + str(countSeq) + " sequences.")

