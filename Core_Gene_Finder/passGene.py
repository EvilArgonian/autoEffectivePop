import sys
import os

blastFile = sys.argv[1]
geneFile = sys.argv[2]
threshold = float(sys.argv[3])

mismatches = 0
length = 0
with open(blastFile, "r") as b:
    for line in b.readlines():
        mismatches += float(line.split("\t")[4])
        length += float(line.split("\t")[3])
if length == 0:
    print("Failed! Error: Length of 0.")
    os.rename(geneFile, "FAILED_" + geneFile)
    exit()
else:
    avg_identity = float((length - mismatches)/length)

if avg_identity >= threshold:
    # Do I need to add the matched gene into the query for future runs here?
    print("Passed!")
else:
    os.rename(geneFile, "FAILED_" + geneFile)
    print("Failed! Similarity below threshold: " + str(avg_identity) + "<" + str(threshold))
