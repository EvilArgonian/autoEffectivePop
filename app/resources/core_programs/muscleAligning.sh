#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder=${1}
specLabel="${specFolder##*/}"
temp="../../../temp"

# Run muscle alignment on nucleotide orthogroups
mkdir -p ${temp}/${specLabel}/muscle_output/${specLabel}
for filename in ${temp}/${specLabel}/muscle_input/*; do
	titleWithoutFolder="${filename##*/}"
	echo "Aligning ${specLabel} strain ${titleWithoutFolder} in muscle..."
	./muscle3.8.31_i86linux64 -in ${temp}/${specLabel}/muscle_input/${titleWithoutFolder} -fastaout ${temp}/${specLabel}/muscle_output/${titleWithoutFolder} 
done

# Removal of muscle input once muscle output has been acquired
rm -rf ${temp}/${specLabel}/muscle_input/
