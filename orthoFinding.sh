#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder=${1}
specLabel="${specFolder##*/}"

resultsFolder=$(echo $(python getResultsFolder.py temp/${specLabel}/Nucleotide))

# Index for later grouping step, and rename with a fasta extension Orthofinder recognizes
# Determine if this will need to be changed back (probably?)
for filename in $(find temp/${specLabel}/Nucleotide -mindepth 1 -maxdepth 1 -type f -name '*.ffn'); do
	titleWithoutFolder="${filename##*/}"
	title="${titleWithoutFolder%%.ffn*}"
	python index.py ${filename} temp/${specLabel}/Nucleotide/${title}_index.txt temp/${specLabel}/Error/${title}.txt
	mv ${filename} temp/${specLabel}/Nucleotide/${title}.fa
done

rm -rf ${resultsFolder}
# Run Orthofinder on protein data
./OrthoFinder/orthofinder -f temp/${specLabel}/Nucleotide -og -d -S blast_nucl -A muscle -M msa
mv ${resultsFolder} temp/${specLabel}/Nucleotide/OrthoFinder/Results
resultsFolder="temp/${specLabel}/Nucleotide/OrthoFinder/Results"

# Interpret non-paralogous (single-copy) orthogroups from Orthofinder results
python gatherSingleCopyOrthogroups.py ${resultsFolder} temp/${specLabel}/Nucleotide/single_copy_og.txt

# Removal of orthofinder files once completed
 rm -rf temp/${specLabel}/Nucleotide/Orthofinder #Re-enable after testing! 
