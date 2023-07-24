#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder=${1}
keepOldData=${2}
specLabel="${specFolder##*/}"

# Run muscle alignment on nucleotide orthogroups
mkdir -p ${specFolder}/muscle_output/
for filename in ${specFolder}/muscle_input/*; do
	titleWithoutFolder="${filename##*/}"
	echo "Aligning ${specLabel} strain ${titleWithoutFolder} in muscle..."
	./muscle3.8.31_i86linux64 -in ${specFolder}/muscle_input/${titleWithoutFolder} -fastaout ${specFolder}/muscle_output/${titleWithoutFolder} 
done

# Removal of muscle input once muscle output has been acquired
if ! (( keepOldData )); then
	rm -rf ${specFolder}/muscle_input/
fi
