import sys
import os

geneFile = sys.argv[1]
blastFile = sys.argv[2]

with open(blastFile, "r") as b:
    line = b.readlines[2]
    geneBeforeGB = line[line.index(" "): line.index(">")]  # Slices portion including gene name
    try:  # Attempts to remove portion dedicated to species name, if present
        geneBeforeGB = geneBeforeGB[0:geneBeforeGB.index("[")]
    except Exception:
        pass
    geneName = geneBeforeGB.trim()  # Replace with location of gene name in blast file
    renaming = geneName.title().replace(" ", "_") + ".txt"
os.rename(geneFile, renaming)
print(renaming)
