import os
import sys

category = sys.argv[1]
species = sys.argv[2]
runNum = sys.argv[3]
specFolder = os.path.join("categories/All/", species)
outFolder = os.path.join("core_genes", category, "Run_" + str(runNum), "Genes")

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
                    with open(outFolder + "/Gene_" + str(geneNum) + ".txt", "w") as outFile:
                        outFile.write(nucSeqTitle + " [Gene_" + str(geneNum) + "]\n")
                        outFile.write(nucSeqBuilder)
                nucSeqTitle = line.strip()
                nucSeqBuilder = ""
                geneNum += 1
            else:
                nucSeqBuilder += line.strip().upper()
        with open(outFolder + "/" + nucSeqTitle, "w") as outFile:
            outFile.write(">" + nucSeqTitle + "\n")
            outFile.write(nucSeqBuilder + "\n")
else:
    print("Genes folder already exists.")
