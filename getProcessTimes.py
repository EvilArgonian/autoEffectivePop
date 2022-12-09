import os
import re

outputFolder = "final_output"
inputFolder = "input"

with open("speciesProcessTimeTable.txt", "w") as tableFile:
    for speciesFolder in os.listdir(outputFolder):
        speciesPath = os.path.join(outputFolder, speciesFolder)
        if os.path.isdir(speciesPath):
            #try:
            with open(speciesPath + "/Process_Time.txt", "r") as timeFile:
                timeString = re.findall(r"Runtime: \d+ seconds", timeFile.read())
                print(timeString)
                runtimeSeconds = int(timeString[0].split()[1])
                tableFile.write(speciesFolder + "\t" + runtimeSeconds + "\n")
                print("Found runtime for " + speciesFolder + ": " + runtimeSeconds + " seconds.")
            #except Exception:
                #print("Failed to find runtime for " + speciesFolder + ".")
                #continue
print("All done!")