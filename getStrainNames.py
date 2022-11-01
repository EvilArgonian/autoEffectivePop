import os
import re

outputFolder = "final_output"
muscleOutFolder = "muscle_output"

with open("speciesStrainTable.txt", "w") as tableFile:
    for speciesFolder in os.listdir(outputFolder):
        speciesPath = os.path.join(outputFolder, speciesFolder)
        if os.path.isdir(speciesPath):
            with open(speciesPath + "Strains.txt", "w") as strainFile:
                strainList = []
                speciesMuscleFolder = os.path.join(muscleOutFolder, speciesFolder)
                if len(os.listdir(speciesMuscleFolder)) > 0:
                    for muscleAlignment in os.listdir(speciesMuscleFolder):
                        with open(os.path.join(speciesMuscleFolder, muscleAlignment), "r") as alignFile:
                            for line in alignFile.readlines():
                                if line.startswith(">"):
                                    existCheck = re.search("\[strain=(.+?)\]", line)
                                    if existCheck:
                                        strainName = existCheck.group(1)
                                        if strainName not in strainList:
                                            strainList.append(strainName)
                    if len(strainList) == 0:
                        print("No strains found in " + speciesFolder)
                        continue
                    for strain in strainList:
                        strainFile.write(strain + "\n")
                        tableFile.write(speciesFolder + "\t" + strain + "\n")
        print("Completed searching " + speciesFolder)