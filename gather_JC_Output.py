import os
import sys

specName = sys.argv[1]
outFile = sys.argv[2]
readFile = "final_output/" + specName + "/wattersonsThetaValues.txt"

if os.path.exists(readFile):
    with open(readFile, "r") as rf:
        for line in rf.readlines():
            cleanLine = line.replace("_collapsed_mutation_fastas", "")
            cleanLine = cleanLine.replace(" Watterson's Theta S: ", "")
            cleanLine = cleanLine.replace(" Watterson's Theta N: ", "")
            cleanLine = cleanLine.replace(" Watterson's Theta: ", "")

            with open(outFile, "a") as of:
                of.write(specName + "\t" + cleanLine)
    print("Done with " + specName)
