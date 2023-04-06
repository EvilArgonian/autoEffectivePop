# file app/__main__.py

import argparse
import subprocess


def main():
    # Launch primary shell script with options here!

    # Initialize parser
    parser = argparse.ArgumentParser(description="Run the autoEffPop program.")

    # Adding input_species argument as
    parser.add_argument('input_species', metavar='N', nargs='+', help='a list of all species being input')

    # Adding Ploidy argument (defaults to 1; haploid)
    # parser.add_argument("-p", "--Ploidy", type=int, choices=[1, 2], help="Show Ploidy", default=1)

    # Read arguments from command line
    args = parser.parse_args()

    scriptCall = 'autoEffLaunch.sh '
    for inSpec in args.input_species:
        scriptCall += inSpec + " "
    subprocess.run(['sh', scriptCall])

    print("Find your desired outputs in the final_output folder corresponding to the input species.")
    print("Alternatively, find the output values quickly in the consolidated_output file corresponding to the run date.")


if __name__ == '__main__':
    main()
