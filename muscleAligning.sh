#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder=${1}
specLabel="${specFolder##*/}"

# Run muscle alignment on nucleotide orthogroups
mkdir -p muscle_output/${specLabel}
for filename in muscle_input/${specLabel}/*; do
	titleWithoutFolder="${filename##*/}"
	echo "Aligning ${specLabel} strain ${titleWithoutFolder} in muscle..."
	./muscle3.8.31_i86linux64 -in muscle_input/${specLabel}/${titleWithoutFolder} -fastaout muscle_output/${specLabel}/${titleWithoutFolder} 
done

# Removal of muscle input once muscle output has been acquired
rm -rf muscle_input/${specLabel}/
