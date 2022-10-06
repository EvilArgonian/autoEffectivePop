import sys

species = sys.argv[1].strip()
mutationFile = "../reference_files/mutation_rates.txt"

mutRate = "Unknown"
found = False
with open(mutationFile, "r") as f:
    for line in f.readlines():
        if line.split("\t")[0].strip() == species:
            mutRate = line.split("\t")[1]
            found = True
            break
if not found:
    with open(mutationFile, "a+") as f:
        f.write(species + "\tUnknown\n")
print(mutRate)

