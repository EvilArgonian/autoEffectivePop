import os
import re
import sys

outputFolder = "final_output"
muscleOutFolder = "muscle_output"

if len(sys.argv) > 1:
    speciesFolder = sys.argv[1]
    speciesPath = os.path.join(outputFolder, speciesFolder)
    if os.path.isdir(speciesPath):
        with open(speciesPath + "/SurvivingStrains.txt", "w") as strainFile:
            strainList = []
            speciesMuscleFolder = os.path.join(muscleOutFolder, speciesFolder)
            for muscleAlignment in os.listdir(speciesMuscleFolder):
                print("Checking muscle alignment: " + muscleAlignment)
                with open(os.path.join(speciesMuscleFolder, muscleAlignment), "r") as alignFile:
                    for line in alignFile.readlines():
                        if line.startswith(">"):
                            existCheck = re.search("\[strain=(.+?)\]", line)
                            if existCheck:
                                strainName = existCheck.group(1)
                                if strainName not in strainList:
                                    strainList.append(strainName)
                                    print("Counted strain: " + strainName)
            if len(strainList) == 0:
                print("No surviving strains found in " + speciesFolder)
            for strain in strainList:
                strainFile.write(strain + "\n")
            print("Surviving strains found in " + speciesFolder + ": " + str(len(strainList)))
    else:
        print("Unrecognized species folder: " + speciesFolder)
    exit(0)

with open("speciesStrainTable.txt", "w") as tableFile:
    for speciesFolder in os.listdir(outputFolder):
        speciesPath = os.path.join(outputFolder, speciesFolder)
        if os.path.isdir(speciesPath):
            with open(speciesPath + "/SurvivingStrains.txt", "w") as strainFile:
                strainList = []
                speciesMuscleFolder = os.path.join(muscleOutFolder, speciesFolder)
                try:
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
                        print("No surviving strains found in " + speciesFolder)
                        continue
                    for strain in strainList:
                        strainFile.write(strain + "\n")
                        tableFile.write(speciesFolder + "\t" + strain + "\n")
                except Exception:
                    continue
        print("Completed searching " + speciesFolder)
print("All done!")