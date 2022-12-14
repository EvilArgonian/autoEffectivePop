import os
import sys
import dendropy
import re
import datetime

specName = sys.argv[1]

table = {
    # 'M' - START, '_' - STOP
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TGT": "C", "TGC": "C",
    "GAT": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",
    "TTT": "F", "TTC": "F",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    "CAT": "H", "CAC": "H",
    "ATA": "I", "ATT": "I", "ATC": "I",
    "AAA": "K", "AAG": "K",
    "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATG": "M",
    "AAT": "N", "AAC": "N",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TGG": "W",
    "TAT": "Y", "TAC": "Y",
    "TAA": "_", "TAG": "_", "TGA": "_"
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
dendropyByNumStrains = {}


class TestComplementLocationException(Exception):
    def __init__(self, actualPos, message="Actual Position: "):
        self.actualPos = actualPos
        self.message = message + str(actualPos)
        super(Exception, self).__init__(self.message)


class UnfoundLocationException(Exception):
    def __init__(self, message="Location Not Identified"):
        self.message = message
        super(Exception, self).__init__(self.message)


def buildNucDict(specName, file):
    # Building sequences for processing
    nucDict = {}
    nucSeqTitle = ""
    nucSeqBuilder = ""
    for line in open("muscle_output/" + specName + "/" + file, "r").readlines():
        if line.startswith(">"):
            if nucSeqTitle != "":
                nucDict.update({nucSeqTitle: nucSeqBuilder})
            nucSeqTitle = line.strip()
            nucSeqBuilder = ""
        else:
            nucSeqBuilder += line.strip()
    nucDict.update({nucSeqTitle: nucSeqBuilder})
    return nucDict


def getConsensus(nucDict):
    # Simple algorithm for determining consensus sequence; no fancy parameters involved
    seqLength = len(nucDict.values()[0])
    numSeq = len(nucDict.keys())
    consensus = ""
    GC_sum = 1
    for pos in range(0, seqLength):
        freqDict = {'A': 0, 'C': 0, 'G': 0, 'T': 0, '-': 0}
        for i in range(0, numSeq):
            nuc = (nucDict.values()[i][pos]).upper()
            if nuc == '_':  # Corrective in case '_' is used to mark gaps instead of '-'
                nuc = '-'
            if nuc not in freqDict.keys():  # Encountered rarely. N's for unknown, perhaps?
                continue
            freqDict.update({nuc: freqDict.get(nuc) + 1})
        # Favors A, C, G, T, _ in that order for breaking ties
        highest = freqDict.get('A')
        highestNuc = 'A'
        if freqDict.get('C') > highest:
            highest = freqDict.get('C')
            highestNuc = 'C'
        if freqDict.get('G') > highest:
            highest = freqDict.get('G')
            highestNuc = 'G'
        if freqDict.get('T') > highest:
            highest = freqDict.get('T')
            highestNuc = 'T'
        if freqDict.get('-') > highest:
            highest = freqDict.get('-')
            highestNuc = '-'
        consensus += highestNuc

        if highestNuc == 'G' or highestNuc == 'C':
            GC_sum += 1

    with open("final_output/" + specName + "/GC_values.txt", "a+") as gc_file:
        gc_file.write(str(float(GC_sum) / seqLength) + "\n")

    return consensus


def getComplement(nucStr):
    if nucStr == "BEG" or nucStr == "END":
        return nucStr # Should this switch BEG and END?
    outStr = ""
    for nuc in nucStr:
        if nuc == 'A':
            outStr += 'T'
        elif nuc == 'T':
            outStr+='A'
        elif nuc == 'C':
            outStr += 'G'
        elif nuc == 'G':
            outStr += 'C'
    return outStr


def calcThetas(nucDict, numStrains, ancestralSeq):
    # Processing/counting for Watterson's Theta & Theta S values
    numSeq = len(nucDict.keys())
    seqLength = len(nucDict.values()[0])

    # Create a pair of forward and backward facing loops to determine the longest leading/trailing gap sequences;
    # Remove all positions within these from any calculations (no changes counted, not counted against length)
    gapLengths = [0.0] * numSeq  # Initialize counts of leading gaps
    gapsEnded = [False] * numSeq  # Initialize flags for leading gap ends
    for pos in range(0, seqLength):
        for seqIndex in range(0, numSeq):
            if not gapsEnded[seqIndex]:
                if nucDict.values()[seqIndex][pos] == "_" or nucDict.values()[seqIndex][pos] == "-":
                    gapLengths[seqIndex] += 1.0
                else:
                    gapsEnded[seqIndex] = True
        if all(gapsEnded):  # If all leading gaps have already ended
            break
    leadingGaps = max(gapLengths)

    gapLengths = [0.0] * numSeq  # Initialize counts of trailing gaps
    gapsEnded = [False] * numSeq  # Initialize flags for trailing gap ends
    for pos in range(seqLength - 1, -1, -1):
        for seqIndex in range(0, numSeq):
            if not gapsEnded[seqIndex]:
                if nucDict.values()[seqIndex][pos] == "_" or nucDict.values()[seqIndex][pos] == "-":
                    gapLengths[seqIndex] += 1.0
                else:
                    gapsEnded[seqIndex] = True
        if all(gapsEnded):  # If all leading gaps have already ended
            break
    trailingGaps = max(gapLengths)

    with open("final_output/" + specName + "/" + specName + "_MutationCalls.txt", "a") as mutCalls:
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
            if consensusCodon in synChances.keys():
                potentialSynChanges += sum(synChances[consensusCodon])
                potentialNonSynChanges += (3 - sum(synChances[consensusCodon]))
            for seqIndex in range(0, numSeq):
                actualCodon = nucDict.values()[seqIndex][i:i + 3]
                mutsInCodon = [0, 0, 0]
                for pos in range(0, 3):
                    if i + pos < leadingGaps or i + pos >= seqLength - trailingGaps:
                        continue  # Ignore positions within the leading and trailing gap sections
                    if not consensusCodon in table.keys() or not actualCodon in table.keys():
                        continue
                    if pos >= len(consensusCodon) or pos >= len(actualCodon):
                        continue
                    if consensusCodon[pos] != actualCodon[pos]:
                        mutsInCodon[pos] = 1
                        strainName = re.search("\[strain=(.+?)\]", nucDict.keys()[seqIndex]).group(1)
                        geneName = nucDict.keys()[seqIndex].split(" ")[0]
                        synStatus = "S" if table[consensusCodon] == table[actualCodon] else "N" # Technically could be inaccurate in codons with 2 or 3 mutations; minor difference.
                        twoLeft = "BEG" if i+pos-2 < leadingGaps else ancestralSeq[i+pos-2]
                        oneLeft = "BEG" if i + pos - 1 < leadingGaps else ancestralSeq[i + pos - 1]
                        middle = ancestralSeq[i+pos]
                        oneRight = "END" if i +pos + 1 >= seqLength - trailingGaps else ancestralSeq[i + pos + 1]
                        twoRight = "END" if i + pos + 2 >= seqLength - trailingGaps else ancestralSeq[i + pos + 2]
                        adjPos = "Err"
                        try:
                            actualPos = re.search("\[location=(.+?)\]", nucDict.keys()[seqIndex]).group(1)
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
                            callOutput = specName + ", " + strainName + ", " + geneName + ", " + synStatus + ", " + adjPos + ", " + twoLeft + ", " + oneLeft + ", " + middle + ", " + nucDict.values()[seqIndex][i + pos] + ", " + oneRight + ", " + twoRight + "\n"
                            mutCalls.write(callOutput)
                        except Exception:
                            callOutput = specName + ", " + strainName + ", " + geneName + ", " + synStatus + ", " + adjPos + ", " + twoLeft + ", " + oneLeft + ", " + middle + ", " + nucDict.values()[seqIndex][i + pos] + ", " + oneRight + ", " + twoRight + "\n"
                            mutCalls.write(callOutput)
                        if not foundSegSite[pos]:
                            actualAllChanges += 1
                            foundSegSite[pos] = True  # Comment out if counting multiple in one column
                if i < leadingGaps or i >= seqLength - trailingGaps:
                    continue  # Ignore positions within the leading and trailing gap sections
                if consensusCodon not in table.keys() or actualCodon not in table.keys():
                    continue
                if sum(mutsInCodon) == 3: # This gets ridiculous fast...
                    inBetween12_1 = actualCodon[0] + consensusCodon[1:] # Ttt
                    inBetween13_2 = actualCodon[0:2] + consensusCodon[2] # TTt
                    inBetween25_2 = actualCodon[0] + consensusCodon[1] + actualCodon[2]  # TtT
                    inBetween34_1 = consensusCodon[0] + actualCodon[1] + consensusCodon[2] # tTt
                    inBetween46_2 = consensusCodon[0] + actualCodon[1:] # tTT
                    inBetween56_1 = consensusCodon[0:2] + actualCodon[2] # ttT

                    totSynFound = 0.0
                    totNonSynFound = 0.0
                    if table[consensusCodon] == table[inBetween12_1]:  # Compare consensus to between possibility part 1 of paths 1 and 2 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween12_1] == table[inBetween13_2]:  # Compare between possibility part 1 of path 1 to part 2 of path 1
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween13_2] == table[actualCodon]:  # Compare between possibility part 2 of paths 1 and 3 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween12_1] == table[inBetween25_2]: # Compare between possibility part 1 of path 2 to part 2 of path 2
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween25_2] == table[actualCodon]:  # Compare between possibility part 2 of paths 2 and 5 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[consensusCodon] == table[inBetween34_1]: # Compare consensus to between possibility part 1 of paths 3 and 4 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween34_1] == table[inBetween13_2]: # Compare between possibility part 1 of path 3 to part 2 of path 3
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween34_1] == table[inBetween46_2]:  # Compare between possibility part 1 of path 4 to part 2 of path 4
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween46_2] == table[actualCodon]:  # Compare between possibility part 2 of paths 4 and 6 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[consensusCodon] == table[inBetween56_1]:  # Compare consensus to between possibility part 1 of paths 5 and 6 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween56_1] == table[inBetween25_2]:  # Compare between possibility part 1 of path 5 to part 2 of path 5
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween56_1] == table[inBetween46_2]:  # Compare between possibility part 1 of path 6 to part 2 of path 6
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
                    if table[consensusCodon] == table[inBetween1]: # Compare consensus to to first between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween1] == table[actualCodon]:# Compare first between possibility to actual
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[consensusCodon] == table[inBetween2]: # Compare consensus to to second between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween2] == table[actualCodon]: # Compare second between possibility to actual
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
    harmonic = sum([1.0 / float(i) for i in range(1, numSeq)])  # numSeq-1th harmonic number
    if potentialSynChanges == 0:
        watsThetaS = 0
    else:
        watsThetaS = float(float(actualSynChanges) / harmonic) / potentialSynChanges

    if potentialNonSynChanges == 0:
        watsThetaN = 0
    else:
        watsThetaN = float(float(actualNonSynChanges) / harmonic) / potentialNonSynChanges

    if (seqLength - (leadingGaps + trailingGaps)) == 0:
        watsTheta = 0
    else:
        watsTheta = float(float(actualAllChanges) / harmonic) / (seqLength - (leadingGaps + trailingGaps))

    # thetaByNumStrains is a dictionary containing all values needed to average watsTheta over all same-num-contributor orthogroups
    # It is organized as such:
    # Key = Number of contributing strains
    # Value = List of four items:
    # Item 0 = The cumulative value of each orthogroups' watsThetaS (for all orthogroups belonging to this key)
    # Item 1 = The cumulative value of each orthogroups' watsThetaN (for all orthogroups belonging to this key)
    # Item 2 = The cumulative value of each orthogroups' watsTheta (for all orthogroups belonging to this key)
    # Item 3 = The number of orthogroups seen belonging to this key (the number which the cumulative values are divided by)
    if not numStrains in thetaByNumStrains.keys():
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


