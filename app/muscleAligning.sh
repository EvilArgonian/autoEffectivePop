#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolderTemp=${1}
specLabel="${specFolderTemp##*/}"

# Run muscle alignment on nucleotide orthogroups
mkdir -p ${specFolderTemp}/muscle_output/
for filename in ${specFolderTemp}/muscle_input/*; do
	titleWithoutFolder="${filename##*/}"
	echo "Aligning ${specLabel} strain ${titleWithoutFolder} in muscle..."
	./muscle3.8.31_i86linux64 -in ${specFolderTemp}/muscle_input/${titleWithoutFolder} -fastaout ${specFolderTemp}/muscle_output/${titleWithoutFolder} 
done

# Removal of muscle input once muscle output has been acquired
rm -rf ${specFolderTemp}/muscle_input/
