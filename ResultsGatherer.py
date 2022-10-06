import os

resultsSuperFolder = "final_output"


with open("GatheredResults.txt", "w+") as outFile:
    with open("NoResultsFound.txt", "w+") as badOutFile:
        with open("OldRunSpecies", "w+") as oldOutFile:
            for filename in os.listdir(resultsSuperFolder):
                speciesFolder = os.path.join(resultsSuperFolder, filename)
                if os.path.isdir(speciesFolder):
                    resultsFile = os.path.join(speciesFolder, "Results.txt")
                    if os.path.isfile(resultsFile):
                        print("Found " + resultsFile)
                        with open(resultsFile, "r") as readFile:
                            if readFile.readlines()[0].startswith("Species"):
                                oldOutFile.write(filename)
                            else:
                                outFile.write(readFile.readlines()[0])
                    else:
                        print("Did not find " + resultsFile)
                        badOutFile.write(filename + "\n")
