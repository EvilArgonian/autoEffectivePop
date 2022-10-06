#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

#Parse input; should be in form 'Genus_species' or an array of such statements
if [ -z "${1+set}" ]; then
    echo "Input not provided!"
else
	a=("$@")
	num_left=${#a[@]}
	echo "${num_left} Inputs"
	for spec in ${a[@]}; do
		python fetchInput.py $spec
		sh ${spec}_fetch.sh
		rm ${spec}_fetch.sh
		
		if [ "$(ls -A input/${spec})" ]; then
			echo "${spec} folder generated in input."
		else
			echo "${spec} did not yield results."
			rmdir input/${spec}
		fi
		
		num_left=$(( num_left-1 ))
		if [[ "${num_left}" == "0" ]]; then
			echo "All done!"
		else
			echo "${num_left} inputs left!"
			sleep 30
		fi
	done
	echo "Done fetching input!"
fi

