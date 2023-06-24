#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Moving JC Modified-Processing Input!"

#Establish what species are being processed; $1 and further arguments should be species names matching those used as directory names in the input folder
processInput=()
if [ -z "${1+set}" ]; then 
    for file in $(find ../../jcaraway/collapsed_fastas/ -mindepth 1 -maxdepth 1 -type d); do
		processInput+=($file)
	done
else 
	for arg in "$@"; do
		processInput+=("../../jcaraway/collapsed_fastas/"$arg)
	done
fi

echo "Input Processing: ${processInput[@]}"

outFolder="modifiedAlignmentInput/"

processCount=0
for inputFolder in ${processInput[@]}; do
	{ # Try	
		inputLabel="${inputFolder##*/}"
		
		processCount=$(( ${processCount}+1 ))
		echo "Processing input for Species ${processCount}: ${inputLabel}"
		
		for geneFolder in $(find ${inputFolder}/ -mindepth 1 -maxdepth 1 -type d); do
			echo "Found ${geneFolder}"
			mkdir ${outFolder}/${inputLabel}/
			cp ${geneFolder} ${outFolder}/${inputLabel}/
		done
		
		if [[ -f "${outFolder}/${inputLabel}/ORF1a_collapsed_mutation_fastas.fa" ]]; then #Check if it contains gene ORF1a, which is contained within ORF1ab, and must be processed separately to avoid counting the sites doubly
			mkdir ${outFolder}/${inputLabel}_1a/
			mv ${outFolder}/${inputLabel}/ORF1a_collapsed_mutation_fastas.fa" "${outFolder}/${inputLabel}_1a/
		fi
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${inputFolder##*/}"
	}
done
