import os
import re

outputFolder = "final_output"
inputFolder = "input"

with open("speciesUnfilteredStrainTable.txt", "w") as tableFile:
    for speciesFolder in os.listdir(outputFolder):
        speciesPath = os.path.join(outputFolder, speciesFolder)
        if os.path.isdir(speciesPath):
            with open(speciesPath + "/UnfilteredStrains.txt", "w") as strainFile:
                strainList = []
                speciesInputFolder = os.path.join(inputFolder, speciesFolder)
                try:
                    for strainFolder in os.listdir(speciesInputFolder):
                        if os.path.isdir(os.path.join(speciesInputFolder, strainFolder)):
                            strainList.append(strainFolder)
                    if len(strainList) == 0:
                        print("No unfiltered input strains found in " + speciesFolder)
                        continue
                    for strain in strainList:
                        strainFile.write(strain + "\n")
                        tableFile.write(speciesFolder + "\t" + strain + "\n")
                except Exception:
                    continue
        print("Completed searching " + speciesFolder)
print("All done!")