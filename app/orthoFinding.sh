#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolderTemp=${1}
specLabel="${specFolderTemp##*/}"

resultsFolder=$(echo $(python getResultsFolder.py ${specFolderTemp}/Nucleotide))

# Index for later grouping step, and rename with a fasta extension Orthofinder recognizes
# Determine if this will need to be changed back (probably?)
for filename in $(find ${specFolderTemp}/Nucleotide -mindepth 1 -maxdepth 1 -type f -name '*.ffn'); do
	titleWithoutFolder="${filename##*/}"
	title="${titleWithoutFolder%%.ffn*}"
	python index.py ${filename} ${specFolderTemp}/Nucleotide/${title}_index.txt ${specFolderTemp}/Error/${title}.txt
	mv ${filename} ${specFolderTemp}/Nucleotide/${title}.fa
done

rm -rf ${resultsFolder}
# Run Orthofinder on protein data
./OrthoFinder/orthofinder -f ${specFolderTemp}/Nucleotide -og -d -S blast_nucl -A muscle -M msa
mv ${resultsFolder} ${specFolderTemp}/Nucleotide/OrthoFinder/Results
resultsFolder="${specFolderTemp}/Nucleotide/OrthoFinder/Results"

# Interpret non-paralogous (single-copy) orthogroups from Orthofinder results
python gatherSingleCopyOrthogroups.py ${resultsFolder} ${specFolderTemp}/Nucleotide/single_copy_og.txt

# Removal of orthofinder files once completed
rm -rf ${specFolderTemp}/Nucleotide/Orthofinder

# Build Orthogroup files from ungrouped sequence files
mkdir -p ${specFolderTemp}/muscle_input/
python gatherOrthogroupSequences.py ${specFolderTemp}/Nucleotide ${specFolderTemp}/Nucleotide/single_copy_og.txt ${specFolderTemp}/muscle_input/

# Removal of old Nucleotide files once muscle input has already been acquired
rm -rf ${specFolderTemp}/Nucleotide/ 
