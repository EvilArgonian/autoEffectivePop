import os

resultsSuperFolder = "final_output"


with open("GatheredResults.txt", "a+") as outFile:
    with open("NoResultsFound.txt", "a+") as badOutFile:
        for filename in os.listdir(resultsSuperFolder):
            speciesFolder = os.path.join(resultsSuperFolder, filename)
            if os.path.isdir(speciesFolder):
                resultsFile = os.path.join(speciesFolder, "Results.txt")
                if os.path.isfile(resultsFile):
                    print("Found " + resultsFile)
                    with open(resultsFile, "r") as readFile:
                        outFile.write(readFile.readlines()[0])
                else:
                    print("Did not find " + resultsFile)
                    badOutFile.write(filename + "\n")