def calcPis(nucDict, numStrains, ancestralSeq):
    numSeq = len(nucDict.keys())
    seqLength = len(nucDict.values()[0])

    # All positions with gaps in any sequence are to be discounted
    gapsFound = [0] * seqLength
    for pos in range(0, seqLength):
        for seqIndex in range(0, numSeq):
            if nucDict.values()[seqIndex][pos] == "_" or nucDict.values()[seqIndex][pos] == "-":
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
        if consCodon in synChances.keys():
            potentialSynSites += sum(synChances[consCodon])
            potentialNonSynSites += (3 - sum(synChances[consCodon]))

    # Processing/counting for Pi values
    synMutations = 0.0
    nonSynMutations = 0.0
    mutations = 0.0


    for index1 in range(0, numSeq):
        seq1 = nucDict.values()[index1]
        for index2 in range(index1 + 1, numSeq):
            seq2 = nucDict.values()[index2]
            for i in range(0, seqLength, 3):
                mutsInCodon = [0, 0, 0]
                for pos in range(0, 3):
                    if i + pos >= seqLength:
                        continue  # At end of loop with remainder (shouldn't occur in perfect coding sequences)
                    if gapsFound[i + pos] == 1:  # Prevents counting any positions with gaps in any sequence
                        continue
                    if seq1[i + pos] != seq2[i + pos]:  # If base pair at pos differs from other...
                        mutations += 1  # Increases if mutation occurred
                        mutsInCodon[pos] = 1
                if i + 3 > seqLength:
                    continue  # At end of loop with remainder (shouldn't occur in perfect coding sequences)
                site1 = seq1[i:i + 3]
                site2 = seq2[i:i + 3]
                if site1 not in table.keys() or site2 not in table.keys():
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
                    if table[site1] == table[inBetween12_1]:  # Compare consensus to between possibility part 1 of paths 1 and 2 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween12_1] == table[inBetween13_2]:  # Compare between possibility part 1 of path 1 to part 2 of path 1
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween13_2] == table[site2]:  # Compare between possibility part 2 of paths 1 and 3 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween12_1] == table[inBetween25_2]:  # Compare between possibility part 1 of path 2 to part 2 of path 2
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween25_2] == table[site2]:  # Compare between possibility part 2 of paths 2 and 5 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[site1] == table[inBetween34_1]:  # Compare consensus to between possibility part 1 of paths 3 and 4 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween34_1] == table[inBetween13_2]:  # Compare between possibility part 1 of path 3 to part 2 of path 3
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween34_1] == table[inBetween46_2]:  # Compare between possibility part 1 of path 4 to part 2 of path 4
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween46_2] == table[site2]:  # Compare between possibility part 2 of paths 4 and 6 to actual [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[site1] == table[inBetween56_1]:  # Compare consensus to between possibility part 1 of paths 5 and 6 [Weight = 2]
                        totSynFound += 2.0
                    else:
                        totNonSynFound += 2.0
                    if table[inBetween56_1] == table[inBetween25_2]:  # Compare between possibility part 1 of path 5 to part 2 of path 5
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween56_1] == table[inBetween46_2]:  # Compare between possibility part 1 of path 6 to part 2 of path 6
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0

                    # Determine if actual weightings exceed any others found in this codon column and update if so
                    # Division by 6 for the 6 possible paths
                    synMutations += (totSynFound / 6.0)
                    nonSynMutations += (totNonSynFound / 6.0)

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
                    if table[site1] == table[inBetween1]:  # Compare consensus to to first between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween1] == table[site2]:  # Compare first between possibility to actual
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[site1] == table[inBetween2]:  # Compare consensus to to second between possibility
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0
                    if table[inBetween2] == table[site2]:  # Compare second between possibility to actual
                        totSynFound += 1.0
                    else:
                        totNonSynFound += 1.0

                    # Determine if actual weightings exceed any others found in this codon column and update if so
                    # Division by 2 for the 2 possible paths
                    synMutations += (totSynFound / 2.0)
                    nonSynMutations += (totNonSynFound / 2.0)

                elif sum(mutsInCodon) == 1:
                    if table[site1] == table[site2]:
                        synMutations += 1.0
                    if table[site1] != table[site2]:
                        nonSynMutations += 1.0

    perComparison = float(1.0 / ((numSeq * (numSeq - 1)) / 2))  # 1 over the number of comparisons
    piS = float(perComparison * synMutations) / potentialSynSites
    piN = float(perComparison * nonSynMutations) / potentialNonSynSites
    pi = float(perComparison * mutations) / (seqLength - sum(gapsFound))

    # piByNumStrains is a dictionary containing all values needed to average pi over all same-num-contributor orthogroups
    # It is organized as such:
    # Key = Number of contributing strains
    # Value = List of four items:
    # Item 0 = The cumulative value of each orthogroups' piS (for all orthogroups belonging to this key)
    # Item 1 = The cumulative value of each orthogroups' piN (for all orthogroups belonging to this key)
    # Item 2 = The cumulative value of each orthogroups' pi (for all orthogroups belonging to this key)
    # Item 3 = The number of orthogroups seen belonging to this key (the number which the cumulative values are divided by)
    if numStrains not in piByNumStrains.keys():
        piByNumStrains.update(
            {numStrains: [float(piS), float(piN), float(pi), 1]})  # Initialize the key:value for newly encountered key
    else:
        update_sumPiS = piByNumStrains.get(numStrains)[0] + float(piS)
        update_sumPiN = piByNumStrains.get(numStrains)[1] + float(piN)
        update_sumPi = piByNumStrains.get(numStrains)[2] + float(pi)
        update_num = piByNumStrains.get(numStrains)[3] + 1
        piByNumStrains.update({numStrains: [update_sumPiS, update_sumPiN, update_sumPi, update_num]})

    outString = file.split(".")[0] + "\tPi S: " + str(piS) + "\tPi N: " + str(piN) + "\tPi: " + str(pi) + "\n"
    return outString


