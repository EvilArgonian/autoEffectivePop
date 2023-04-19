import os
import sys
import argparse
import shutil

def main():
    # Initialize parser
    parser = argparse.ArgumentParser(description="Run the input setup tool for the core gene finder.")
    # Adding input_species argument as
    parser.add_argument('-f', "--Force", action='store_true', help='Flag to indicate that the setup should clear and rewrite the input.')
    # Read arguments from command line
    args = parser.parse_args()

    if not os.path.exists("consensus_input/"):
        os.mkdir("consensus_input/")

    missingConsensus = []
    for speciesFolder in os.listdir("../final_output/")
        inFolder = os.path("../final_output/", speciesFolder)
        outFolder = os.path("consensus_input",speciesFolder)
        inConsensusFile = os.path.join(inFolder, "consensusSeqs.txt")
        outConsensusFile = os.path.join(outFolder, speciesFolder,".txt")
        if os.path.exists(outFolder):
            if os.path.exists(outConsensusFile):
                if args.force:
                    os.remove(outConsensusFile)
                else:
                    print(speciesFolder + " already has input here; Skipping.")
                    continue
        else:
            os.mkdir(outFolder)

        if os.path.exists(inConsensusFile):
            shutil.copy(inConsensusFile, outConsensusFile) # Copy and rename to species name
        else:
            missingConsensus.append(speciesFolder)
            print(speciesFolder + " did not have an associated consensus file!")

    with open("missingConsensus.txt", "w") as missingFile:
        for spec in missingConsensus:
            missingFile.write(spec + "\n")

if __name__ == '__main__':
    main()
