import csv
import os
import sys

nucSpeciesFolder = sys.argv[1]  # Folder where nucleotide sequences are found
orthoFile = sys.argv[2]  # File containing reference list of genes in orthogroups
outF = sys.argv[3]  # Output folder
numOrthogroups = 0
with open(orthoFile, "r") as f:
    numOrthogroups = len(f.readlines()) - 1
    f.seek(0)
    checkError = f.readline()
    if checkError.startswith("ERROR"):
        print(checkError)
        sys.exit(1)
singleCopyOrthogroups = csv.reader(open(orthoFile, "r"), delimiter="\t")

bigDictOfStrainDicts = {}  # Double dictionary
# Outer dict maps strain -> strain dictionary
# Strain dict maps gene -> orthogroup gene belongs to
orthogroupNums = {}

conflicts = 0
conflictList = {}  # Gene : instances seen
strains = []
lineNum = 0
for line in singleCopyOrthogroups:
    if lineNum == 0:
        skipFirst = True
        for strain in line:
            if skipFirst:
                skipFirst = False
                continue
            if strain.strip() == "":  # Probably isn't needed?
                continue
            strains.append(strain.strip())
            bigDictOfStrainDicts.update({strain.strip(): {}})  # Initialize each strain with an empty dict
        lineNum += 1
        continue
    genesInGroup = 0
    indexInSCO = 0  # Index within the Single Copy Orthogroup; index of the column within the line
    skipOrthogroup = True  # For headers
    conflictOccurred = False
    for gene in line:
        if skipOrthogroup:
            skipOrthogroup = False
            continue
        if gene.strip() == "":  # Ignore strains that don't contribute to the orthogroup
            indexInSCO += 1
            continue
        genesInGroup += 1
        currStrain = strains[indexInSCO]
        indexInSCO += 1
        if gene in bigDictOfStrainDicts.get(currStrain):
            conflicts += 1
            numTimes = conflictList.get(currStrain + "_" + gene) or 2
            conflictList.update({currStrain + "_" + gene: numTimes})
        bigDictOfStrainDicts.get(currStrain).update({gene: line[0]})  # Associate gene names to orthogroups
    lineNum += 1
    orthogroupNums.update({line[0]: genesInGroup})

errorCount = 0
errorOrthogroups = []
for strain in bigDictOfStrainDicts.keys():
    if strain == "":
        print("ERROR: Empty-String Strain")
        errorCount += 1
        continue
    if not os.path.exists(nucSpeciesFolder + "/" + strain + "_index.txt"):
        print("ERROR: Strain or strain index not found")
        errorCount += 1
        continue
    with open(nucSpeciesFolder + "/" + strain + "_index.txt", "r") as n:
        indexDict = {}
        for line in n.readlines():
            gene = line.split("\t#---#\t")[0]  # Rigorously specific delimitation used
            index = line.split("\t#---#\t")[1]
            indexDict.update({gene: index})

        file = strain + ".ffn"
        if not os.path.exists(file):
            file = strain + ".fa"
        with open(nucSpeciesFolder + "/" + file, "r") as f:
            geneArr = f.readlines()
            numLines = len(geneArr)
        for gene in bigDictOfStrainDicts.get(strain).keys():
            orthogroup = bigDictOfStrainDicts.get(strain).get(gene)
            geneFormat2 = gene.replace("_", ":", 1)  # One format changed a '_' to a ':'?
            if gene in indexDict:
                indexInStrainFile = int(indexDict.get(gene))
            elif geneFormat2 in indexDict:
                indexInStrainFile = int(indexDict.get(geneFormat2))
            else:
                errorCount += 1
                indexInStrainFile = -1
                errorOrthogroups.append(orthogroup)
                print("ERROR: Gene index not found (" + gene + " / " + geneFormat2 + ")")
            # Copy the original nucleotide gene
            if indexInStrainFile > -1:
                outputStr = geneArr[indexInStrainFile].strip() + " [strain=" + strain + "]\n"
                indexInStrainFile += 1
                while indexInStrainFile < numLines and not geneArr[indexInStrainFile].startswith(">"):
                    outputStr = outputStr + geneArr[indexInStrainFile].strip() + "\n"
                    indexInStrainFile += 1

                genesInGroup = orthogroupNums.get(orthogroup)
                with open(outF + "/" + str(genesInGroup) + "_" + orthogroup + ".fa", "a+") as outFile:
                    outFile.write(outputStr)

for badOg in errorOrthogroups:
    genesInGroup = orthogroupNums.get(badOg)
    if os.path.exists(str(genesInGroup) + "_" + badOg + ".fa"):
        os.remove(str(genesInGroup) + "_" + badOg + ".fa")
        print("Removing " + str(genesInGroup) + "_" + badOg + ".fa due to at least one erroneous gene finding.")
    else:
        print("Orthogroup with unrecognized gene (check gene name formatting for inconsistencies) unused: " + badOg)

print("Gathering of orthogroup sequences complete! Errors: " + str(errorCount))

