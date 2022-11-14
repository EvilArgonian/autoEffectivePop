#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Launching!"

#Establish what species are being processed; $1 and further arguments should be species names matching those used as directory names in the input folder
processSpecies=()
if [ -z "${1+set}" ]; then 
    for file in $(find input/ -mindepth 1 -maxdepth 1 -type d); do
		processSpecies+=($file)
	done
else 
	for arg in "$@"; do
		processSpecies+=("input/"$arg)
	done
fi

echo "Species Processing: ${processSpecies[@]}"

processCount=0
for specFolder in ${processSpecies[@]}; do
	{ # Try	

		specLabel="${specFolder##*/}"
		
		processCount=$(( ${processCount}+1 ))
		echo "Processing input for Species ${processCount}: ${specLabel}"
		start_time=`date +%s`
		
		sh inputProcessing.sh ${specFolder}
		
		specFolderTemp=temp/${specLabel}
		
		# This line should determine number of strains
		echo "Finding number of strains..."
		strains=$(find ${specFolderTemp}/BLAST/ -mindepth 1 -maxdepth 1 -type f -name '*.ffn' -printf x | wc -c)
		if (( strains > 400 )); then
			echo "High strain count recognized; optimizing for time using blastFilteringLite."
			sh blastFilteringLite.sh ${specFolderTemp}
		elif (( strains < 3 )); then
			echo "Low strain count recognized; no calculations to perform."
			continue
		else
			echo "Normal blast filtering beginning."
			sh blastFiltering.sh ${specFolderTemp}
		fi
		
		
		end_time=`date +%s`
		runtime=$((end_time-start_time))
		finished=`date +"%Y-%m-%d %T"`
		echo -e "${specLabel} Process Time (Filter-Only run): ${runtime} seconds\tFinished: ${finished}"
	
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${specFolder##*/}"
	}
done
	
