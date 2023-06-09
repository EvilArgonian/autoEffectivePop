import sys

geneFile = sys.argv[1]
blastFile = sys.argv[2]
try:
    e_threshold = float(sys.argv[3])
except Exception:
    # e_threshold = 0.1 # Defaults to 0.1
    print("Failed! E-value threshold not parsed correctly.")

# mismatches = 0
# length = 0
with open(blastFile, "r") as b:
    stored_e_val = 99999.0
    # stored_line = ""
    for line in b.readlines():
        # mismatches += float(line.split("\t")[4])
        # length += float(line.split("\t")[3])
        e_val = float(line.split("\t")[10])
        if e_val < stored_e_val:
            stored_e_val = e_val
            # stored_line = line

if stored_e_val <= e_threshold:
    # Do I need to add the matched gene into the query for future runs here?
    # ANSWER: Currently assuming a match of A to B and a match of A to C sufficiently proves a match of B to C
    print("Passed!")
else:
    print("Failed! E-value above threshold: " + str(stored_e_val) + ">" + str(e_threshold))
