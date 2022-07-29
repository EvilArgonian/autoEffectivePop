import ftplib
import re

speciesRaw = []
def getAllLines(line):
    speciesRaw.append(line)

ncbi_FTP = "ftp.ncbi.nlm.nih.gov"

ftp = ftplib.FTP(ncbi_FTP, "anonymous", "")
ftp.cwd("genomes/refseq/bacteria")
try:
    ftp.retrlines('NLST', getAllLines)
except EOFError as e:
    with open("massFetchErrors.txt", "w") as eFile:
        eFile.write(str(e))
species = []
for item in speciesRaw:
    spec = re.findall("[a-zA-Z]+_[a-zA-Z]+", item)
    if len(spec) == 1 and not spec[0] in species:
        species.append(spec[0])

outstring = ""
for spec in species:
    outstring += spec + " "
print(outstring)

