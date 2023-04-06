import sys

species = sys.argv[1].strip()
mutFile = "../mutation_rates.txt"

mutRate = "Unknown"
found = False
with open(mutFile, "r") as f:
    for line in f.readlines():
        if line.split("\t")[0].strip() == species:
            mutRate = line.split("\t")[1]
            found = True
            break
if not found:
    with open("mutation_rates.txt", "a+") as f:
        f.write(species + "\tUnknown\n")
print(mutRate)

