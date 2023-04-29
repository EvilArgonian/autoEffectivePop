#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

category=${1} # The name of the category being processed, as it appears in consensus_input
repeatRuns=${2} # The amount of repeat runs to perform, of which the genes that are selected in each of these runs will be considered valid


echo "Launching Core Gene Finding for ${category}!"

catSpecies=()
for file in $(find consensus_input/${category} -mindepth 1 -maxdepth 1 -type d); do
	catSpecies+=(${file})
done

catSize=${#catSpecies[@]}
randomSize = $((catSize * (9/10))) # 90% of initial size, rounded down
randomSet = ()

for randomIndex in $(shuf --input-range=0-$(( ${#catSpecies[*]} - 1 )) -n ${randomSize}); do
	randomSet+=(${catSpecies[${randomIndex}]})
done

# Determine what databases already exist
seenDatabases=("Default")
for filename in consensus_input/${category}/*.ndb; do
	titleWithoutFolder="${filename##*/}"
	seenDatabases+=("${titleWithoutFolder}");
done

# Create any other databases 
for spec in ${randomSet[@]}; do
	if [[ ! ${seenDatabases[@]} =~ "${title}.ffn.ndb" ]]; then
		echo "Making database for ${titleWithoutFolder}"
		../ncbi-blast-2.10.1+/bin/makeblastdb -in consensus_input/${category}/${spec}/${spec}.txt -out ${spec}/ -dbtype nucl
	else
		echo "Database for ${titleWithoutFolder} already exists."
	fi
	../ncbi-blast-2.10.1+/bin/makeblastdb -in consensus_input/${category}/${spec}/${spec}.txt -out ${spec}/ -dbtype nucl
done

for indexA in {0..$((randomSize-1))}; do 
	speciesA=(${randomSet[${indexA}]})
	for indexB in {$((indexA+1))..$((randomSize-1))}; do
		speciesB=(${randomSet[${indexB}]})
	done
done