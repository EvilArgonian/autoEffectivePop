import sys

outFile = sys.argv[1]
strains = sys.argv[2]
runtime = sys.argv[3]
label = "Unlabeled"
if sys.argv[4]:
    label = sys.argv[4]

with open(outFile, "w") as o:
    o.write("Total elapsed real time (" + label + "):\n")
    o.write("Strains: " + str(strains) + "\t" + str(runtime) + "s")

