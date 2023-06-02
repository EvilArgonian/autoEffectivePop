import sys
import os

geneFile = sys.argv[1]
blastFile = sys.argv[2]

with open(blastFile, "r") as b:
    line = b.readlines()[2]
    subStrStart = line.index(" ")
    subStrEnd = line.index("[")
    geneBeforeGB = line[subStrStart:subStrEnd]  # Slices portion including gene name
    #try:  # Attempts to remove portion dedicated to species name, if present
    #    geneBeforeGB = geneBeforeGB[0:geneBeforeGB.index("[")]
    #except Exception:
    #    pass
    geneName = geneBeforeGB.trim().title()  # Replace with location of gene name in blast file
    renaming = geneName.replace(" ", "_") + ".txt"
os.rename(geneFile, renaming)
print(renaming)
