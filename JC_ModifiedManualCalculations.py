import os
import sys
import re
import datetime

# from functools import lru_cache

specName = sys.argv[1]

table = {
    # Other IUPAC codes with certain results commented for possible later integration
    # 'M' - START, '_' - STOP
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    # "GCR": "A", "GCY": "A", "GCS": "A", "GCW": "A", "GCK": "A", "GCM": "A", "GCB": "A", "GCD": "A", "GCH": "A", "GCV": "A", "GCN": "A",
    "TGT": "C", "TGC": "C",  # "TGY": "C",
    "GAT": "D", "GAC": "D",  # "GAY": "D",
    "GAA": "E", "GAG": "E",  # "GAR": "E",
    "TTT": "F", "TTC": "F",  # "TTY": "F",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    # "GGR": "G", "GGY": "G", "GGS": "G", "GGW": "G", "GGK": "G", "GGM": "G", "GGB": "G", "GGD": "G", "GGH": "G", "GGV": "G", "GGN": "G",
    "CAT": "H", "CAC": "H",  # "CAY": "H",
    "ATA": "I", "ATT": "I", "ATC": "I",  # "ATY": "I", "ATW": "I", "ATM": "I", "ATH": "I",
    "AAA": "K", "AAG": "K",  # "AAR": "K",
    "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    # "TTR": "L", "CTR": "L", "CTY": "L", "CTS": "L", "CTW": "L", "CTK": "L", "CTM": "L", "CTB": "L", "CTD": "L", "CTH": "L", "CTV": "L", "CTN": "L",
    "ATG": "M",
    "AAT": "N", "AAC": "N",  # "AAY": "N",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    # "CCR": "P", "CCY": "P", "CCS": "P", "CCW": "P", "CCK": "P", "CCM": "P", "CCB": "P", "CCD": "P", "CCH": "P", "CCV": "P", "CCN": "P",
    "CAA": "Q", "CAG": "Q",  # "CAR": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    # "CGR": "R", "CGY": "R", "CGS": "R", "CGW": "R", "CGK": "R", "CGM": "R", "CGB": "R", "CGD": "R", "CGH": "R", "CGV": "R", "CGN": "R", "AGR": "R",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
    # "TCR": "S", "TCY": "S", "TCS": "S", "TCW": "S", "TCK": "S", "TCM": "S", "TCB": "S", "TCD": "S", "TCH": "S", "TCV": "S", "TCN": "S", "AGY": "S",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    # "ACR": "T", "ACY": "T", "ACS": "T", "ACW": "T", "ACK": "T", "ACM": "T", "ACB": "T", "ACD": "T", "ACH": "T", "ACV": "T", "ACN": "T",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    # "GTR": "V", "GTY": "V", "GTS": "V", "GTW": "V", "GTK": "V", "GTM": "V", "GTB": "V", "GTD": "V", "GTH": "V", "GTV": "V", "GTN": "V",
    "TGG": "W",
    "TAT": "Y", "TAC": "Y",  # "TAY": "Y",
    "TAA": "_", "TAG": "_", "TGA": "_"  # "TAR": "_"
}
synChances = {
    "GCT": [0.0, 0.0, 1.0], "GCC": [0.0, 0.0, 1.0], "GCA": [0.0, 0.0, 1.0], "GCG": [0.0, 0.0, 1.0],
    "TGT": [0.0, 0.0, (1.0 / 3.0)], "TGC": [0.0, 0.0, (1.0 / 3.0)],
    "GAT": [0.0, 0.0, (1.0 / 3.0)], "GAC": [0.0, 0.0, (1.0 / 3.0)],
    "GAA": [0.0, 0.0, (1.0 / 3.0)], "GAG": [0.0, 0.0, (1.0 / 3.0)],
    "TTT": [0.0, 0.0, (1.0 / 3.0)], "TTC": [0.0, 0.0, (1.0 / 3.0)],
    "GGT": [0.0, 0.0, 1.0], "GGC": [0.0, 0.0, 1.0], "GGA": [0.0, 0.0, 1.0], "GGG": [0.0, 0.0, 1.0],
    "CAT": [0.0, 0.0, (1.0 / 3.0)], "CAC": [0.0, 0.0, (1.0 / 3.0)],
    "ATA": [0.0, 0.0, (2.0 / 3.0)], "ATT": [0.0, 0.0, (2.0 / 3.0)], "ATC": [0.0, 0.0, (2.0 / 3.0)],
    "AAA": [0.0, 0.0, (1.0 / 3.0)], "AAG": [0.0, 0.0, (1.0 / 3.0)],
    "TTA": [(1.0 / 3.0), 0.0, (1.0 / 3.0)], "TTG": [(1.0 / 3.0), 0.0, (1.0 / 3.0)], "CTT": [0.0, 0.0, 1.0],
    "CTC": [0.0, 0.0, 1.0], "CTA": [(1.0 / 3.0), 0.0, 1.0], "CTG": [(1.0 / 3.0), 0.0, 1.0],
    "ATG": [0.0, 0.0, 0.0],
    "AAT": [0.0, 0.0, (1.0 / 3.0)], "AAC": [0.0, 0.0, (1.0 / 3.0)],
    "CCT": [0.0, 0.0, 1.0], "CCC": [0.0, 0.0, 1.0], "CCA": [0.0, 0.0, 1.0], "CCG": [0.0, 0.0, 1.0],
    "CAA": [0.0, 0.0, (1.0 / 3.0)], "CAG": [0.0, 0.0, (1.0 / 3.0)],
    "CGT": [0.0, 0.0, 1.0], "CGC": [0.0, 0.0, 1.0], "CGA": [(1.0 / 3.0), 0.0, 1.0], "CGG": [(1.0 / 3.0), 0.0, 1.0],
    "AGA": [(1.0 / 3.0), 0.0, (1.0 / 3.0)], "AGG": [(1.0 / 3.0), 0.0, (1.0 / 3.0)],
    "TCT": [0.0, 0.0, 1.0], "TCC": [0.0, 0.0, 1.0], "TCA": [0.0, 0.0, 1.0], "TCG": [0.0, 0.0, 1.0],
    "AGT": [0.0, 0.0, (1.0 / 3.0)], "AGC": [0.0, 0.0, (1.0 / 3.0)],
    "ACT": [0.0, 0.0, 1.0], "ACC": [0.0, 0.0, 1.0], "ACA": [0.0, 0.0, 1.0], "ACG": [0.0, 0.0, 1.0],
    "GTT": [0.0, 0.0, 1.0], "GTC": [0.0, 0.0, 1.0], "GTA": [0.0, 0.0, 1.0], "GTG": [0.0, 0.0, 1.0],
    "TGG": [0.0, 0.0, 0.0],
    "TAT": [0.0, 0.0, (1.0 / 3.0)], "TAC": [0.0, 0.0, (1.0 / 3.0)],
    "TAA": [0.0, (1.0 / 3.0), (1.0 / 3.0)], "TAG": [0.0, 0.0, (1.0 / 3.0)], "TGA": [0.0, (1.0 / 3.0), 0.0]
}

