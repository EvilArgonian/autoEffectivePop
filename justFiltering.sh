#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Assumptions:
# Inputs are in the form of ffn, ffa, or tgz files.
# Titles of species folders in input should match the names used in mutation_rates.txt

echo "Begin!"

#Establish what species are being processed; $1 should be a folder directory in the form of 'input/species' if provided
processSpecies=()
if [ -z "${1+set}" ]; then 
    for file in $(find input/ -mindepth 1 -maxdepth 1 -type d); do
		processSpecies+=($file)
	done
else 
	for arg in "$@"; do
		if [[ "${arg}" =~ ^"input/*" ]]; then
			processSpecies+=("input/"$arg) # Assumes that anything not beginning with the input/ folder was just a species name
		else
			processSpecies+=($arg)
		fi
	done
fi

echo "Processing: ${processSpecies[@]}"

newToProcess=()
oldToRemoveFromProcess=()

currentDirectory=()
for entry in $(find input/ -mindepth 1); do
	currentDirectory+=(${entry})
done
readarray -t alreadyProcessed < input/AlreadyProcessed.txt

for entry in ${currentDirectory[@]}; do # For entries added since last save of already processed entries
	IFS=/
	read -a entryParts <<< ${entry}
	entrySpecLevel="${entryParts[0]}/${entryParts[1]}"
	IFS=$'\n\t'
	if [[ ! ${alreadyProcessed[@]} =~ ${entry} && ${processSpecies[@]} =~ ${entrySpecLevel} ]]; then
		newToProcess+=(${entry})
	fi
done

for entry in ${alreadyProcessed[@]}; do # For entries removed since last save of already processed entries
	IFS=/
	read -a entryParts <<< ${entry}
	entrySpecLevel="${entryParts[0]}/${entryParts[1]}"
	IFS=$'\n\t'
	if [[ ! ${currentDirectory[@]} =~ ${entry} && ${processSpecies[@]} =~ ${entrySpecLevel} ]]; then
		oldToRemoveFromProcess+=(${entry})
	fi
done

truncate -s 0 input/AlreadyProcessed.txt
for item in ${currentDirectory[@]}; do
	echo ${item} >> input/AlreadyProcessed.txt
done

# Writing boolean logic as arithmetic expressions for ease of use.
true=1
false=0


