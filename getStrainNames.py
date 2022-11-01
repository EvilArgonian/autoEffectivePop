import os
import re

outputFolder = "final_output"
muscleOutFolder = "muscle_output"

for speciesFolder in os.listdir(outputFolder):
    speciesPath = os.path.join(outputFolder, speciesFolder)
    if os.path.isdir(speciesPath):
            with open("speciesStrainTable.txt", "w") as tableFile:
            with open(speciesPath + "Strains.txt", "w") as strainFile:
                strainList = []
                for muscleAlignment in os.listdir(os.path.join(muscleOutFolder, speciesFolder)):
                    with open(muscleAlignment, "r") as alignFile:
                        for line in alignFile.readlines():
                            if line.startswith(">"):
                                strainName = re.search("\[strain=(.+?)\]", line).group(1)
                                if strainName not in strainList:
                                    strainList.append(strainName)
                for strain in strainList:
                    strainFile.write(strain + "\n")
                    tableFile.write(speciesFolder + "\t" + strain)
                break # Use to test