thetaByNumStrains = {}
piByNumStrains = {}


class TestComplementLocationException(Exception):
    def __init__(self, actualPos, message="Actual Position: "):
        self.actualPos = actualPos
        self.message = message + str(actualPos)
        super(Exception, self).__init__(self.message)


class UnfoundLocationException(Exception):
    def __init__(self, message="Location Not Identified"):
        self.message = message
        super(Exception, self).__init__(self.message)


def buildNucDict(file):
    # Building sequences for processing
    nucDict = {}  # Index 0 is consensus
    nucSeqTitle = ""
    nucSeqBuilder = ""
    with open(file, "r") as alignedFile:
        for line in alignedFile:
            if line.startswith(">"):
                if nucSeqTitle != "":
                    nucDict.update({nucSeqTitle: nucSeqBuilder})
                nucSeqTitle = line.strip()
                nucSeqBuilder = ""
            else:
                nucSeqBuilder += line.strip().upper()
        nucDict.update({nucSeqTitle: nucSeqBuilder})
    return nucDict


def getComplement(nucStr):
    if nucStr == "BEG" or nucStr == "END":
        return nucStr  # Should this switch BEG and END?
    outStr = ""
    for nuc in nucStr:
        if nuc == 'A':
            outStr += 'T'
        elif nuc == 'T':
            outStr += 'A'
        elif nuc == 'C':
            outStr += 'G'
        elif nuc == 'G':
            outStr += 'C'
    return outStr


# @lru_cache(maxsize=None)
def harmonic(n):
    if n <= 0:
        return -1  # Input should not be non-positive
    if n == 1:
        return n
    return float(1 / n) + harmonic(n - 1)


