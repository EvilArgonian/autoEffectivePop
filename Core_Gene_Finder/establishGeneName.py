import sys
import os

geneFile = sys.argv[1]
blastFile = sys.argv[2]
try:
    with open(blastFile, "r") as b:
        index = 0
        for searchLine in b.readlines():
            if searchLine.startswith("Sequences producing significant alignments:"):
                index += 2  # Line to parse will be 2 lines down
                break
            index += 1
        line = b.readlines()[index]
        subStrStart = line.index(" ")
        subStrEnd = line.index("[")
        geneBeforeGB = line[subStrStart:subStrEnd]  # Slices portion including gene name
        # try:  # Attempts to remove portion dedicated to species name, if present
        #    geneBeforeGB = geneBeforeGB[0:geneBeforeGB.index("[")]
        # except Exception:
        #    pass
        geneName = geneBeforeGB.trim().title()  # Replace with location of gene name in blast file
        renaming = geneName.replace(" ", "_") + ".txt"
    os.rename(geneFile, renaming)
except Exception:
    renaming = "Error_" + geneFile
print(renaming)