def calcDendropy(nucDict, numStrains, file):
    seqLength = len(nucDict.values()[0])

    dnaMatrix = dendropy.DnaCharacterMatrix.get(
        path="muscle_output/" + specName + "/" + file,
        schema="fasta"
    )

    dendropyTheta = dendropy.calculate.popgenstat.wattersons_theta(dnaMatrix) / seqLength # Dendropy does not appear to already divide by seqLength (Should I worry about leading/trailing gaps?)
    dendropyPi = dendropy.calculate.popgenstat.nucleotide_diversity(dnaMatrix)  # / seqLength

    # dendropyByNumStrains is a dictionary containing all values needed to average Dendropy Theta and Pi over all same-num-contributor orthogroups
    # It is organized as such:
    # Key = Number of contributing strains
    # Value = List of three items:
    # Item 0 = The cumulative value of each orthogroups' Dendropy Theta (for all orthogroups belonging to this key)
    # Item 1 = The cumulative value of each orthogroups' Dendropy Pi  (for all orthogroups belonging to this key)
    # Item 2 = The number of orthogroups seen belonging to this key (the number which the cumulative values are divided by)
    if numStrains not in dendropyByNumStrains.keys():
        dendropyByNumStrains.update({numStrains: [dendropyTheta, dendropyPi, 1]})  # Initialize the key:value for newly encountered key
    else:
        update_sumTheta = dendropyByNumStrains.get(numStrains)[0] + dendropyTheta
        update_sumPi = dendropyByNumStrains.get(numStrains)[1] + dendropyPi
        update_num = dendropyByNumStrains.get(numStrains)[2] + 1
        dendropyByNumStrains.update({numStrains: [update_sumTheta, update_sumPi, update_num]})


    outString = file.split(".")[0] + "\tDendropy Watterson's Theta: " + str(dendropyTheta) + "\tDendropy Pi: " + str(dendropyPi) + "\n"
    return outString