def calcThetas(nucDict, numStrains, ancestralSeq, file):
    # Processing/counting for Watterson's Theta & Theta S values
    numDictSeq = len(list(nucDict.keys()))
    seqLength = len(list(nucDict.values())[0])

    # Create a pair of forward and backward facing loops to determine the longest leading/trailing gap sequences;
    # Remove all positions within these from any calculations (no changes counted, not counted against length)
    gapLengths = [0.0] * numDictSeq  # Initialize counts of leading gaps
    gapsEnded = [False] * numDictSeq  # Initialize flags for leading gap ends
    for pos in range(0, seqLength):
        for seqIndex in range(0, numDictSeq):
            if not gapsEnded[seqIndex]:
                if list(nucDict.values())[seqIndex][pos] == "_" or list(nucDict.values())[seqIndex][pos] == "-":
                    gapLengths[seqIndex] += 1.0
                else:
                    gapsEnded[seqIndex] = True
        if all(gapsEnded):  # If all leading gaps have already ended
            break
    leadingGaps = max(gapLengths)

    gapLengths = [0.0] * numDictSeq  # Initialize counts of trailing gaps
    gapsEnded = [False] * numDictSeq  # Initialize flags for trailing gap ends
    for pos in range(seqLength - 1, -1, -1):
        for seqIndex in range(0, numDictSeq):
            if not gapsEnded[seqIndex]:
                if list(nucDict.values())[seqIndex][pos] == "_" or list(nucDict.values())[seqIndex][pos] == "-":
                    gapLengths[seqIndex] += 1.0
                else:
                    gapsEnded[seqIndex] = True
        if all(gapsEnded):  # If all leading gaps have already ended
            break
    trailingGaps = max(gapLengths)

    with open("final_output/" + specName + "/" + specName + "_MutationCalls.txt", "a+") as mutCalls:
        # Tracking for mutations seen
        actualSynChanges = 0.0
        actualNonSynChanges = 0.0
        actualAllChanges = 0
        potentialSynChanges = 0.0
        potentialNonSynChanges = 0.0

        for i in range(0, seqLength, 3):  # For each codon
            consensusCodon = ancestralSeq[i:i + 3]
            # Determine potential synonymous changes
            foundSynSite = 0.0
            foundNonSynSite = 0.0
            foundSegSite = [False, False, False]
            if consensusCodon in list(synChances.keys()):
                potentialSynChanges += sum(synChances[consensusCodon])
                potentialNonSynChanges += (3 - sum(synChances[consensusCodon]))
            for seqIndex in range(1, numDictSeq):
                actualCodon = list(nucDict.values())[seqIndex][i:i + 3]
                mutsInCodon = [0, 0, 0]
                for pos in range(0, 3):
                    if i + pos < leadingGaps or i + pos >= seqLength - trailingGaps:
                        continue  # Ignore positions within the leading and trailing gap sections
                    if consensusCodon not in list(table.keys()) or actualCodon not in list(table.keys()):
                        synCheck = False
                    else:
                        synCheck = True
                    if pos >= len(consensusCodon) or pos >= len(actualCodon):
                        continue
                    if consensusCodon[pos] != actualCodon[pos]:
                        mutsInCodon[pos] = 1
                        try:
                            strainName = re.search("\[strain=(.+?)\]", list(nucDict.keys())[seqIndex]).group(1)
                        except Exception:
                            strainName = "Strain Name Not Found"
                        geneName = list(nucDict.keys())[seqIndex].split(" ")[0]
                        if synCheck:
                            # Technically could be inaccurate in codons with 2 or 3 mutations; minor difference.
                            synStatus = "S" if table[consensusCodon] == table[actualCodon] else "N"
                        else:
                            synStatus = "U"  # Represents uncertain synonymity
                        twoLeft = "BEG" if i + pos - 2 < leadingGaps else ancestralSeq[i + pos - 2]
                        oneLeft = "BEG" if i + pos - 1 < leadingGaps else ancestralSeq[i + pos - 1]
                        middle = ancestralSeq[i + pos]
                        oneRight = "END" if i + pos + 1 >= seqLength - trailingGaps else ancestralSeq[i + pos + 1]
                        twoRight = "END" if i + pos + 2 >= seqLength - trailingGaps else ancestralSeq[i + pos + 2]
                        adjPos = "InSeq_" + str(i + pos)
                        try:
                            actualPos = re.search("\[location=(.+?)\]", list(nucDict.keys())[seqIndex]).group(1)
                            if "complement" in actualPos:
                                twoLeft = getComplement(twoLeft)
                                oneLeft = getComplement(oneLeft)
                                middle = getComplement(middle)
                                oneRight = getComplement(oneRight)
                                twoRight = getComplement(twoRight)

                                actualPos = re.search("\((.+?)\.\.", actualPos).group(1)
                            else:
                                actualPos = re.search("(.+?)\.\.", actualPos).group(1)
                            try:
                                adjPos = str(int(actualPos) + i + pos)
                            except ValueError:
                                adjPos = "Err " + actualPos + "+" + str(i + pos)
                            callOutput = specName + ", " + strainName + ", " + geneName + ", " + synStatus + ", " + adjPos + ", " + twoLeft + ", " + oneLeft + ", " + middle + ", " + \
                                         list(nucDict.values())[seqIndex][i + pos] + ", " + oneRight + ", " + twoRight + "\n"
                            mutCalls.write(callOutput)
                        except Exception:
                            callOutput = specName + ", " + strainName + ", " + geneName + ", " + synStatus + ", " + adjPos + ", " + twoLeft + ", " + oneLeft + ", " + middle + ", " + \
                                         list(nucDict.values())[seqIndex][i + pos] + ", " + oneRight + ", " + twoRight + "\n"
                            mutCalls.write(callOutput)
                        if not foundSegSite[pos]:
                            actualAllChanges += 1
                            foundSegSite[pos] = True  # Comment out if counting multiple in one column
                if i < leadingGaps or i >= seqLength - trailingGaps:
                    continue  # Ignore positions within the leading and trailing gap sections
                if consensusCodon not in list(table.keys()) or actualCodon not in list(table.keys()):
                    continue
                if sum(mutsInCodon) == 3:  # This gets ridiculous fast...
                    inBetween12_1 = actualCodon[0] + consensusCodon[1:]  # Ttt
                    inBetween13_2 = actualCodon[0:2] + consensusCodon[2]  # TTt
                    inBetween25_2 = actualCodon[0] + consensusCodon[1] + actualCodon[2]  # TtT
                    inBetween34_1 = consensusCodon[0] + actualCodon[1] + consensusCodon[2]  # tTt
                    inBetween46_2 = consensusCodon[0] + actualCodon[1:]  # tTT
                    inBetween56_1 = consensusCodon[0:2] + actualCodon[2]  # ttT

                    totSynFound = 0.0
                    totNonSynFound = 0.0
                    if table[consensusCodon] == table[
                        inBetween12_1]:  # Compare consensus to between possibility part 1 of paths 1 and 2 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween12_1] == table[
                        inBetween13_2]:  # Compare between possibility part 1 of path 1 to part 2 of path 1
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween13_2] == table[
                        actualCodon]:  # Compare between possibility part 2 of paths 1 and 3 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween12_1] == table[
                        inBetween25_2]:  # Compare between possibility part 1 of path 2 to part 2 of path 2
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween25_2] == table[
                        actualCodon]:  # Compare between possibility part 2 of paths 2 and 5 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[consensusCodon] == table[
                        inBetween34_1]:  # Compare consensus to between possibility part 1 of paths 3 and 4 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween34_1] == table[
                        inBetween13_2]:  # Compare between possibility part 1 of path 3 to part 2 of path 3
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween34_1] == table[
                        inBetween46_2]:  # Compare between possibility part 1 of path 4 to part 2 of path 4
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween46_2] == table[
                        actualCodon]:  # Compare between possibility part 2 of paths 4 and 6 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[consensusCodon] == table[
                        inBetween56_1]:  # Compare consensus to between possibility part 1 of paths 5 and 6 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween56_1] == table[
                        inBetween25_2]:  # Compare between possibility part 1 of path 5 to part 2 of path 5
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween56_1] == table[
                        inBetween46_2]:  # Compare between possibility part 1 of path 6 to part 2 of path 6
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0

                    # Determine if actual weightings exceed any others found in this codon column and update if so
                    # Division by 6 for the 6 possible paths
                    if foundSynSite < (totSynFound / 6.0):
                        actualSynChanges += (totSynFound / 6.0) - foundSynSite
                        foundSynSite = (totSynFound / 6.0)
                    if foundNonSynSite < (totNonSynFound / 6.0):
                        actualNonSynChanges += (totNonSynFound / 6.0) - foundNonSynSite
                        foundNonSynSite = (totNonSynFound / 6.0)

                elif sum(mutsInCodon) == 2:
                    mutPos1 = -1
                    mutPos2 = -1
                    for pos in range(0, 3):
                        if mutsInCodon[pos] == 1 and mutPos1 == -1:
                            mutPos1 = pos
                        elif mutsInCodon[pos] == 1:
                            mutPos2 = pos
                    inBetween1 = consensusCodon[0:mutPos1] + actualCodon[mutPos1] + consensusCodon[mutPos1 + 1:]
                    inBetween2 = consensusCodon[0:mutPos2] + actualCodon[mutPos2] + consensusCodon[mutPos2 + 1:]

                    totSynFound = 0.0
                    totNonSynFound = 0.0
                    if table[consensusCodon] == table[inBetween1]:  # Compare consensus to to first between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween1] == table[actualCodon]:  # Compare first between possibility to actual
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[consensusCodon] == table[inBetween2]:  # Compare consensus to to second between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween2] == table[actualCodon]:  # Compare second between possibility to actual
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0

                    # Determine if actual weightings exceed any others found in this codon column and update if so
                    # Division by 2 for the 2 possible paths
                    if foundSynSite < (totSynFound / 2.0):
                        actualSynChanges += (totSynFound / 2.0) - foundSynSite
                        foundSynSite = (totSynFound / 2.0)
                    if foundNonSynSite < (totNonSynFound / 2.0):
                        actualNonSynChanges += (totNonSynFound / 2.0) - foundNonSynSite
                        foundNonSynSite = (totNonSynFound / 2.0)

                elif sum(mutsInCodon) == 1:
                    if foundSynSite < 1 and table[consensusCodon] == table[actualCodon]:
                        actualSynChanges += 1.0 - foundSynSite
                        foundSynSite = 1.0  # Comment out if counting multiple in one column
                    if foundNonSynSite < 1 and table[consensusCodon] != table[actualCodon]:
                        actualNonSynChanges += 1.0 - foundNonSynSite
                        foundNonSynSite = 1.0  # Comment out if counting multiple in one column

    # Calculate various statistics # 'float' everywhere because thanks python
    try:
        nonMutCopies = int(list(nucDict.keys())[0].split("_")[-3])
    except Exception:
        nonMutCopies = 0
    # harmonicNum = harmonic(numDictSeq + nonMutCopies)  # Harmonic number
    harmonicNum = sum([1.0 / float(i) for i in range(1, numDictSeq + nonMutCopies)])  # numSeq-1th harmonic number
    if potentialSynChanges == 0:
        watsThetaS = 0
    else:
        watsThetaS = float(float(actualSynChanges) / harmonicNum) / potentialSynChanges

    if potentialNonSynChanges == 0:
        watsThetaN = 0
    else:
        watsThetaN = float(float(actualNonSynChanges) / harmonicNum) / potentialNonSynChanges

    if (seqLength - (leadingGaps + trailingGaps)) == 0:
        watsTheta = 0
    else:
        watsTheta = float(float(actualAllChanges) / harmonicNum) / (seqLength - (leadingGaps + trailingGaps))

    with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
        tracker.write("Thetas: Harmonic Number: " + str(harmonicNum) + ". ")
        tracker.write("Potential Syn: " + str(potentialSynChanges) + ". ")
        tracker.write("Potential NonSyn: " + str(potentialNonSynChanges) + ". ")
        tracker.write("Actual Syn: " + str(actualSynChanges) + ". ")
        tracker.write("Actual NonSyn: " + str(actualNonSynChanges) + ". ")
        tracker.write("Actual Mutations: " + str(actualAllChanges) + ". ")

    # thetaByNumStrains is a dictionary containing all values needed to average watsTheta over all same-num-contributor orthogroups
    # It is organized as such:
    # Key = Number of contributing strains
    # Value = List of four items:
    # Item 0 = The cumulative value of each orthogroups' watsThetaS (for all orthogroups belonging to this key)
    # Item 1 = The cumulative value of each orthogroups' watsThetaN (for all orthogroups belonging to this key)
    # Item 2 = The cumulative value of each orthogroups' watsTheta (for all orthogroups belonging to this key)
    # Item 3 = The number of orthogroups seen belonging to this key (the number which the cumulative values are divided by)
    if numStrains not in list(thetaByNumStrains.keys()):
        thetaByNumStrains.update(
            {numStrains: [watsThetaS, watsThetaN, watsTheta, 1]})  # Initialize the key:value for newly encountered key
    else:
        update_sumThetaS = thetaByNumStrains.get(numStrains)[0] + watsThetaS
        update_sumThetaN = thetaByNumStrains.get(numStrains)[1] + watsThetaN
        update_sumTheta = thetaByNumStrains.get(numStrains)[2] + watsTheta
        update_num = thetaByNumStrains.get(numStrains)[3] + 1
        thetaByNumStrains.update({numStrains: [update_sumThetaS, update_sumThetaN, update_sumTheta, update_num]})

    outString = file.split(".")[0] + "\tWatterson's Theta S: " + str(watsThetaS) + "\tWatterson's Theta N: " + str(
        watsThetaN) + "\tWatterson's Theta: " + str(watsTheta) + "\n"
    return outString


