#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder=${1}
specLabel="${specFolder##*/}"

# Build Orthogroup files from ungrouped sequence files
mkdir -p muscle_input/${specLabel}
python gatherOrthogroupSequences.py temp/${specLabel}/Nucleotide temp/${specLabel}/Nucleotide/single_copy_og.txt muscle_input/${specLabel}

# Removal of old Nucleotide files once muscle input has already been acquired
rm -rf temp/${specLabel}/Nucleotide/ #Re-enable when done testing!