with open("final_output/" + specName + "/wattersonsThetaValues.txt", "w") as f:
    with open("final_output/" + specName + "/piValues.txt", "w") as f2:
        with open("final_output/" + specName + "/dendropyValues.txt", "w") as f3:
            with open("final_output/" + specName + "/GC_values.txt", "a+") as gc_file:
                gc_file.truncate(0)  # To clear the file for later appends
            for file in os.listdir("muscle_output/" + specName + "/"):
                nucDict = buildNucDict(specName, file)
                # nucDict is a dictionary of sequence names mapped to actual sequences.
                # the sequences are aligned coding sequences, thus equal length and divisible by 3

                if len(nucDict) < 2:
                    continue

                # Number of contributing strains is indicated by first num before _ in file name (e.g. 3_OG0000123.fa has 3 contributing strains)
                numStrains = file.split("_")[0]
                consensus = getConsensus(nucDict)
                f.write(calcThetas(nucDict, numStrains, consensus))
                f2.write(calcPis(nucDict, numStrains, consensus))
                f3.write(calcDendropy(nucDict, numStrains, file))

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
sumOfAllAvgDendropyTheta = 0.0
sumOfAllAvgDendropyPi = 0.0
allCountThetas = 0  # These allCounts may (always?) be the same, but are listed distinctly in case not
allCountPis = 0
allCountDendropies = 0