def calcPis(nucDict, numStrains, ancestralSeq, file):
    numDictSeq = len(list(nucDict.keys()))
    seqLength = len(list(nucDict.values())[0])

    # All positions with gaps in any sequence are to be discounted
    gapsFound = [0] * seqLength
    for pos in range(0, seqLength):
        for seqIndex in range(0, numDictSeq):
            if list(nucDict.values())[seqIndex][pos] == "_" or list(nucDict.values())[seqIndex][pos] == "-":
                gapsFound[pos] = 1
                break
    if all(gapsFound):
        outString = "ERROR_ALL_GAPS_" + file.split(".")[0] + "\tPi S: NA" + "\tPi N: NA" + "\tPi: NA" + "\n"
        return outString

    potentialSynSites = 0
    potentialNonSynSites = 0
    for i in range(0, seqLength, 3):
        if i + 3 > seqLength:
            continue  # At end of loop with remainder (shouldn't occur in perfect coding sequences)
        consCodon = ancestralSeq[i:i + 3]
        if consCodon in list(synChances.keys()):
            potentialSynSites += sum(synChances[consCodon])
            potentialNonSynSites += (3 - sum(synChances[consCodon]))

    # Processing/counting for Pi values
    synMutations = 0.0
    nonSynMutations = 0.0
    mutations = 0.0

    for index1 in range(0, numDictSeq):
        seq1 = list(nucDict.values())[index1]
        try:
            multiplier1 = 1 + int(list(nucDict.keys())[index1].split("_")[-1])
        except Exception:
            multiplier1 = 1
        for index2 in range(index1 + 1, numDictSeq):
            seq2 = list(nucDict.values())[index2]
            try:
                multiplier2 = 1 + int(list(nucDict.keys())[index2].split("_")[-1])
            except Exception:
                multiplier2 = 1
            for i in range(0, seqLength, 3):
                mutsInCodon = [0, 0, 0]
                for pos in range(0, 3):
                    if i + pos >= seqLength:
                        with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
                            tracker.write("Non-perfect coding sequence. ")
                        continue  # At end of loop with remainder (shouldn't occur in perfect coding sequences)
                    if gapsFound[i + pos] == 1:  # Prevents counting any positions with gaps in any sequence
                        continue
                    if seq1[i + pos] != seq2[i + pos]:  # If base pair at pos differs from other...
                        mutations += (1 * multiplier1 * multiplier2)  # Increases if mutation occurred
                        mutsInCodon[pos] = 1
                if i + 3 > seqLength:
                    with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
                        tracker.write("Non-perfect coding sequence flag 2. ")
                    continue  # At end of loop with remainder (shouldn't occur in perfect coding sequences)
                site1 = seq1[i:i + 3]
                site2 = seq2[i:i + 3]
                if site1 not in list(table.keys()) or site2 not in list(table.keys()):
                    continue

                if sum(mutsInCodon) == 3:  # This gets ridiculous fast...
                    inBetween12_1 = site1[0] + site2[1:]  # Ttt
                    inBetween13_2 = site1[0:2] + site2[2]  # TTt
                    inBetween25_2 = site1[0] + site2[1] + site1[2]  # TtT
                    inBetween34_1 = site2[0] + site1[1] + site2[2]  # tTt
                    inBetween46_2 = site2[0] + site1[1:]  # tTT
                    inBetween56_1 = site2[0:2] + site1[2]  # ttT

                    totSynFound = 0.0
                    totNonSynFound = 0.0
                    # Compare consensus to between possibility part 1 of paths 1 and 2 [Weight = 2]
                    if table[site1] == table[inBetween12_1]:
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    # Compare between possibility part 1 of path 1 to part 2 of path 1
                    if table[inBetween12_1] == table[inBetween13_2]:
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    # Compare between possibility part 2 of paths 1 and 3 to actual [Weight = 2]
                    if table[inBetween13_2] == table[site2]:
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    # Compare between possibility part 1 of path 2 to part 2 of path 2
                    if table[inBetween12_1] == table[inBetween25_2]:
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    # Compare between possibility part 2 of paths 2 and 5 to actual [Weight = 2]
                    if table[inBetween25_2] == table[site2]:
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    # Compare consensus to between possibility part 1 of paths 3 and 4 [Weight = 2]
                    if table[site1] == table[inBetween34_1]:
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    # Compare between possibility part 1 of path 3 to part 2 of path 3
                    if table[inBetween34_1] == table[inBetween13_2]:
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    # Compare between possibility part 1 of path 4 to part 2 of path 4
                    if table[inBetween34_1] == table[inBetween46_2]:
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    # Compare between possibility part 2 of paths 4 and 6 to actual [Weight = 2]
                    if table[inBetween46_2] == table[site2]:
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    # Compare consensus to between possibility part 1 of paths 5 and 6 [Weight = 2]
                    if table[site1] == table[inBetween56_1]:
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    # Compare between possibility part 1 of path 5 to part 2 of path 5
                    if table[inBetween56_1] == table[inBetween25_2]:
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    # Compare between possibility part 1 of path 6 to part 2 of path 6
                    if table[inBetween56_1] == table[inBetween46_2]:
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0

                    # Determine if actual weightings exceed any others found in this codon column and update if so
                    # Division by 6 for the 6 possible paths
                    synMutations += ((totSynFound / 6.0) * multiplier1 * multiplier2)
                    nonSynMutations += ((totNonSynFound / 6.0) * multiplier1 * multiplier2)

                elif sum(mutsInCodon) == 2:
                    mutPos1 = -1
                    mutPos2 = -1
                    for pos in range(0, 3):
                        if mutsInCodon[pos] == 1 and mutPos1 == -1:
                            mutPos1 = pos
                        elif mutsInCodon[pos] == 1:
                            mutPos2 = pos
                    inBetween1 = site1[0:mutPos1] + site2[mutPos1] + site1[mutPos1 + 1:]
                    inBetween2 = site1[0:mutPos2] + site2[mutPos2] + site1[mutPos2 + 1:]
                    totSynFound = 0.0
                    totNonSynFound = 0.0
                    if table[site1] == table[inBetween1]:  # Compare consensus to first between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween1] == table[site2]:  # Compare first between possibility to actual
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[site1] == table[inBetween2]:  # Compare consensus to second between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween2] == table[site2]:  # Compare second between possibility to actual
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0

                    # Determine if actual weightings exceed any others found in this codon column and update if so
                    # Division by 2 for the 2 possible paths
                    synMutations += ((totSynFound / 2.0) * multiplier1 * multiplier2)
                    nonSynMutations += ((totNonSynFound / 2.0) * multiplier1 * multiplier2)

                elif sum(mutsInCodon) == 1:
                    if table[site1] == table[site2]:
                        synMutations += (1.0 * multiplier1 * multiplier2)
                    if table[site1] != table[site2]:
                        nonSynMutations += (1.0 * multiplier1 * multiplier2)

    try:
        nonMutCopies = int(list(nucDict.keys())[0].split("_")[-3])
    except Exception:
        nonMutCopies = 0
    totalSeq = float(numDictSeq + nonMutCopies)
    # perComparison = float(1.0 / ((totalSeq * (totalSeq - 1.0)) / 2.0))  # 1 over the number of theoretical comparisons
    # perComparison = float(1.0 / ((numDictSeq * (numDictSeq - 1.0)) / 2.0))  # 1 over the number of comparisons
    perComparison = (2.0 * totalSeq) / (totalSeq-1)  # Normalizer
    with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
        tracker.write("\nPis: Per-comparison: " + str(perComparison) + ". ")
        tracker.write("Potential Syn: " + str(potentialSynSites) + ". ")
        tracker.write("Potential NonSyn: " + str(potentialNonSynSites) + ". ")
        tracker.write("Actual Syn: " + str(synMutations) + ". ")
        tracker.write("Actual NonSyn: " + str(nonSynMutations) + ". ")
        tracker.write("Actual Mutations: " + str(mutations) + ". ")
    try:
        piS = float(perComparison * synMutations) / potentialSynSites
    except Exception:
        piS = 0.0
    try:
        piN = float(perComparison * nonSynMutations) / potentialNonSynSites
    except Exception:
        piN = 0.0
    pi = float(perComparison * mutations) / (seqLength - sum(gapsFound))

    # piByNumStrains is a dictionary containing all values needed to average pi over all same-num-contributor orthogroups
    # It is organized as such:
    # Key = Number of contributing strains
    # Value = List of four items:
    # Item 0 = The cumulative value of each orthogroups' piS (for all orthogroups belonging to this key)
    # Item 1 = The cumulative value of each orthogroups' piN (for all orthogroups belonging to this key)
    # Item 2 = The cumulative value of each orthogroups' pi (for all orthogroups belonging to this key)
    # Item 3 = The number of orthogroups seen belonging to this key (the number which the cumulative values are divided by)
    if numStrains not in list(piByNumStrains.keys()):
        piByNumStrains.update(
            {numStrains: [float(piS), float(piN), float(pi), 1]})  # Initialize the key:value for newly encountered key
    else:
        update_sumPiS = piByNumStrains.get(numStrains)[0] + float(piS)
        update_sumPiN = piByNumStrains.get(numStrains)[1] + float(piN)
        update_sumPi = piByNumStrains.get(numStrains)[2] + float(pi)
        update_num = piByNumStrains.get(numStrains)[3] + 1
        piByNumStrains.update({numStrains: [update_sumPiS, update_sumPiN, update_sumPi, update_num]})

    with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
        tracker.write("Pis: Past piByNumStrains update. ")

    outString = file.split(".")[0] + "\tPi S: " + str(piS) + "\tPi N: " + str(piN) + "\tPi: " + str(pi) + "\n"
    return outString


