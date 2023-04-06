#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolderTemp=${1}
specLabel="${specFolderTemp##*/}"

# Writing boolean logic as arithmetic expressions for ease of use.
true=1
false=0

# Make BLAST databases
shouldSkip=${false}

seenDatabases=("Default")
for filename in ${specFolderTemp}/BLAST/*.ffn.ndb; do
	titleWithoutFolder="${filename##*/}"
	seenDatabases+=("${titleWithoutFolder}");
done

strains=()
for filename in ${specFolderTemp}/BLAST/*.ffn; do
	titleWithoutFolder="${filename##*/}"
	title="${titleWithoutFolder%%.ffn*}"
	strains+=("${title}")
	if [[ ${title} == "*" ]]; then
		echo "No strains to BLAST for ${specLabel}"
		shouldSkip=${true}
		continue
	fi
	if [[ ! ${seenDatabases[@]} =~ "${title}.ffn.ndb" ]]; then
		echo "Making database for ${titleWithoutFolder}"
		./ncbi-blast-2.10.1+/bin/makeblastdb -in ${filename} -dbtype nucl
	else
		echo "Database for ${titleWithoutFolder} already exists."
	fi
done

if (( shouldSkip )); then
	echo "Did not process ${specLabel}, as there were no strains to BLAST."
	exit 1
fi

touch ${specFolderTemp}/Filtered/Removal_Log.txt
touch ${specFolderTemp}/Filtered/Filtration_Log_Lite.txt
touch ${specFolderTemp}/Filtered/Statistics_Lite.txt
touch ${specFolderTemp}/Filtered/RemovalForSimilarity_Lite.txt
touch ${specFolderTemp}/Filtered/RemovalForDissimilarity_Lite.txt

skipFiltering=${false}; # Flag included for testing purposes. Change to true to skip filtering steps entirely.