# xByNumStrains are dictionaries containing all values needed to average the stat x over all same-num-contributor orthogroups
# It is organized as such:
# Key = Number of contributing strains
# Value = List of three items:
# Item 0 = The cumulative value of each orthogroups' xS (for all orthogroups belonging to this key; Synonymous only)
# Item 1 = The cumulative value of each orthogroups' xN (for all orthogroups belonging to this key; Nonsynonymous only)
# Item 2 = The cumulative value of each orthogroups' x (for all orthogroups belonging to this key)
# Item 3 = The number of orthogroups seen belonging to this key (the number which the cumulative values are divided by)

for key in thetaByNumStrains.keys():
    # Acquires average thetas of all groups with the same number of contributing strains (S for silent, N for non-silent, no mark for no regard)
    valueTheta = thetaByNumStrains.get(key)
    avgForNumThetaS = float(valueTheta[0]) / valueTheta[3]
    avgForNumThetaN = float(valueTheta[1]) / valueTheta[3]
    avgForNumTheta = float(valueTheta[2]) / valueTheta[3]
    sumOfAllAvgThetaS += float(avgForNumThetaS)
    sumOfAllAvgThetaN += float(avgForNumThetaN)
    sumOfAllAvgTheta += float(avgForNumTheta)

    allCountThetas += 1