with open("final_output/" + specName + "/wattersonsThetaValues.txt", "w") as f:
    with open("final_output/" + specName + "/piValues.txt", "w") as f2:
        # f3 would have been dendropy, but this is not achievable without creating a full dna matrix of too many ancestral sequence copies
        with open("final_output/" + specName + "/consensusSeqs.txt", "w") as f4:
            with open("final_output/" + specName + "/GC_values.txt", "a+") as gc_file:
                gc_file.truncate(0)  # To clear the file for later appends
            with open("final_output/" + specName + "/" + specName + "_MutationCalls.txt", "a+") as mutCalls:
                mutCalls.truncate(0)  # To clear the file for later appends
            with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
                tracker.truncate(0)  # To clear the file for later appends
            warnings = []
            for ogFile in os.listdir("modifiedAlignmentInput/" + specName + "/"):
                filePath = os.path.join("modifiedAlignmentInput/", specName, ogFile)
                currNucDict = buildNucDict(filePath)
                with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
                    tracker.write("Processing " + ogFile + " with nucDict of length " + str(len(currNucDict)) + ". ")
                # nucDict is a dictionary of sequence names mapped to actual sequences.
                # the sequences are aligned coding sequences, thus equal length and divisible by 3
                # Number of contributing strains is indicated by first num before _ in file name (e.g. 3_OG0000123.fa has 3 contributing strains)
                try:
                    currNumStrains = int(ogFile.split("_")[0])
                except Exception:
                    warnings.append(ogFile)
                    currNumStrains = "-1"  # Indicates that strain number is not being considered as a factor

                try:
                    currConsensus = list(currNucDict.values())[0]
                    thisTheta = calcThetas(currNucDict, currNumStrains, currConsensus, ogFile)
                    f.write(thisTheta)
                    # f2.write(calcPis(currNucDict, currNumStrains, currConsensus, ogFile))
                    f4.write(">" + ogFile + "\n" + currConsensus + "\n")
                    with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
                        tracker.write(ogFile + " processed with theta " + str(thisTheta) + ".\n")
                except Exception as e:
                    with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
                        tracker.write("ERROR: " + ogFile + " failed to process.\n")
                        tracker.write(str(e))

