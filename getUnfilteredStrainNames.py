import os
import sys
import re

outputFolder = "final_output"
inputFolder = "input"

if len(sys.argv) > 1:
    outputFolder = "input"  # Causes this to report all strains, even of non-finishing inputs

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
                    if len(strainList) > 400:
                        with open("Over400.txt", "a+") as greater400:
                            greater400.write(speciesFolder + "\t" + str(len(strainList)) + "\n")
                    else:
                        with open("Under400.txt", "a+") as lessEq400:
                            lessEq400.write(speciesFolder + "\t" + str(len(strainList)) + "\n")
                except Exception:
                    continue
        print("Completed searching " + speciesFolder)
print("All done!")