# Unpack .tgz files and .fna.gz files
for specFolder in ${processSpecies[@]}; do
	specLabel="${specFolder##*/}"
	
	echo "Checking ${specLabel}"
	
	shouldSkip=${true}
	for item in ${newToProcess[@]}; do
		echo "Comparing ${item} ----> ${specFolder}"
		if [[ ${item} =~ .*"${specLabel}".* ]]; then
			shouldSkip=${false}
			echo "Processing ${specLabel}..."
			break
		fi
	done
	if (( shouldSkip )); then
		for item in ${oldToRemoveFromProcess[@]}; do
			if [[ ${item} =~ .*"${specLabel}".* ]]; then
				shouldSkip=${false}
				echo "Processing ${specLabel}..."
				break
			fi
		done
	fi
	if (( shouldSkip )); then
		echo "Did not process ${specLabel}, as it was unchanged from last run."
		continue
	fi
	
	for strainFolder in $(find ${specFolder} -mindepth 1 -maxdepth 1 -type d); do
		for filename in ${strainFolder}/*.tgz; do
			if [[ -f ${filename} ]]; then
				titleWithoutFolder="${filename##*/}"
				tar zxpf ${filename} -C ${strainFolder}
				rm ${filename}
			fi
		done
		for filename in ${strainFolder}/*.fna.gz; do
			if [[ -f ${filename} ]]; then
				titleWithoutFolder="${filename##*/}"
				title="${titleWithoutFolder%%.fna.gz*}"
				gunzip -c ${filename} > ${strainFolder}/${title}.fna
				mv ${strainFolder}/${title}.fna ${strainFolder}/${title}.ffn # Marking as ffn for later processing. Does this break anything?
			fi
		done
	done
	
	strainArray=$(find ${specFolder} -mindepth 1 -maxdepth 1 -type d)
	if [[ ! -v ${strainArray[@]} ]]; then
	echo "Skipped ${specFolder}, as it had less than 2 strains."
		continue
	fi
	if [ ${#strainArray[@]} -lt 2 ]; then
	echo "Skipped ${specFolder}, as it had less than 2 strains."
		continue
	fi
	
	rm -rf temp/${specLabel}/
	mkdir -p temp/${specLabel}/Nucleotide
	mkdir -p temp/${specLabel}/Protein
	mkdir -p temp/${specLabel}/Error
	mkdir -p temp/${specLabel}/BLAST
	mkdir -p temp/${specLabel}/Filtered
	
	
	
	# Combine nucleotide files of a strain for single title, move to temp
	for strainFolder in $(find ${specFolder} -mindepth 1 -maxdepth 1 -type d); do
		strainLabel="${strainFolder##*/}"
		countSeq=0
		for filename in ${strainFolder}/*.ffn; do # Do .ffa's as well
			if [[ -f ${filename} ]]; then
				cat ${filename} >> temp/${specLabel}/BLAST/${strainLabel}.ffn
				countSeq=$(( ${countSeq}+1 ))
			fi
		done
		echo "Completed agglomerating sequences of ${strainLabel}: ${countSeq} sequences."
	done
done

for specFolder in $(find temp/ -mindepth 1 -maxdepth 1 -type d); do # specFolder resembles temp/<specLabel>
	specLabel="${specFolder##*/}"
	if [[ ! " ${processSpecies[@]} " =~ " input/${specLabel} " ]]; then
		continue
	fi
	shouldSkip=${true}
	for item in ${newToProcess[@]}; do
		echo "Comparing ${item} ----> ${specFolder}"
		if [[ ${item} =~ .*"${specLabel}".* ]]; then
			shouldSkip=${false}
			echo "Processing ${specLabel}..."
			break
		fi
	done
	if (( shouldSkip )); then
		for item in ${oldToRemoveFromProcess[@]}; do
			if [[ ${item} =~ .*"${specLabel}".* ]]; then
				shouldSkip=${false}
				echo "Processing ${specLabel}..."
				break
			fi
		done
	fi
	if (( shouldSkip )); then
		echo "Did not process ${specLabel}, as it was unchanged from last run."
		continue
	fi
	
	# Make BLAST databases
	for filename in ${specFolder}/BLAST/*.ffn; do
		#titleWithoutFolder="${filename##*/}"
		#title="${titleWithoutFolder%%.ffn*}"
		./ncbi-blast-2.10.1+/bin/makeblastdb -in ${filename} -dbtype nucl
	done
	
	# BLAST each strain against each other
	seen=("Default")
	for filename in ${specFolder}/BLAST/*.ffn; do
		titleWithoutFolder="${filename##*/}"
		title="${titleWithoutFolder%%.ffn*}"
		for filename2 in ${specFolder}/BLAST/*.ffn; do
			titleWithoutFolder2="${filename2##*/}"
			title2="${titleWithoutFolder2%%.ffn*}"
			if [[ ${title} != ${title2} && ! ${seen[@]} =~ "${title2}" ]]; then
				echo "BLASTing ${title} against ${title2}"
				./ncbi-blast-2.10.1+/bin/blastn -task megablast -num_threads 4 -db ${filename} -query ${filename2} -outfmt 6 -num_alignments 1 >> temp/${specLabel}/BLAST/${title}_vs_${title2}.txt
			fi
		done
		seen+=("${title}")
	done
	
	# Create distribution of avgIdentities; Analyze for strains that fall outside the confidence interval
	# NOTE: Moving of files from temp/<specLabel>/BLAST to temp/<specLabel>/Nucleotide should occur in filterByIdentity, not here
	speciesEntirelyFiltered=$(echo $(python filterByIdentity.py ${specLabel} .9999))
	
	if (( speciesEntirelyFiltered )); then
		echo "${specFolder} was entirely filtered away!"
		continue # Skips to next specFolder
	fi
done

