import sys
import os

category = sys.argv[1]
outFile = sys.argv[2]

categoryRuns = os.path.join("core_genes", category)

firstRun = True
passedInAll = []
for run in os.listdir(categoryRuns):
    passedGeneFile = os.path.join(categoryRuns, run, "Passed_Genes.txt")
    with open(passedGeneFile, "r") as p:
        if firstRun:
            for line in p.readlines():
                passedInAll.append(line.strip())
        else:
            passedInThis = []
            for line in p.readlines():
                passedInThis.append(line.strip())
            passedInAll = [gene for gene in passedInAll if gene in passedInThis]
with open(outFile, "w") as out:
    for gene in passedInAll:
        out.write(gene + "\n")