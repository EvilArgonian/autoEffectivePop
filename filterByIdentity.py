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
specLabel = sys.argv[1]
confidence = .9999  # Defaults to 99.99%
if len(sys.argv) > 1:
    confidence = Decimal(sys.argv[2])

folder = "temp/" + specLabel + "/BLAST/"
# Folder will contain the strain files in the form <strain>.ffn, and the BLAST comparisons in the form <strain1>_vs_<strain2>.txt

with open("temp/" + specLabel + "/Filtered/Filtration_Log.txt", "w") as logFile:
    avgIdentityData = {}  # This dict will record all observations of avgIdentity in the 1 on 1 BLASTs
    strains = []  # This list will record each strain name
    logFile.write("Beginning BLAST data collection for " + specLabel + "\n")
    for filename in os.listdir(folder):  # For every file
        if "_vs_" in filename and filename.endswith(".txt"):  # Interprets identity from strain v strain BLAST
            thisVs = ".".join(filename.split(".")[0:len(filename.split(".")) - 1])  # This nonsense to allow for strain names with periods in them
            mismatches = 0
            length = 0
            with open(folder + "/" + filename, "r") as i:
                for line in i.readlines():
                    mismatches += float(line.split("\t")[4])
                    length += float(line.split("\t")[3])
            if length == 0:
                avg_identity = 1  # Shouldn't happen. What might cause this?
            else:
                avg_identity = float((length - mismatches)/length)
            avgIdentityData.update({thisVs: avg_identity})
            logFile.write("Data added: " + thisVs + " with score " + str(avg_identity) + "\n")
        elif filename.endswith(".ffn"):
            thisStrain = ".".join(filename.split(".")[0:len(filename.split(".")) - 1])  # This nonsense to allow for strain names with periods in them
            strains.append(thisStrain)

    # Printing for testing
    with open("temp/" + specLabel + "/Filtered/Statistics.txt", "w") as f:
        dataCount = 0
        for versus in avgIdentityData.keys():
            dataCount += 1
            twoStrainArr = versus.split("_vs_")
            if len(twoStrainArr) != 2:
                logFile.write("ERROR: twoStrainArr found with " + str(len(twoStrainArr)) + " strains: " + str(twoStrainArr))
                continue  # This shouldn't occur.
            f.write(versus + " > ")
            if twoStrainArr[0] not in strains or twoStrainArr[1] not in strains:
                avgIdentityData.pop(versus)
                logFile.write(str(dataCount) + " of " + str(len(avgIdentityData.keys())) + "- BLAST data involving unused strain discarded: " + versus + "\n")
            else:
                f.write(str(dataCount) + " of " + str(len(avgIdentityData.keys())) + "- " + versus + "\t" + str(avgIdentityData[versus]) + "\n")

    logFile.write(str(len(strains)) + " strains recognized: " + str(strains) + "\n")

    # Evaluate the mean, sd, sample size, etc
    sampleSize = len(avgIdentityData.values())
    sampleMean = Decimal(numpy.mean(avgIdentityData.values()))
    sampleStdDev = Decimal(stats.tstd(avgIdentityData.values()))
    sampleStdError = Decimal(stats.tsem(avgIdentityData.values()))
    sampleVariance = sampleStdDev * sampleStdDev

    logFile.write("Sample statistics:" + "\n")
    logFile.write("Sample Size: " + str(sampleSize) + "\n")
    logFile.write("Sample Mean: " + str(sampleMean) + "\n")
    logFile.write("Sample Standard Deviation: " + str(sampleStdDev) + "\n")
    logFile.write("Sample Standard Error: " + str(sampleStdError) + "\n")

    if sampleSize == 1:  # One versus file, or just 2 strains
        twoStrainArr = avgIdentityData.keys()[0].split("_vs_")
        for strain in twoStrainArr:  # For each of the only 2 strains
            source = "temp/" + specLabel + "/BLAST/" + strain + ".ffn"
            destination = "temp/" + specLabel + "/Nucleotide/"
            shutil.copy(source, destination)
        print("2")  # Cannot do any statistical evaluation, so the strains are simply passed through
        sys.exit()

    boundDiff = Decimal(2 * sampleStdDev)
    lowerBound = Decimal(sampleMean - boundDiff)

    logFile.write("Lowerbound of " + specLabel + " determined to be: " + str(lowerBound) + "\n")

    # Any average of all 1v1s incorporating a given strain that *falls below* the range indicates too dissimilar strains
    # On an unrelated note, the word "exceeds" should really have an established antonym "deceeds"
    removed = []
    removalInfo = []
    for strain in strains:  # For each strain
        strainData = []
        for versus in avgIdentityData.keys():  # For each 1v1 that compares 2 surviving strains
            twoStrainArr = versus.split("_vs_")
            if strain in twoStrainArr:
                strainData.append(Decimal(avgIdentityData[versus]))
        avgOfStrainAvgs = numpy.mean(strainData)
        if numpy.isnan(float(avgOfStrainAvgs)):  # Occasional NaN issue with avgOfStrainAvgs? How to handle?
            removed.append(strain)
            removalInfo.append(strain + " Average of Strain-Vs-Other-Strain Average Identities: " + str(
                avgOfStrainAvgs) + ", which produced a NaN.")
            logFile.write(strain + " Average of Strain-Vs-Other-Strain Average Identities: " + str(
                avgOfStrainAvgs) + ", which produced a NaN." + "\n")
        else:
            if avgOfStrainAvgs < lowerBound:
                removed.append(strain)
                removalInfo.append(strain + " Average of Strain-Vs-Other-Strain Average Identities: " + str(
                    avgOfStrainAvgs) + ", which is under the critical value by " + str(lowerBound - avgOfStrainAvgs))
                logFile.write(strain + " Average of Strain-Vs-Other-Strain Average Identities: " + str(
                    avgOfStrainAvgs) + ", which is under the critical value by " + str(lowerBound - avgOfStrainAvgs) + "\n")

    for strain in removed:
        strains.remove(strain)
        source = "temp/" + specLabel + "/BLAST/" + strain + ".ffn"
        destination = "temp/" + specLabel + "/Filtered/"
        try:
            shutil.copy(source, destination)
        except IOError as e:
            logFile.write("Strain copy to " + destination + " failed!" + "\n")

    with open("temp/" + specLabel + "/Filtered/RemovalForDissimilarity.txt",
              "w") as f:
        f.write("Mean AvgIdentity: " + str(sampleMean) + "\tStandard Deviation: " + str(
            sampleStdDev) + "\tLower Bound: " + str(lowerBound) + "\n")
        for item in removalInfo:
            f.write(item + "\n")  # Records comparisons that resulted in removal

    logFile.write(
        "Remaining " + str(len(strains)) + " " + specLabel + " strains recognized (partial): " + str(strains) + "\n")

    if len(strains) >= 3:  # Ceases calculations if less than 3 strains
        remaining = {}  # For reanalyzing remaining data
        for versus in avgIdentityData.keys():
            twoStrainArr = versus.split("_vs_")
            if twoStrainArr[0] in strains and twoStrainArr[1] in strains:
                remaining.update({versus: avgIdentityData[versus]})

        sampleSize = len(remaining.values())
        sampleMean = Decimal(numpy.mean(remaining.values()))
        sampleStdDev = Decimal(stats.tstd(remaining.values()))
        sampleStdError = Decimal(stats.tsem(remaining.values()))
        sampleVariance = sampleStdDev * sampleStdDev

        logFile.write("Sample statistics:" + "\n")
        logFile.write("Sample Size: " + str(sampleSize) + "\n")
        logFile.write("Sample Mean: " + str(sampleMean) + "\n")
        logFile.write("Sample Standard Deviation: " + str(sampleStdDev) + "\n")
        logFile.write("Sample Standard Error: " + str(sampleStdError) + "\n")

        boundDiff = Decimal(2 * sampleStdDev)
        upperBound = Decimal(sampleMean + boundDiff)
        upperBound = Decimal(.999)  # HARD CUTOFF USED; REMOVE THIS TO RETURN TO StdDev
        if upperBound >= 1:
            logFile.write("Upperbound of " + specLabel + " determined to be: " + str(upperBound) + ", which is greater than 1. Upperbound set instead to .999\n")
            upperbound = Decimal(.999)
        else:
            logFile.write("Upperbound of " + specLabel + " determined to be: " + str(upperBound) + "\n")

        # Any 1v1 that *exceeds* the range indicates too similar strains
        removed = []
        removalInfo = []
        for strain in strains:  # For each strain
            if strain in removed:
                continue  # If the strain was already flagged for similarity, ignore
            for versus in remaining.keys():  # For each...
                twoStrainArr = versus.split("_vs_")
                if strain in twoStrainArr:  # ...appearance of the strain in a 1v1 comparison
                    testValue = Decimal(remaining[versus])
                    if testValue > upperBound:  # Strains are too similar
                        otherStrain = twoStrainArr[1 - twoStrainArr.index(strain)]
                        if otherStrain in removed:
                            continue  # If the other strain was already flagged for similarity, ignore
                        removed.append(otherStrain)  # Remove one of the too similar strains
                        removalInfo.append(
                            "Removed " + otherStrain + " from " + versus + " Average Identity: " + str(
                                testValue) + ", which is over the critical value by " + str(testValue - upperBound))
                        logFile.write("Removed " + otherStrain + " from " + versus + " Average Identity: " + str(
                            testValue) + ", which is over the critical value by " + str(
                            testValue - upperBound) + "\n")

        for strain in removed:
            logFile.write("Enacting removal of " + strain + "\n")
            strains.remove(strain)
            source = "temp/" + specLabel + "/BLAST/" + strain + ".ffn"
            destination = "temp/" + specLabel + "/Filtered/"
            try:
                shutil.copy(source, destination)
            except IOError as e:
                logFile.write("Strain copy to " + destination + " failed!")

        with open("temp/" + specLabel + "/Filtered/RemovalForSimilarity.txt", "w") as f:
            f.write("Mean AvgIdentity: " + str(sampleMean) + "\tStandard Deviation: " + str(
                sampleStdDev) + "\tUpper Bound: " + str(upperBound) + "\n")
            for item in removalInfo:
                f.write(item + "\n")  # Records comparisons that resulted in removal

        logFile.write("Remaining " + str(len(strains)) + " " + specLabel + " strains recognized (final): " + str(strains) + "\n")
        if len(strains) >= 2:  # Ceases calculations if less than 2 strains
            for strain in strains:  # For each finally remaining strain
                source = "temp/" + specLabel + "/BLAST/" + strain + ".ffn"
                destination = "temp/" + specLabel + "/Nucleotide/"
                try:
                    shutil.copy(source, destination)
                except IOError as e:
                    logFile.write("Strain copy to " + destination + " failed!" + "\n")
            print(len(strains))  # Marks that not too many species were filtered
        else:
            logFile.write("Not enough strains surviving final filtration of " + specLabel + "\n")
            print("-1")  # Marks that too many species were filtered
    else:
        logFile.write("Not enough strains surviving partial filtration of " + specLabel + "\n")
        print("-1")  # Marks that too many species were filtered

