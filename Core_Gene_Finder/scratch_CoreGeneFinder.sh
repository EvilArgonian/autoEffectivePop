#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

category=${1} # The name of the category being processed, as it appears in categories directory
repeatRuns=${2} # The amount of repeat runs to perform, of which the genes that are selected in each of these runs will be considered valid
matchThreshold=${3} # During BLAST evaluations, the similarity threshold that must be beaten to count as a match and thus keep the gene in the core set. A decimal between 0 and 1, such as '0.9'


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
	outFolder = "categories/${category}/${speciesA}/BLAST/"
	rm -rf ${outFolder} # Clear prior BLAST output
	for seqFile in $(find categories/All/${speciesA}/Individual_Seqs -mindepth 1 -maxdepth 1 -type f); do
		seqFileWithoutFolder="${seqFile##*/}"
		consensusSeq="${seqFileWithoutFolder%%.txt*}"
		for indexB in {$((indexA+1))..$((randomSize-1))}; do
			speciesB=(${randomSet[${indexB}]})
			databaseB = "categories/All/${speciesB}/${speciesB}"
			./ncbi-blast-2.10.1+/bin/blastx -task megablast -num_threads 4 -db ${databaseB} -query ${seqFile} -outfmt 6 -num_alignments 1 >> ${outFolder}/${speciesA}_consensusSeq_vs_${speciesB}.txt
		done
	done
done
#BLAST results are now in category-specific folders, because although individual BLAST results should be identical at the seq_vs_species level, the amount and combinations of such files varies by category 

# Acquire the initial list of genes from first species, which will be filtered down with each comparison to other species without a sufficient match
# Note that these genes don't yet have names; they will be labeled
remainingGenes=()
for seqFile in $(find categories/All/${randomSet[0]}/Individual_Seqs -mindepth 1 -maxdepth 1 -type f); do
	seqFileWithoutFolder="${seqFile##*/}"
	consensusSeq="${seqFileWithoutFolder%%.txt*}"
	remainingGenes+=${consensusSeq}
done