import os
import sys

category = sys.argv[1]
species = sys.argv[2]
runNum = sys.argv[3]
specFolder = os.path.join("categories/All/", species)
outFolder = os.path.join("core_genes", category, "Run_" + str(runNum), "Genes")
failFile = os.path.join("core_genes", category, "Run_" + str(runNum), "Fails", "NamingFails.txt")
failCount = 0

if not os.path.exists(specFolder):
    print("Species not found in All category!")
    exit(1)
if not os.path.exists(outFolder):
    print(("Creating Genes folder for run as " + outFolder))
    os.mkdir(outFolder)
    with open(specFolder + "/" + species + ".txt", "r") as consensusFile:
        nucSeqTitle = ""
        nucSeqBuilder = ""
        geneNum = 0
        for line in consensusFile:
            if line.startswith(">"):
                if nucSeqTitle != "":
                    nonArbitraryReference = os.path.join("../temp", species, "muscle_output", nucSeqTitle[1:])
                    if os.path.exists(nonArbitraryReference):
                        with open(nonArbitraryReference, "r") as refFile:
                            nameDeterminer = {}
                            foundAny = False
                            for refLine in refFile:
                                if refLine.startswith(">") and "[protein=" in refLine:
                                    subStrStart = refLine.find("[protein=")
                                    if subStrStart >= 0:
                                        subStrEnd = refLine.find("]", subStrStart)
                                        foundAny = True
                                        possName = refLine[subStrStart + 9:subStrEnd]
                                        if possName not in list(nameDeterminer.keys()):
                                            nameDeterminer.update({possName: 1})
                                        else:
                                            nameDeterminer.update({possName: nameDeterminer.get(possName) + 1})
                            if foundAny:
                                if len(list(nameDeterminer.keys())) == 1:
                                    name = list(nameDeterminer.keys())[0].replace(" ", "_").replace("/", "-")
                                else:
                                    highestCountName = list(nameDeterminer.keys())[0]
                                    print("Comparing possible gene names for orthogroup " + nucSeqTitle[1:] + " of species " + str(species) + ":")
                                    for key in list(nameDeterminer.keys()):
                                        print("\t" + key + "\t- found in " + str(nameDeterminer.get(key)) + " sequence headers.")
                                        if nameDeterminer.get(key) > nameDeterminer.get(highestCountName):
                                            highestCountName = key
                                    name = highestCountName.replace(" ", "_").replace("/", "-").replace("/", "-")
                            else:
                                failCount += 1
                                print("No [protein=X] tags identified in orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
                                with open(failFile, "a") as fFile:
                                    fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tNo [protein=X] tags")
                                name = "Arbitrary_Gene_" + str(geneNum)
                    else:
                        failCount += 1
                        print("No muscle output files found for orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
                        with open(failFile, "a") as fFile:
                            fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tNo muscle_output")
                        name = "Arbitrary_Gene_" + str(geneNum)
                    geneFilePath = os.path.join(outFolder, name + ".txt")
                    if not os.path.exists(geneFilePath):
                        with open(geneFilePath, "w") as outFile:
                            outFile.write(nucSeqTitle + " [" + name + "]\n")
                            outFile.write(nucSeqBuilder)
                    else:
                        failCount += 1
                        print("Gene name already taken for orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
                        with open(failFile, "a") as fFile:
                            fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tGene name redundancy")
                nucSeqTitle = line.strip()
                nucSeqBuilder = ""
                geneNum += 1
            else:
                nucSeqBuilder += line.strip().upper()
        geneFilePath = os.path.join(outFolder, name + ".txt")
        if not os.path.exists(geneFilePath):
            with open(geneFilePath, "w") as outFile:
                outFile.write(nucSeqTitle + " [" + name + "]\n")
                outFile.write(nucSeqBuilder)
        else:
            failCount += 1
            print("Gene name already taken for orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
            with open(failFile, "a") as fFile:
                fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tGene name redundancy")
else:
    print("Genes folder already exists.")
