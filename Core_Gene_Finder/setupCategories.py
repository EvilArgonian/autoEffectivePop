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
    parser.add_argument('-f', '--force', action='store_true',
                        help='Flag to indicate that the setup should clear and rewrite the input.')
    # Adding dehyphenate argument as
    # parser.add_argument('-dh', '--dehyphenate', action='store_true',
    #                    help='Flag to indicate using the secondary function to remove all hyphens from already otherwise setup categories.')
    # Read arguments from command line
    args = parser.parse_args()

    if not os.path.exists("categories/"):
        os.mkdir("categories/")

    # if args.dehyphenate:
    #     for category in os.listdir("categories/"):
    #         for species in os.listdir(os.path.join("categories/", category)):
    #             for fileName in os.listdir(os.path.join("categories/", category, species)):
    #                if fileName.endswith(".txt"):
    #                     with open(os.path.join("categories/", category, species, fileName), "w+") as f:
    #                         replaceStr = ""
    #                         for line in f.readlines():
    #                             if not line.startswith(">"):
    #                                 replaceStr += line.replace("-", "")
    #                             else:
    #                                 replaceStr += line
    #                         f.truncate(0)
    #                         f.write(replaceStr)
    #     exit()

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
            categories.append(elem.strip())

        inFolder = os.path.join("../final_output/", species)
        inConsensusFile = os.path.join(inFolder, "consensusSeqs.txt")
        if os.path.exists(inConsensusFile):
            for category in categories:
                category = category.title().replace(" ", "_")
                catFolder = os.path.join("categories", category)
                if not os.path.exists(catFolder):
                    os.mkdir(catFolder)
                outFolder = os.path.join(catFolder, species)
                outConsensusFile = os.path.join(outFolder, str(species + ".txt"))
                if os.path.exists(outFolder):
                    if os.path.exists(outConsensusFile):
                        if args.force:
                            os.remove(outConsensusFile)
                        else:
                            print(species + " already has input in category " + category + "; Skipping.")
                            continue
                else:
                    os.mkdir(outFolder)
                # Copy and rename to species name, losing hyphens
                with open(inConsensusFile, "r") as inF:
                    with open(outConsensusFile) as outF:
                        for copyLine in inF.readlines():
                            if not copyLine.startswith(">"):
                                outF.write(copyLine.replace("-", ""))
                            else:
                                outF.write(copyLine)
        else:
            missingConsensus.append(species)
            print(species + " did not have an associated consensus file!")

    with open("missingConsensus.txt", "w") as missingFile:
        for spec in missingConsensus:
            missingFile.write(spec + " ")


if __name__ == '__main__':
    main()