# BLAST each strain against each other
elemsUnseen="${#strains[@]}"
echo "Initial number of strains to handle: ${elemsUnseen}"
loopCount=0
seen=("Default")
while (( elemsUnseen > 0 )); do
	if (( skipFiltering )); then
		break
	fi 
	if ((loopCount >= ${#strains[@]})); then
		break
	fi
	filename=${specFolderTemp}/BLAST/${strains[${loopCount}]}.ffn
	titleWithoutFolder="${filename##*/}"
	title="${titleWithoutFolder%%.ffn*}"
	
	echo "${title} outer loop ${loopCount}..."
	for strain in "${strains[@]}"; do
		filename2="${specFolderTemp}/BLAST/${strain}.ffn"
		titleWithoutFolder2="${filename2##*/}"
		title2="${titleWithoutFolder2%%.ffn*}"
		if [[ ${title} != ${title2} && ! ${seen[@]} =~ "${title2}" ]]; then
			redundancyCheck1=${specFolderTemp}/BLAST/${title}_vs_${title2}.txt
			redundancyCheck2=${specFolderTemp}/BLAST/${title2}_vs_${title}.txt
			if [[ -f "$redundancyCheck1" || -f "$redundancyCheck2" ]]; then
				echo "BLAST for ${title} and ${title2} already exists."
			else
				echo "BLASTing ${title} against ${title2}"
				./ncbi-blast-2.10.1+/bin/blastn -task megablast -num_threads 4 -db ${filename} -query ${filename2} -outfmt 6 -num_alignments 1 >> ${specFolderTemp}/BLAST/${title}_vs_${title2}.txt
			fi
		fi
	done
	strains=()
	elemsUnseen=0
	seen+=("${title}")
	python filterByIdentityLite.py ${specLabel} ${title} "2" ".995"
	# IFS=$','
	readarray -d ',' -t remStrains < "${specFolderTemp}/Filtered/Output.txt"
	echo "Remaining strains: ${remStrains[@]}"
	for strain in ${remStrains[@]}; do
		strains+=("${strain}")
		if [[ " ${seen[@]} " =~ " ${strain} " ]]; then
			echo "${strain} seen already..."
			continue
		else
			elemsUnseen=$((elemsUnseen + 1))
			echo "${strain} not seen... (${elemsUnseen} total)"
		fi
	done
	loopCount=$((loopCount + 1))
	echo "Loop ${loopCount} unfiltered strains remaining unseen: ${elemsUnseen}"
done

#Regular filtration of remaining strains #Now only performed if less than 400 strains remain
numRemainingStrains=${#remStrains[@]}
if (( numRemainingStrains < 400 )); then
	mkdir ${specFolderTemp}/Filtered/Lite/

	#Push filtered strains out of the way

	echo "Setting aside filtered strains."
	for filename in ${specFolderTemp}/BLAST/*.ffn; do
		titleWithoutFolder="${filename##*/}"
		title="${titleWithoutFolder%%.ffn*}"
		if ! [[ " ${remStrains[@]} " =~ " ${title} " ]]; then
			mv ${filename} ${specFolderTemp}/Filtered/Lite/
			echo "${filename} moved."
		fi
	done

	echo "Setting aside filtered BLAST comparisons."
	for filename in ${specFolderTemp}/BLAST/*_vs_*.txt; do
		titleWithoutFolder="${filename##*/}"
		titleVs="${titleWithoutFolder%%.txt*}"
		title="${titleVs%%_vs_*}"
		title2="${titleVs##*_vs_}"
		if ! [[ " ${remStrains[@]} " =~ " ${title} " ]]; then
			if ! [[ " ${remStrains[@]} " =~ " ${title2} " ]]; then
				mv ${filename} ${specFolderTemp}/Filtered/Lite/
				echo "${filename} moved."
			fi
		fi
	done

	#BLAST each remaining strain against each other if needed
	echo "Remaining BLAST rounds:"
	for filename in ${specFolderTemp}/BLAST/*.ffn; do
		titleWithoutFolder="${filename##*/}"
		title="${titleWithoutFolder%%.ffn*}"
		if (( skipFiltering )); then
			cp ${filename} ${specFolderTemp}/Nucleotide/${titleWithoutFolder}
			continue
		else
			for filename2 in ${specFolderTemp}/BLAST/*.ffn; do
				titleWithoutFolder2="${filename2##*/}"
				title2="${titleWithoutFolder2%%.ffn*}"
				echo "Title: ${title} - Title 2: ${title2}"
				if [[ ${title} != ${title2} && ! ${seen[@]} =~ "${title}" && ! ${seen[@]} =~ "${title2}" ]]; then
					echo "BLASTing ${title} against ${title2}"
					./ncbi-blast-2.10.1+/bin/blastn -task megablast -num_threads 4 -db ${filename} -query ${filename2} -outfmt 6 -num_alignments 1 >> ${specFolderTemp}/BLAST/${title}_vs_${title2}.txt
				fi
			done
			seen+=("${title}")
		fi
	done
	echo "Blast comparisons in total: $(find ${specFolderTemp}/BLAST/ -name "*_vs_*.txt" -printf '.' | wc -m)"

	echo "Launching full filtering round on remaining strains:"
	# Create distribution of avgIdentities; Analyze for strains that fail statistical tests
	finalSurvivingStrains=$(echo $(python filterByIdentity.py ${specLabel} .9999))
	# Surviving unfiltered strains have been copied to temp/Nucleotide

	if (( finalSurvivingStrains == -1)); then
		echo "${specFolderTemp} was entirely filtered away!"
		exit 1
	else
		echo "${specFolderTemp} finished filtering with ${finalSurvivingStrains} surviving strains"
	fi
else
	echo "Moving less-rigorously filtered 400+ strains to temp/Nucleotide"
	for filename in ${specFolderTemp}/BLAST/*.ffn; do
		titleWithoutFolder="${filename##*/}"
		title="${titleWithoutFolder%%.ffn*}"
		cp ${filename} ${specFolderTemp}/Nucleotide/${titleWithoutFolder}
	done
fi

