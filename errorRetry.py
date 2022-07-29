errorFile = "fetch_errors.txt"
outFile = "massFetch.txt"

with open(errorFile, "r") as e:
  with open(outFile, "w") as o:
      for line in e.readlines():
          speciesName = line.split()[0]
          o.write(speciesName + " ")

