# file app/__main__.py

import pkg_resources
import argparse
import subprocess


# print(pkg_resources.resource_string('resources', 'myFile.txt')) # Resource reference

def main():
    # Launch primary shell script with options here!

    # Initialize parser
    parser = argparse.ArgumentParser(description="Run the autoEffPop program.")

    # Adding input_species argument
    parser.add_argument('input_species', metavar='N', nargs='+', help='a list of all species being input')

    # Adding Ploidy argument (defaults to 1; haploid)
    # TO BE IMPLEMENTED
    parser.add_argument("-p", "--Ploidy", type=int, choices=[1, 2], help="Show Ploidy", default=1)

    # Output printing option group
    verbosenessGroup = parser.add_mutually_exclusive_group()

    # Adding option to increase verbosity
    # TO BE IMPLEMENTED
    verbosenessGroup.add_argument("-v", "--verbose", action='store_true', help="increase output verbosity")

    # Adding option to decrease verbosity
    # TO BE IMPLEMENTED
    verbosenessGroup.add_argument("-q", "--quiet", action='store_true', help="do not print any output")

    # Adding option to force rerunning BLAST filtering phase
    # TO BE IMPLEMENTED
    parser.add_argument("--forceBLAST", help="Force remaking of BLAST databases during filtering phase, even if prior databases exist")

    # Adding option to include Dendropy results
    # TO BE IMPLEMENTED
    parser.add_argument("--dendropy", help="include Dendropy's pi and theta estimators in results")

    # TODO: Investigate add_subparsers for use in specifying tools in command line rather than main program arguments
    # Adding option to run the results gathering tool
    # TO BE IMPLEMENTED
    parser.add_argument("--toolGatherResults", default="GatheredResults.txt", help="runs the result-gathering helper tool, rather than the main program")

    # Adding option to run the GC_Content gathering tool
    # TO BE IMPLEMENTED
    parser.add_argument("--toolGatherGCs", default="GatheredGC_Content.txt", help="runs the GC-content-gathering helper tool, rather than the main program")

    # Adding option to run the input fetching tool
    # TO BE IMPLEMENTED
    parser.add_argument("--toolFetchInput", nargs=1,
                        help="runs the input fetching helper tool to pull an input species from NCBI's refseq database, rather than the main program")

    # Read arguments from command line
    args = parser.parse_args()

    # TODO: Decide whether to call the main sh file with amendments to handle the above options, or to rewrite the core script within this file.
    scriptCall = 'resources/core_programs/autoEffLaunch.sh '
    for inSpec in args.input_species:
        scriptCall += inSpec + " "
    subprocess.run(['sh', scriptCall])

    print("Find your desired outputs in the final_output folder corresponding to the input species.")
    print("Alternatively, find the output values quickly in the consolidated_output file corresponding to the run date.")


if __name__ == '__main__':
    main()
