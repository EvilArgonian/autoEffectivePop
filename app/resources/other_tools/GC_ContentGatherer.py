import os

gcContentSuperFolder = "final_output"


with open("GatheredGC_Content.txt", "w+") as outFile:
    with open("NoGC_ContentFound.txt", "w+") as badOutFile:
        for filename in os.listdir(gcContentSuperFolder):
            speciesFolder = os.path.join(gcContentSuperFolder, filename)
            if os.path.isdir(speciesFolder):
                gcFile = os.path.join(speciesFolder, "GC_Content.txt")
                if os.path.isfile(gcFile):
                    print("Found " + gcFile)
                    with open(gcFile, "r") as readFile:
                        outFile.write(readFile.readlines()[0])
                else:
                    print("Did not find " + gcFile)
                    badOutFile.write(filename + "\n")