if len(warnings) > 0:
    with open("final_output/" + specName + "/Warnings.txt", "w") as warn_file:
        warn_file.write(
            "File names did not all convey the number of strains; two-step averaging may be inaccurate if some and not all were conveyed. Files not conveyed:\n")
        for warning in warnings:
            warn_file.write(warning + "\n")

with open("final_output/" + specName + "/GC_values.txt", "r+") as gc_file:
    gc_sum = 0.0
    count_GCs = 0
    for line in gc_file.readlines():
        gc_sum += float(line.strip())
        count_GCs += 1

    if count_GCs == 0:
        avg_GC = -1  # Error occurs when no GC_values file exists, usually due to a run of the same species being started too soon before another finishes.
    else:
        avg_GC = gc_sum / count_GCs
    currDate = datetime.datetime.now().strftime("%b%d")
    with open("consolidated_output/GC_Values_" + currDate + ".txt", "a+") as consGC:
        with open("final_output/" + specName + "/GC_Content.txt", "w") as finGC:
            finGC.write(specName + "\t" + str(avg_GC) + "\n")
            consGC.write(specName + "\t" + str(avg_GC) + "\n")

sumOfAllAvgThetaS = 0.0
sumOfAllAvgThetaN = 0.0
sumOfAllAvgTheta = 0.0
sumOfAllAvgPiS = 0.0
sumOfAllAvgPiN = 0.0
sumOfAllAvgPi = 0.0
allCountThetas = 0  # These allCounts may (always?) be the same, but are listed distinctly in case not
allCountPis = 0

