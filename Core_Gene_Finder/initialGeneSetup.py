import os
import sys
import csv

category = sys.argv[1]
species = sys.argv[2]
runNum = sys.argv[3]
specFolder = os.path.join("categories/All/", species)
outFolder = os.path.join("core_genes", category, "Run_" + str(runNum), "Genes")
failFile = os.path.join("core_genes", category, "Run_" + str(runNum), "Fails", "NamingFails.txt")
failCount = 0
cogFile = os.path.join("cog-20.cog.csv")  # From NCBI's COG 2020. Column 1 is GeneID, 3 is ProteinID,  7 is the COG ID, and 11 is the e-value for the protein's match with the COG profile.

# Possible implementations. Only one will be used at a time, and will supercede each other in presented order.
# Consider adding a config for changing these? Possibly unnecessary for the scope.
useCOGviaProteinID = True
useProtein = False

# What tags from original orthogroup sequences get recorded in the orthogroup consensus sequence.
recordList = ["gene", "locus_tag", "protein_id", "protein"]  # [gene=X], [locus_tag=X], [protein_id=X], [protein=X]

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
                            if useCOGviaProteinID:
                                searchTag = "[protein_id="
                                searchLen = 12
                            elif useProtein:
                                searchTag = "[protein="
                                searchLen = 9
                            else:
                                failCount += 1
                                print("No naming implementation enabled.")
                                with open(failFile, "a") as fFile:
                                    fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tNo naming implementation enabled\n")
                                name = "Arbitrary_Gene_" + str(geneNum)
                                continue

                            recordKeeper={}
                            for item in recordList:
                                recordKeeper.update({item: ""})

                            tagDeterminer = {}  # Records counts of unique tag values for the searched tag.
                            foundAny = False
                            for refLine in refFile:
                                if refLine.startswith(">"):
                                    if searchTag in refLine:
                                        subStrStart = refLine.find(searchTag)
                                        if subStrStart >= 0:
                                            subStrEnd = refLine.find("]", subStrStart)
                                            foundAny = True
                                            possTag = refLine[subStrStart + searchLen:subStrEnd]
                                            if possTag not in list(tagDeterminer.keys()):
                                                tagDeterminer.update({possTag: 1})
                                            else:
                                                tagDeterminer.update({possTag: tagDeterminer.get(possTag) + 1})
                                    for recordItem in recordList:
                                        if "[" + recordItem + "=" in refLine:
                                            subStrStart = refLine.find("[" + recordItem + "=")
                                            subStrEnd = refLine.find("]", subStrStart)
                                            recordData = refLine[subStrStart + searchLen:subStrEnd]
                                            recordKeeper.update({recordItem: recordKeeper.get(recordItem) + recordData + ", "})
                            if foundAny:
                                if len(list(tagDeterminer.keys())) == 1:
                                    highestCountTag = list(tagDeterminer.keys())[0].replace(" ", "_").replace("/", "-")
                                else:
                                    if useProtein:  # Clears a list of non-helpful possible protein values from suggestion.
                                        tagDeterminer.pop("hypothetical protein", 0)
                                        tagDeterminer.pop("hypothetical_protein", 0)
                                        tagDeterminer.pop("hypothetical-protein", 0)
                                        tagDeterminer.pop("unknown protein", 0)
                                        tagDeterminer.pop("unknown_protein", 0)
                                        tagDeterminer.pop("unknown-protein", 0)
                                        tagDeterminer.pop("undefined", 0)

                                    highestCountTag = list(tagDeterminer.keys())[0]
                                    print("Comparing possible gene names for orthogroup " + nucSeqTitle[1:] + " of species " + str(species) + ":")
                                    for key in list(tagDeterminer.keys()):
                                        print("\t" + key + "\t- found in " + str(tagDeterminer.get(key)) + " sequence headers.")
                                        if tagDeterminer.get(key) > tagDeterminer.get(highestCountTag):
                                            highestCountTag = key
                                if useCOGviaProteinID:
                                    cogData = csv.reader(open(cogFile, "r"), delimiter=",")
                                    # Column 3 is ProteinID,  7 is the COG ID, and 11 is the e-value for the protein's match with the COG profile.
                                    # Above column values are base 1; shifted -1 for programming base 0.
                                    foundCOG = False
                                    for row in cogData:
                                        if row[2] == highestCountTag:
                                            name = row[6]
                                            foundCOG = True
                                            break
                                    if not foundCOG:
                                        failCount += 1
                                        print("No COG group found for protein_id tag in orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
                                        with open(failFile, "a") as fFile:
                                            fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tNo COG group found for tag: " + highestCountTag + "\n")
                                        name = "Arbitrary_Gene_" + str(geneNum)
                                elif useProtein:
                                    name = highestCountTag.replace(" ", "_").replace("/", "-").replace("/", "-")
                            else:
                                failCount += 1
                                print("No " + searchTag + "X] tags identified in orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
                                with open(failFile, "a") as fFile:
                                    fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tNo " + searchTag + "X] tags\n")
                                name = "Arbitrary_Gene_" + str(geneNum)
                    else:
                        failCount += 1
                        print("No muscle output files found for orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
                        with open(failFile, "a") as fFile:
                            fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tNo muscle_output\n")
                        name = "Arbitrary_Gene_" + str(geneNum)

                    geneFilePath = os.path.join(outFolder, name + ".txt")
                    if not os.path.exists(geneFilePath):
                        with open(geneFilePath, "w") as outFile:
                            recordStr = ""
                            for item in recordList:
                                recordStr += "[contributing_" + item + "=" + recordKeeper.get(item).strip()[0:-1] + "] "
                            recordStr.strip()
                            outFile.write(nucSeqTitle + " [core_gene_ref_name=" + name + "] " + recordStr + "\n")
                            outFile.write(nucSeqBuilder)
                    else:
                        failCount += 1
                        print("Gene name \"" + name + "\" already taken for orthogroup " + nucSeqTitle[1:] + " of species " + str(species))
                        with open(failFile, "a") as fFile:
                            fFile.write(nucSeqTitle[1:] + "\t" + str(failCount) + "\tGene name redundancy\n")
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
