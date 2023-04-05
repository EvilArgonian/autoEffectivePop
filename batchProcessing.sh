#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Determining all species to run."

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

countRuns=0
countFails=0
for specFolder in ${processSpecies[@]}; do
	countRuns=$(( ${countRuns}+1 ))
	echo "Species ${countRuns}: ${specFolder} running..."
	sh autoEffLaunch.sh ${specFolder##*/} || ( echo "${specFolder##*/} failed to process." && countFails=$(( ${countFails}+1 )) )
done

echo "Completed with ${countFails} failures."
