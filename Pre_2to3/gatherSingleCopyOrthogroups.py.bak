import csv
import sys

orthoFile = sys.argv[1] + '/Orthogroups/Orthogroups.tsv'
outFile = sys.argv[2]

paralogFile = csv.reader(open(orthoFile, "r"), delimiter="\t")
nonParalogs = []
numNonParalogs = 0
numLines = 0
for line in paralogFile:
    numLines += 1
    linePasses = True
    for strainGroup in line:
        if "," in strainGroup:  # A comma demonstrates presence of multiple
            linePasses = False
            break
    if linePasses:
        numNonParalogs += 1
        print("Found " + str(numNonParalogs) + " single-copy orthogroups so far, out of " + str(numLines) + " lines.")
        nonParalogs.append(line)

with open(outFile, 'w') as f:
    if numNonParalogs == 0:
        f.write("ERROR: No single-copy orthogroups!")
        print("No single-copy orthogroups found! Cannot continue with calculations.")
    else:
        for orthogroup in nonParalogs:
            for gene in orthogroup:
                f.write(gene + "\t")
            f.write("\n")
        print("Gathering of single-copy orthogroups complete!")
