#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

category=${1} # The name of the category being processed, as it appears in categories directory
repeatRuns=${2} # The amount of repeat runs to perform, of which the genes that are selected in each of these runs will be considered valid
matchE_Threshold=${3} # During BLAST evaluations, the e_val threshold that must be beaten (lower is more matching) to count as a match and thus keep the gene in the core set. A decimal between 0 and 1, such as '0.1'

echo "Launching Core Gene Finding for ${category}!"
catSpecies=()
for specFile in $(find categories/${category} -mindepth 1 -maxdepth 1 -type d); do
		specFileWithoutFolder="${specFile##*/}"
		spec="${specFileWithoutFolder%%.txt*}"
		catSpecies+=(${spec})
	done
catSize=${#catSpecies[@]}
randomSize=$(( ${catSize} * 9 / 10)) # 90% of initial size, rounded down
echo "${catSize} species in the category; random ${randomSize} in each run."
echo "Preparing BLAST databases for whole category."
# Determine what databases already exist (NOTE: All databases are stored in the 'All' category, not other categories, to remove redundancy
seenDatabases=("Default")
for spec in ${catSpecies[@]}; do
	if [[ -f categories/All/${spec}/${spec}.ndb ]]; then
		seenDatabases+=("${spec}");
	fi
done

# Create any other databases 
for spec in ${catSpecies[@]}; do
	if [[ ! ${seenDatabases[@]} =~ "${spec}" ]]; then
		echo "Making database for ${spec}"
		../ncbi-blast-2.14.0+/bin/makeblastdb -in categories/${category}/${spec}/${spec}.txt -out categories/All/${spec}/${spec} -dbtype nucl
	else
		echo "Database for ${spec} already exists."
	fi
done

rm -rf core_genes/${category}/
mkdir core_genes/${category}/
for (( runNum=1; runNum<=${repeatRuns}; runNum++ )); do
	echo "Launching run ${runNum} out of ${repeatRuns}!"
	mkdir core_genes/${category}/Run_${runNum}
	
	randomSet=()
	indexLimit=$(( ${#catSpecies[@]} - 1 ))
	for randomIndex in $(shuf -i 0-${indexLimit} -n ${randomSize}); do
		randomSet+=(${catSpecies[${randomIndex}]})
	done
	if [ ${#randomSet[@]} -eq 0 ]; then
		echo "Random Set acquisition failed!"
	fi
	
	echo ${randomSet[@]} > core_genes/${category}/Run_${runNum}/randomSpecies.txt

	# Acquire the initial list of genes from first species, which will be filtered down with each comparison to other species without a sufficient match
	# Note that these genes don't yet have real names; they are labeled arbitrarily
	python initialGeneSetup.py ${category} ${randomSet[0]} ${runNum}
	
	blastOutFolder="core_genes/${category}/Run_${runNum}/BLASTs/"
	failOutFolder="core_genes/${category}/Run_${runNum}/Fails/"
	rm -rf ${blastOutFolder}
	rm -rf ${failOutFolder}
	mkdir ${blastOutFolder}
	mkdir ${failOutFolder}
	
	remainingGenes=()
	for geneFile in $(find core_genes/${category}/Run_${runNum}/Genes/ -mindepth 1 -maxdepth 1 -type f); do # Move non-arbitrary naming to end of a run
		geneFileWithoutFolder="${geneFile##*/}"
		arbitraryGene="${geneFileWithoutFolder%%.txt*}"
		blastOutFile=${blastOutFolder}/Rename_${arbitraryGene}.txt
		{ #Try
			../ncbi-blast-2.14.0+/bin/blastx -query ${geneFile} -db "/home/blastdb/nr" -num_alignments 1 >>  ${blastOutFile}
			# What frequency of attempts to query NCBI is appropriate?
			gene=$(echo $(python establishGeneName.py ${geneFile} ${blastOutFile}))
			remainingGenes+=(${gene})
		} || { # Catch
			remainingGenes+=(${arbitraryGene})
			echo "Gene renaming of ${geneFile} failed. "
		}
	done
	
	# For each other species...
	for (( speciesIndex=1; speciesIndex<=$((randomSize-1)); speciesIndex++ )); do
		species=(${randomSet[${speciesIndex}]})
		database="categories/All/${species}/${species}"
		# For each remaining Gene...
		passedGenes=()
		for gene in ${remainingGenes[@]}; do
			geneFile=core_genes/${category}/Run_${runNum}/Genes/${gene}
			blastOutFile=${blastOutFolder}/${gene}_vs_${species}.txt
			# echo "BLASTing ${geneFile} against ${species} database"
			../ncbi-blast-2.14.0+/bin/tblastx -num_threads 4 -db ${database} -query ${geneFile} -outfmt 6 -num_alignments 1 >> ${blastOutFile} 2>/dev/null
			passFlag=$(echo $(python passGene.py ${geneFile} ${blastOutFile} ${matchE_Threshold}))
			if [[ ${passFlag}=="Passed!" ]]; then
				passedGenes+=(${gene})
			else
				cp ${geneFile} ${failOutFolder}
				echo "${gene} ${passFlag}"
			fi
		done
		remainingGenes=${passedGenes}
		if [ ${#remainingGenes[@]} -eq 0 ]; then
			break
		fi
	done
	if [ ${#remainingGenes[@]} -eq 0 ]; then
		echo "No core genes survived!"
	else
		echo "${#remainingGenes[@]} survived."
		printf '%s\n' "${passedGenes[@]}" > core_genes/${category}/Run_${runNum}/Passed_Genes.txt
	fi
done

# Run Comparison
python findSharedCoreGenes.py ${category} core_genes/${category}/Core_Genes.txt
