import os
import sys

specName = sys.argv[1]
outFile = sys.argv[2]
readFile = "final_output/" + specName + "/wattersonsThetaValues.txt"
readOverallFile = "final_output/" + specName + "/Results.txt"

if os.path.exists(readFile):
    with open(outFile, "a") as of:
        with open(readFile, "r") as rf:
            for line in rf.readlines():
                cleanLine = line.replace("_collapsed_mutation_fastas", "")
                cleanLine = cleanLine.replace("Watterson's Theta S: ", "")
                cleanLine = cleanLine.replace("Watterson's Theta N: ", "")
                cleanLine = cleanLine.replace("Watterson's Theta: ", "")

                of.write(specName + "\t" + cleanLine)
        with open(readOverallFile, "r") as rof:
            wS = rof.readlines()[1].split("\t")[9].strip()
            wN = rof.readlines()[1].split("\t")[10].strip()
            wA = rof.readlines()[1].split("\t")[10].strip()

            of.write(specName + "\t" + "Overall" + "\t" + wS + "\t" + wN + "\t" + wA)
    print("Done with " + specName)
