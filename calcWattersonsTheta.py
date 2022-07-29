import os
import dendropy
import sys

folder = sys.argv[1]

with open("final_output/" + folder + "/wattersonsThetaValues.txt", "w") as f:
    sumTheta = 0
    countTheta = 0

    for file in os.listdir("muscle_output/" + folder + "/"):
        dnaDict = {}
        dnaMatrix = dendropy.DnaCharacterMatrix.get(
        path="muscle_output/" + folder + "/" + file,
        schema="fasta"
        )

        watsTheta = dendropy.calculate.popgenstat.wattersons_theta(dnaMatrix)
        sumTheta += watsTheta
        countTheta += 1

        outString = file.split(".")[0] + " Watterson's Theta: " + str(watsTheta) + "\n"
        f.write(outString)

avgWatsTheta = float(sumTheta)/countTheta
print str(avgWatsTheta)
