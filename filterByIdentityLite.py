import os
import shutil
import sys
import numpy
from decimal import Decimal
from scipy import stats

# Goal: to filter out strains that are too similar, or too dissimilar, from other strains of ostenstibly the same species. Two hypothesis tests.
# Null hypothesis 1: A given strain is not too similar to another; it is distant enough to be a unique strain. Any given 1v1 data point of that strain versus another accepted strain is below (within) the critical upper boundary.
# Alternate hypothesis 1: A given strain is too similar to another and thus likely to be the same strain as it. At least one given 1v1 data point of that strain versus another accepted strain is above (beyond) the critical upper boundary.
# Null hypothesis 2: A given strain is not too dissimilar to the others; it is close enough to be a part of the same species. The average of 1v1 data points of that strain is above (within) the critical lower boundary.
# Alternate hypothesis 2: A given strain is too dissimilar to the others and thus likely to be a unique species. The average of 1v1 data points of that strain is below (beyond) the critical lower boundary.
print("Beginning a lite filtering round... ")

specLabel = sys.argv[1]
with open("temp/" + specLabel + "/Filtered/Filtration_Log_Lite.txt", "a+") as logFile:
    confidence = .9999  # Defaults to 99.99%
    currStrain = sys.argv[2]
    if len(sys.argv) > 2:
        confidence = float(sys.argv[3])
        logFile.write("Confidence provided: " + str(confidence) + "\n")
    hardCut = .995 # Using default of .995; return to None to remove
    if len(sys.argv) > 3:
        hardCut = Decimal(sys.argv[4])
        logFile.write("Hard Upperbound provided: " + str(hardCut) + "\n")

    folder = "temp/" + specLabel + "/BLAST/"
    # Folder will contain the strain files in the form <strain>.ffn, and the BLAST comparisons in the form <strain1>_vs_<strain2>.txt

    logFile.write("Determining any prior removed strains:\n")
    removed = []
    if os.path.isfile("temp/" + specLabel + "/Filtered/Removal_Log.txt"):
        with open("temp/" + specLabel + "/Filtered/Removal_Log.txt", "r") as removedStrains:
            for line in removedStrains.readlines():
                removed.append(line.strip())
                logFile.write(line.strip() + " already removed.\n")

    avgIdentityData = {}  # This dict will record all observations of avgIdentity in the 1 on 1 BLASTs
    strains = []  # This list will record each strain name
    logFile.write("Beginning BLAST data collection for " + specLabel + "\n")
    for filename in os.listdir(folder):  # For every file
        # This nonsense to allow for strain names with periods in them
        fileNameFormatted = ".".join(filename.split(".")[0:len(filename.split(".")) - 1])
        if "_vs_" in filename and filename.endswith(".txt"):  # Interprets identity from strain v strain BLAST
            thisVs = fileNameFormatted
            if thisVs.split("_vs_")[0] in removed or thisVs.split("_vs_")[1] in removed:
                continue  # Do not record entries involving removed strains
            mismatches = 0
            length = 0
            with open(folder + "/" + filename, "r") as i:
                for line in i.readlines():
                    mismatches += float(line.split("\t")[4])
                    length += float(line.split("\t")[3])
            if length == 0:
                avg_identity = 1  # Shouldn't happen. What might cause this?
            else:
                avg_identity = float((length - mismatches) / length)
            avgIdentityData.update({thisVs: avg_identity})
            logFile.write("Data added: " + thisVs + " with score " + str(avg_identity) + "\n")
        elif filename.endswith(".ffn") and fileNameFormatted not in removed:
            strains.append(fileNameFormatted)

    # Outputting for testing
    with open("temp/" + specLabel + "/Filtered/Statistics_Lite.txt", "a+") as f:
        for versus in avgIdentityData.keys():
            f.write(versus + "\t" + str(avgIdentityData[versus]) + "\n")

    logFile.write(str(len(strains)) + " strains recognized: " + str(strains) + "\n")

    # Evaluate the mean, sd, sample size, etc
    sampleSize = len(avgIdentityData.values())
    sampleMean = Decimal(numpy.mean(avgIdentityData.values()))
    sampleStdDev = Decimal(stats.tstd(avgIdentityData.values()))
    sampleStdError = Decimal(stats.tsem(avgIdentityData.values()))

    logFile.write("Sample statistics:" + "\n")
    logFile.write("Sample Size: " + str(sampleSize) + "\n")
    logFile.write("Sample Mean: " + str(sampleMean) + "\n")
    logFile.write("Sample Standard Deviation: " + str(sampleStdDev) + "\n")
    logFile.write("Sample Standard Error: " + str(sampleStdError) + "\n")

    print("Sample statistics:")
    print("Sample Size: " + str(sampleSize))
    print("Sample Mean: " + str(sampleMean))
    print("Sample Standard Deviation: " + str(sampleStdDev))
    print("Sample Standard Error: " + str(sampleStdError))

    if sampleSize == 1:  # One versus file, or just 2 strains
        twoStrainArr = avgIdentityData.keys()[0].split("_vs_")
        for strain in twoStrainArr:  # For each of the only 2 strains
            source = "temp/" + specLabel + "/BLAST/" + strain + ".ffn"
            destination = "temp/" + specLabel + "/Nucleotide/"
            shutil.copy(source, destination)
        with open("temp/" + specLabel + "/Filtered/Output.txt", "w") as outFile:
            # Cannot do any statistical evaluation, so the strains are simply passed through
            outFile.write(" ".join(strains))
        sys.exit()

    boundDiff = Decimal(2 * sampleStdDev)
    lowerBound = Decimal(sampleMean - boundDiff)
    if (not hardCut) or (hardCut and Decimal(sampleMean + boundDiff) < hardCut):
        upperBound = Decimal(sampleMean + boundDiff)
    else:
        upperBound = hardCut
    logFile.write("Lowerbound of " + specLabel + " set to be: " + str(lowerBound) + "\n")
    logFile.write("Upperbound of " + specLabel + " set to be: " + str(upperBound) + "\n")

    # Any 1v1 outside of the range indicates too much dissimilarity (below) or similarity (above)
    removed = []
    removalInfo = []
    for strain in strains:  # For each strain
        if strain in removed:
            continue  # If the strain was already flagged for removal, ignore
        for versus in avgIdentityData.keys():  # For each...
            twoStrainArr = versus.split("_vs_")
            if strain in twoStrainArr and currStrain in twoStrainArr:  # ...appearance of the strain in a 1v1 comparison
                testValue = Decimal(avgIdentityData[versus])
                if testValue > upperBound:  # Strains are too similar
                    otherStrain = twoStrainArr[1 - twoStrainArr.index(strain)]
                    if otherStrain in removed:
                        continue  # If the other strain was already flagged for similarity, ignore
                    otherStrain = twoStrainArr[1 - twoStrainArr.index(currStrain)]  # Avoid removing the current strain
                    removed.append(str(otherStrain))  # Remove one of the too similar strains
                    removalInfo.append("Removed " + otherStrain + " from " + versus + " Average Identity: " + str(
                        testValue) + ", which is over the critical value by " + str(testValue - upperBound))
                    logFile.write("Removed " + otherStrain + " from " + versus + " Average Identity: " + str(
                        testValue) + ", which is over the critical value by " + str(testValue - upperBound) + "\n")
            if testValue < lowerBound:  # Strains are too dissimilar
                otherStrain = twoStrainArr[1 - twoStrainArr.index(strain)]
                if otherStrain in removed:
                    continue  # If the other strain was already flagged for similarity, ignore
                otherStrain = twoStrainArr[1 - twoStrainArr.index(currStrain)]  # Avoid removing the current strain
                removed.append(str(otherStrain))  # Remove one of the too similar strains
                removalInfo.append("Removed " + otherStrain + " from " + versus + " Average Identity: " + str(
                    testValue) + ", which is under the critical value by " + str(lowerBound - testValue))
                logFile.write("Removed " + otherStrain + " from " + versus + " Average Identity: " + str(
                    testValue) + ", which is under the critical value by " + str(lowerBound - testValue) + "\n")

    logFile.write("Total strains removed: " + str(len(removed)) + "\n")
    with open("temp/" + specLabel + "/Filtered/Removal_Log.txt", "a+") as removedStrains:
        for strain in removed:
            strain = str(strain)  # Maybe necessary in case strain name was interpreted as numeric??
            strains.remove(str(strain))  # Redundant casting probably
            source = "temp/" + specLabel + "/BLAST/" + strain + ".ffn"
            destination = "temp/" + specLabel + "/Filtered/"
            try:
                shutil.move(source, destination)
            except IOError as e:
                print("Strain move to " + destination + " failed!")
                logFile.write("Strain move to " + destination + " failed!")
            removedStrains.write(strain + "\n")

    with open("temp/" + specLabel + "/Filtered/RemovalForSimilarity_Lite.txt", "a+") as f:
        with open("temp/" + specLabel + "/Filtered/RemovalForDissimilarity_Lite.txt", "a+") as f2:
            f.write("Mean AvgIdentity: " + str(sampleMean) + "\tStandard Deviation: " + str(
                sampleStdDev) + "\tUpper Bound: " + str(upperBound) + "\n")
            f2.write("Mean AvgIdentity: " + str(sampleMean) + "\tStandard Deviation: " + str(
                sampleStdDev) + "\tLower Bound: " + str(lowerBound) + "\n")
            for item in removalInfo:
                if " over the critical value " in item:
                    f.write(item + "\n")  # Records comparisons that resulted in removal
                else:
                    f2.write(item + "\n")  # Records comparisons that resulted in removal

    logFile.write("Remaining " + str(len(strains)) + " " + specLabel + " strains recognized: " + str(strains) + "\n")
    with open("temp/" + specLabel + "/Filtered/Output.txt", "w") as outFile:
        outFile.write(",".join(strains))

print("Total strains removed: " + str(len(removed)))
print("Remaining " + str(len(strains)) + " " + specLabel + " strains recognized: " + str(strains))
