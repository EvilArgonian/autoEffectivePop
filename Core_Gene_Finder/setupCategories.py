import os
import sys
import argparse
import shutil


def main():
    # Initialize parser
    parser = argparse.ArgumentParser(description="Run the input setup tool for the core gene finder.")
    # Adding category_reference argument as
    parser.add_argument('category_reference', type=argparse.FileType('r'),
                        help='Reference text file that indicates the categories each species belongs to. The format of each line should be the species name followed by each category it belongs to, tab-delimited.')
    # Adding force argument as
    parser.add_argument('-f', '--Force', action='store_true',
                        help='Flag to indicate that the setup should clear and rewrite the input.')
    # Read arguments from command line
    args = parser.parse_args()

    if not os.path.exists("consensus_input/"):
        os.mkdir("consensus_input/")

    missingConsensus = []
    for line in args.category_reference.readlines():
        lineElems = line.split("\t")
        species = lineElems[0]
        categories = ["All"]
        skipName = True
        for elem in lineElems:
            if skipName:
                skipName = False
                continue
            categories.append(elem)

        inFolder = os.path("../final_output/", species)
        inConsensusFile = os.path.join(inFolder, "consensusSeqs.txt")
        if os.path.exists(inConsensusFile):
            for category in categories:
                outFolder = os.path("consensus_input", category, species)
                outConsensusFile = os.path.join(outFolder, species, ".txt")
                if os.path.exists(outFolder):
                    if os.path.exists(outConsensusFile):
                        if args.force:
                            os.remove(outConsensusFile)
                        else:
                            print(species + " already has input in category " + category + "; Skipping.")
                            continue
                else:
                    os.mkdir(outFolder)
                shutil.copy(inConsensusFile, outConsensusFile)  # Copy and rename to species name
        else:
            missingConsensus.append(species)
            print(species + " did not have an associated consensus file!")

    with open("missingConsensus.txt", "w") as missingFile:
        for spec in missingConsensus:
            missingFile.write(spec + "\n")


if __name__ == '__main__':
    main()
