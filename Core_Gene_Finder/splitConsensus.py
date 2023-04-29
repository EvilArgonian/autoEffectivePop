import os
import sys

species = sys.argv[1]
specFolder = os.path.join("categories/All/", species)
outFolder = os.path.join(specFolder, "/Individual_Seqs")

if not os.path.exists(specFolder):
    print("Species not found in All category!")
    exit(1)
if not os.path.exists(outFolder):
    print("Creating Individual_Seqs folder for " + species + " as " + outFolder)
    os.mkdir(outFolder)
    with open(os.path.join(specFolder, species, ".txt"), "r") as consensusFile:
        nucSeqTitle = ""
        nucSeqBuilder = ""
        for line in consensusFile:
            if line.startswith(">"):
                if nucSeqTitle != "":
                    with open(os.path.join(outFolder, nucSeqTitle, ".fa"), "w") as outFile:
                        outFile.write(nucSeqTitle + "\n")
                        outFile.write(nucSeqBuilder)
                nucSeqTitle = line.strip()
                nucSeqBuilder = ""
            else:
                nucSeqBuilder += line.strip().upper()
        with open(os.path.join(outFolder, nucSeqTitle, ".fa"), "w") as outFile:
            outFile.write(nucSeqTitle + "\n")
            outFile.write(nucSeqBuilder)
else:
    print("Species consensus sequences already split.")