for key in piByNumStrains.keys():
    # Acquires average pis of all groups with the same number of contributing strains (S for silent, N for non-silent, no mark for no regard)
    valuePi = piByNumStrains.get(key)
    avgForNumPiS = float(valuePi[0]) / valuePi[3]
    avgForNumPiN = float(valuePi[1]) / valuePi[3]
    avgForNumPi = float(valuePi[2]) / valuePi[3]
    sumOfAllAvgPiS += float(avgForNumPiS)
    sumOfAllAvgPiN += float(avgForNumPiN)
    sumOfAllAvgPi += float(avgForNumPi)

    allCountPis += 1

for key in dendropyByNumStrains.keys():
    # Acquires average pis of all groups with the same number of contributing strains (S for silent, N for non-silent, no mark for no regard)
    valueDendropy = dendropyByNumStrains.get(key)
    avgForNumDendropyTheta = float(valueDendropy[0]) / valueDendropy[2]
    avgForNumDendropyPi = float(valueDendropy[1]) / valueDendropy[2]
    sumOfAllAvgDendropyTheta += float(avgForNumDendropyTheta)
    sumOfAllAvgDendropyPi += float(avgForNumDendropyPi)

    allCountDendropies += 1

# Acquires average of all the averages of groups with the same number of contributing strains (S for silent, N for non-silent, no mark for no regard)
avgWatsThetaS = float(sumOfAllAvgThetaS) / allCountThetas if allCountThetas != 0 else -1
avgWatsThetaN = float(sumOfAllAvgThetaN) / allCountThetas if allCountThetas != 0 else -1
avgWatsTheta = float(sumOfAllAvgTheta) / allCountThetas if allCountThetas != 0 else -1
avgPiS = float(sumOfAllAvgPiS) / allCountPis if allCountPis != 0 else -1
avgPiN = float(sumOfAllAvgPiN) / allCountPis if allCountPis != 0 else -1
avgPi = float(sumOfAllAvgPi) / allCountPis if allCountPis != 0 else -1
avgDendropyTheta = float(sumOfAllAvgDendropyTheta) / allCountDendropies if allCountDendropies != 0 else -1
avgDendropyPi = float(sumOfAllAvgDendropyPi) / allCountDendropies if allCountDendropies != 0 else -1

print(str(avgWatsThetaS) + "," + str(avgWatsThetaN) + "," + str(avgWatsTheta)
      + "," + str(avgPiS) + "," + str(avgPiN) + "," + str(avgPi)
      + "," + str(avgDendropyTheta) + "," + str(avgDendropyPi))

