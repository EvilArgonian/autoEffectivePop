import sys

inFile = sys.argv[1]

with open(inFile, "r") as i:
    mismatches = 0
    length = 0
    count_lines = 0
    for line in i.readlines():
        mismatches += float(line.split("\t")[4])
        length += float(line.split("\t")[3])
        count_lines += 1
    avg_identity = (length - mismatches)/length
print(avg_identity)

