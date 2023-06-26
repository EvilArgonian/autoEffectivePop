#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder=${1}
specLabel="${specFolder##*/}"

# Writing boolean logic as arithmetic expressions for ease of use.
true=1
false=0

# Make BLAST databases
shouldSkip=${false}

seenDatabases=("Default")
for filename in ${specFolder}/BLAST/*.ffn.ndb; do
	titleWithoutFolder="${filename##*/}"
	seenDatabases+=("${titleWithoutFolder}");
done

for filename in ${specFolder}/BLAST/*.ffn; do
	titleWithoutFolder="${filename##*/}"
	title="${titleWithoutFolder%%.ffn*}"
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

seen=("Default")
# BLAST each strain against each other
for filename in ${specFolder}/BLAST/*.ffn; do
	titleWithoutFolder="${filename##*/}"
	title="${titleWithoutFolder%%.ffn*}"
	
	for filename2 in ${specFolder}/BLAST/*.ffn; do
		titleWithoutFolder2="${filename2##*/}"
		title2="${titleWithoutFolder2%%.ffn*}"
		if [[ ${title} != ${title2} && ! ${seen[@]} =~ "${title2}" ]]; then
			redundancyCheck1=temp/${specLabel}/BLAST/${title}_vs_${title2}.txt
			redundancyCheck2=temp/${specLabel}/BLAST/${title2}_vs_${title}.txt
			if [[ -f "$redundancyCheck1" || -f "$redundancyCheck2" ]]; then
				echo "BLAST for ${title} and ${title2} already exists."
			else
				echo "BLASTing ${title} against ${title2}"
				./ncbi-blast-2.14.0+/bin/blastn -task megablast -num_threads 4 -db ${filename} -query ${filename2} -outfmt 6 -num_alignments 1 >> temp/${specLabel}/BLAST/${title}_vs_${title2}.txt
			fi
		fi
	done
	seen+=("${title}")
done

echo "Launching full filtering round on all strains:"
# Create distribution of avgIdentities; Analyze for strains that fail statistical tests
finalSurvivingStrains=$(echo $(python filterByIdentity.py ${specLabel} 2))
# Surviving unfiltered strains have been copied to temp/Nucleotide

if (( finalSurvivingStrains == -1)); then
	echo "${specFolder} was entirely filtered away!"
	exit 1
else
	echo "${specFolder} finished filtering with ${finalSurvivingStrains} surviving strains"
fi

