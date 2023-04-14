#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

#Parse input; should be in form 'Genus_species' or an array of such statements
if [ -z "${1+set}" ]; then
    echo "Input not provided!"
else
	a=("$@")
	count=1
	echo "Input ${count}"
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
		
		count=$(( count+1 ))
		sleep 5
	done
	echo "Done fetching input!"
fi

