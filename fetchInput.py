import os
import sys
import ftplib
from datetime import date

specName = sys.argv[1]
ncbi_FTP = "ftp.ncbi.nlm.nih.gov"
ftp = ftplib.FTP(ncbi_FTP, "anonymous", "")

strains = []


def searchForSpec(line):
    if specName in line:
        strains.append(line)


ffnFiles = []


def searchInStrain(line):
    if line.endswith(".ffn"):
        ffnFiles.append(line)


refSeqPart1 = []


def searchInStrainRefseq1(line):
    if not (("_IMG-" in line) or ("_annotated_" in line)):
        refSeqPart1.append(line)


refSeqPart2 = []


def searchInStrainRefseq2(line):
    if line.endswith("_cds_from_genomic.fna.gz"):
        refSeqPart2.append(line)
    if line.endswith("_genomic.gbff.gz"):  # Pull gbff for David
        refSeqPart2.append(line)


try:
    with open(specName + "_fetch.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("set -uo pipefail\n")
        f.write("set +e\n")
        f.write("IFS=$'\\n\\t'\n\n")
        f.write("mkdir -p input/" + specName + "\n")
        # strainNum = 0
        useOld = False
        ftp.cwd("genomes/refseq/bacteria")

        strains = []
        ftp.retrlines('NLST', searchForSpec)
        if not strains:
            useOld = True
        for line in strains:
            # strainNum += 1

            ftp.cwd(line)
            ftp.cwd("latest_assembly_versions")
            # .../bacteria/<speciesInstance>/latest_assembly_versions
            # print("Current directory: " + ftp.pwd())

            refSeqPart1 = []
            ftp.retrlines('NLST', searchInStrainRefseq1)
            for ref in refSeqPart1:
                if ("README" in ref and len(refSeqPart1) == 1):
                    # Indicates only a README file, which will state that 1000+ assemblies are available, and to refer to
                    # /bacteria/<speciesInstance>/assembly_summary.txt column 20 for ftp addresses
                    ftp.cwd("..")  # Exits to <speciesInstance>/ level
                    # print("Current directory [Alt Reference]: " + ftp.pwd())
                    with open(specName + "_summary.txt", "wb") as summary:
                        ftp.retrbinary("RETR " + "assembly_summary.txt", summary.write)
                    with open(specName + "_summary.txt", "r") as summary:
                        skip2 = 0
                        for assembly in summary.readlines():
                            if skip2 < 2:  # Skip first two lines
                                skip2 += 1
                                continue
                            assemblyArr = assembly.split("\t")
                            # (0-based) Column 0 is the assembly_accession, 8 is the name, 10 is the version_status,
                            # 11 is the assembly_level, 15 is the asm_name, 19 is the folder address
                            # files stored as  <folder>/<gbrs_paired_asm>_<asm_name>_genomic.fna.gz
                            if assemblyArr[10] == "latest" and assemblyArr[11] == "Complete Genome":
                                strainName = assemblyArr[8].replace("strain=", "").replace(" ", "_").replace("(",
                                                                                                             "_").replace(
                                    ")", "_")
                                f.write("mkdir -p input/" + specName + "/" + strainName + "\n")
                                f.write("wget -P input/" + specName + "/" + strainName + "/ " +
                                        assemblyArr[19] + "/" + assemblyArr[0] + "_" + assemblyArr[
                                            15] + "_cds_from_genomic.fna.gz\n")
                    f.write("rm " + specName + "_summary.txt\n")
                    continue  # Should end for loop, as only one item in refSeqPart1
                # print(ref + " of the whole " + str(refSeqPart1)) # For testing.
                ftp.cwd(ref)  # Strangely, majorly changes folder structure. Some kind of shortcutting?
                # print("Current directory [Weird]: " + ftp.pwd()) # For testing.
                # .../bacteria/<speciesInstance>/latest_assembly_versions/<strainInstance>

                refSeqPart2 = []
                ftp.retrlines('NLST', searchInStrainRefseq2)
                if not refSeqPart2:
                    ftp.cwd("..")  # Exits to latest_assembly_versions/ level
                    # print("Current directory [No Ref Exit]: " + ftp.pwd()) # For testing.
                    continue

                strainName = ref.split("_")[2]  # Format of ref seems to be 'GCF_<numbers>_<letters><numbers>'
                # print("Strain: " + str(strainNum) + " found: " + strainName)
                f.write("mkdir -p input/" + specName + "/" + strainName + "\n")
                for strainFile in refSeqPart2:
                    f.write("wget -P input/" + specName + "/" + strainName +
                            "/ ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/" + line + "/latest_assembly_versions/" + ref + "/" + strainFile + "\n")
                # ftp.cwd("..") # Exits to latest_assembly_versions/ level # WAS NOT WORKING
                while ftp.pwd() != "/genomes":  # Exits to genomes/ level
                    ftp.cwd("..")  # Needed due to ftp.cwd(ref) doing strange things.
                ftp.cwd("refseq/bacteria")
                ftp.cwd(line)
                ftp.cwd("latest_assembly_versions")  # Returns to latest_assembly_versions/ level
                # print("Current directory [Ref Exit]: " + ftp.pwd()) # For testing.

            ftp.cwd("../..")  # Exits to bacteria/ level
            # print("Current directory [Next Strain Exit]: " + ftp.pwd()) # For testing.

        if useOld:
            ftp.cwd("../..")  # Exits to genomes/ level
            ftp.cwd("archive/old_genbank/Bacteria")
            # print("Current directory [Old Archive Start]: " + ftp.pwd()) # For testing.
            strains = []
            ftp.retrlines('NLST', searchForSpec)
            for line in strains:
                # strainNum += 1
                # print("Current directory [Old Archive Strain]: " + ftp.pwd()) # For testing.
                ftp.cwd(line)
                ftp.retrlines('NLST', searchInStrain)
                if not ffnFiles:
                    ftp.cwd("..")
                    # print("Current directory [Old Archive No Strain Exit]: " + ftp.pwd()) # For testing.
                    continue
                strainName = line.split(specName)[1][1:]
                # print("Strain: " + str(strainNum) + " found: " + strainName)
                f.write("mkdir -p input/" + specName + "/" + strainName + "\n")
                for strainFile in ffnFiles:
                    f.write("wget -P input/" + specName + "/" + strainName +
                            "/ ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_genbank/Bacteria/" + line + "/" + strainFile + "\n")
                ffnFiles = []
                ftp.cwd("..")
                # print("Current directory [Old Archive Strain Exit]: " + ftp.pwd()) # For testing.

            ftp.cwd("../Bacteria_DRAFT")
            # print("Current directory [Old Archive Draft Start]: " + ftp.pwd()) # For testing.
            strains = []
            ftp.retrlines('NLST', searchForSpec)
            for line in strains:
                # strainNum += 1

                ftp.cwd(line)
                ftp.retrlines('NLST', searchInStrain)
                if not ffnFiles:
                    ftp.cwd("..")
                    # print("Current directory [Old Archive Draft No Strain Exit]: " + ftp.pwd()) # For testing.
                    continue
                strainName = line.split(specName)[1].split("uid")[0][1:-1]
                # print("Strain: " + str(strainNum) + " found: " + strainName)
                f.write("mkdir -p input/" + specName + "/" + strainName + "\n")
                for strainFile in ffnFiles:
                    f.write("wget -P -N input/" + specName + "/" + strainName +
                            "/ ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_genbank/Bacteria_DRAFT/" + line + "/" + strainFile + "\n")
                ffnFiles = []
                ftp.cwd("..")
                # print("Current directory [Old Archive Draft Strain Exit]: " + ftp.pwd()) # For testing.


except Exception as e:
    with open("fetch_errors.txt", "a") as errorFile:
        errorFile.write(specName + " - " + date.today().strftime("%B %d, %Y") + " - " + str(e) + "\n")

ftp.close()
