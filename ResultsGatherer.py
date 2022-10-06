import os

resultsSuperFolder = "final_output"


with open("GatheredResults.txt", "w+") as outFile:
    with open("NoResultsFound.txt", "w+") as badOutFile:
            for filename in os.listdir(resultsSuperFolder):
                speciesFolder = os.path.join(resultsSuperFolder, filename)
                if os.path.isdir(speciesFolder):
                    resultsFile = os.path.join(speciesFolder, "Results.txt")
                    if os.path.isfile(resultsFile):
                        print("Found " + resultsFile)
                        with open(resultsFile, "r") as readFile:
                            lines = readFile.readlines()
                            if lines[0].startswith("Species"):
                                outFile.write(lines[1])
                            else:
                                outFile.write(lines[0])
                    else:
                        print("Did not find " + resultsFile)
                        badOutFile.write(filename + "\n")