# xByNumStrains are dictionaries containing all values needed to average the stat x over all same-num-contributor orthogroups
# It is organized as such:
# Key = Number of contributing strains
# Value = List of three items:
# Item 0 = The cumulative value of each orthogroups' xS (for all orthogroups belonging to this key; Synonymous only)
# Item 1 = The cumulative value of each orthogroups' xN (for all orthogroups belonging to this key; Nonsynonymous only)
# Item 2 = The cumulative value of each orthogroups' x (for all orthogroups belonging to this key)
# Item 3 = The number of orthogroups seen belonging to this key (the number which the cumulative values are divided by)

for key in list(thetaByNumStrains.keys()):
    # Acquires average thetas of all groups with the same number of contributing strains (S for silent, N for non-silent, no mark for no regard)
    valueTheta = thetaByNumStrains.get(key)
    avgForNumThetaS = float(valueTheta[0]) / valueTheta[3]
    avgForNumThetaN = float(valueTheta[1]) / valueTheta[3]
    avgForNumTheta = float(valueTheta[2]) / valueTheta[3]
    sumOfAllAvgThetaS += float(avgForNumThetaS)
    sumOfAllAvgThetaN += float(avgForNumThetaN)
    sumOfAllAvgTheta += float(avgForNumTheta)

    allCountThetas += 1

