#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

category=${1} # The name of the category being processed, as it appears in categories directory
repeatRuns=${2} # The amount of repeat runs to perform, of which the genes that are selected in each of these runs will be considered valid


echo "Launching Core Gene Finding for ${category}!"

catSpecies=()
for specFile in $(find categories/${category} -mindepth 1 -maxdepth 1 -type d); do
	specFileWithoutFolder="${specFile##*/}"
	spec="${specFileWithoutFolder%%.txt*}"
	catSpecies+=(${spec})
done

catSize=${#catSpecies[@]}
randomSize = $((catSize * (9/10))) # 90% of initial size, rounded down
randomSet = ()

for randomIndex in $(shuf --input-range=0-$(( ${#catSpecies[*]} - 1 )) -n ${randomSize}); do
	randomSet+=(${catSpecies[${randomIndex}]})
done

# Determine what databases already exist (NOTE: All databases are stored in the 'All' category, not other categories, to remove redundancy
seenDatabases=("Default")
for spec in ${randomSet[@]}; do
	if [[ -f category/All/${spec}/${spec}.ndb ]]; then
		seenDatabases+=("${spec}");
	fi
done

# Create any other databases 
for spec in ${randomSet[@]}; do
	if [[ ! ${seenDatabases[@]} =~ "${spec}" ]]; then
		echo "Making database for ${spec}"
		../ncbi-blast-2.10.1+/bin/makeblastdb -in categories/${category}/${spec}/${spec}.txt -out categories/All/${spec}/${spec} -dbtype nucl
		python splitConsensus.py ${spec}
	else
		echo "Database for ${spec} already exists."
	fi
done

for indexA in {0..$((randomSize-1))}; do 
	speciesA=(${randomSet[${indexA}]})
	for indexB in {$((indexA+1))..$((randomSize-1))}; do
		speciesB=(${randomSet[${indexB}]})
	done
done