with open("final_output/" + specName + "/" + specName + "_ModifiedTracker.txt", "a+") as tracker:
    tracker.write(specName + " average step 1 theta: " + str(sumOfAllAvgTheta) + "with allCountThetas of ." + str(allCountThetas) + "\n")

for key in list(piByNumStrains.keys()):
    # Acquires average pis of all groups with the same number of contributing strains (S for silent, N for non-silent, no mark for no regard)
    valuePi = piByNumStrains.get(key)
    avgForNumPiS = float(valuePi[0]) / valuePi[3]
    avgForNumPiN = float(valuePi[1]) / valuePi[3]
    avgForNumPi = float(valuePi[2]) / valuePi[3]
    sumOfAllAvgPiS += float(avgForNumPiS)
    sumOfAllAvgPiN += float(avgForNumPiN)
    sumOfAllAvgPi += float(avgForNumPi)

    allCountPis += 1

# Acquires average of all the averages of groups with the same number of contributing strains (S for silent, N for non-silent, no mark for no regard)
avgWatsThetaS = float(sumOfAllAvgThetaS) / allCountThetas if allCountThetas != 0 else -1
avgWatsThetaN = float(sumOfAllAvgThetaN) / allCountThetas if allCountThetas != 0 else -1
avgWatsTheta = float(sumOfAllAvgTheta) / allCountThetas if allCountThetas != 0 else -1
avgPiS = float(sumOfAllAvgPiS) / allCountPis if allCountPis != 0 else -1
avgPiN = float(sumOfAllAvgPiN) / allCountPis if allCountPis != 0 else -1
avgPi = float(sumOfAllAvgPi) / allCountPis if allCountPis != 0 else -1

print((str(avgWatsThetaS) + "," + str(avgWatsThetaN) + "," + str(avgWatsTheta)
      + "," + str(avgPiS) + "," + str(avgPiN) + "," + str(avgPi)
      + "," + str(-1) + "," + str(-1)))
