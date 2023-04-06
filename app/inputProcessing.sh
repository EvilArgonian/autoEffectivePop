#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Writing boolean logic as arithmetic expressions for ease of use.
true=1
false=0


specFolder=${1}
specLabel="${specFolder##*/}"
specFolderTemp="../temp/"${specLabel}
specFolderFinal="../final_output/"${specLabel}

strainCount=0
for strainFolder in $(find ${specFolder} -mindepth 1 -maxdepth 1 -type d); do
	strainCount=$(( ${strainCount}+1 ))
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
			mv -f ${strainFolder}/${title}.fna ${strainFolder}/${title}.ffn # Marking as ffn for later processing. Does this break anything? Doesn't seem to.
			rm ${filename}
		fi
	done
	for filename in ${strainFolder}/*.gbff.gz; do
		if [[ -f ${filename} ]]; then
			rm ${filename} # Eliminates unneeded file.
		fi
	done
	
	# Count number of ffn files
	
done

rm -rf ${specFolderTemp}/Nucleotide
rm -rf ${specFolderTemp}/Error
# rm -rf ${specFolderTemp}/BLAST # Do not remove BLAST folder, to save time on future runs
rm -rf ${specFolderTemp}/Filtered
rm -rf ${specFolderTemp}/muscle_input/
rm -rf ${specFolderTemp}/muscle_output/
rm -rf ${specFolderFinal}

mkdir -p ${specFolderTemp}/Nucleotide
mkdir -p ${specFolderTemp}/Error
mkdir -p ${specFolderTemp}/BLAST
mkdir -p ${specFolderTemp}/Filtered

if (( strainCount < 2 )); then
	echo "Skipped ${specFolder}, as it had less than 2 strains. Strain count: ${strainCount}"
	continue
fi

changeFlag=${true}
echo "Testing if strains are identical in saved BLAST and in current input for ${specFolder}"
if [[ -d "${specFolderTemp}/BLAST/" ]]; then # If BLAST directory exists (should always be true, as it is created above)...
	if [ "$(ls -A ${specFolderTemp}/BLAST/)" ]; then # If BLAST directory is not empty...
		# Perform test of identical strains
		changeFlag=${false}
		savedStrains=("Default")
		for strainFolder in $(find ${specFolderTemp}/BLAST/*.ffn); do
			strainLabel="${strainFolder##*/}"
			savedStrains+=("${strainLabel}")
		done

		accountedStrains=("Default")
		for strainFolder in $(find ${specFolder} -mindepth 1 -maxdepth 1 -type d); do
			strainLabel="${strainFolder##*/}"
			strainLabel="${strainLabel%%.C*}" # This is for handling Winzipped compressed archives in the form C01, C02, etc
			strainLabel="${strainLabel%%.N*}" # This is for handling NEKO files in the form .N # Just dump instead
			if [[ ! ${savedStrains[@]} =~ "${strainLabel}" ]]; then #Check if all our strains can be found in the saved BLAST strains
				changeFlag=${true}
				break;
			else
				accountedStrains+=("${strainLabel}")
			fi
		done

		for savedStrain in ${savedStrains}; do
			if [[ ! ${accountedStrains[@]} =~ "${savedStrain}" ]]; then # Check if all saved BLAST strains can be found in our strains
				changeFlag=${true}
				break;
			fi
		done
	fi
fi

if (( changeFlag )); then # Only update BLAST folder if there was a change
	rm -rf ${specFolderTemp}/BLAST
	mkdir -p ${specFolderTemp}/BLAST
	# Combine nucleotide files of a strain for single title, move to temp
	for strainFolder in $(find ${specFolder} -mindepth 1 -maxdepth 1 -type d); do
		strainLabel="${strainFolder##*/}"
		strainLabel="${strainLabel%%.C*}" # This is for handling Winzipped compressed archives in the form C01, C02, etc
		strainLabel="${strainLabel%%.N*}" # This is for handling NEKO files in the form .N # Just dump instead
		countFFNs=0
		for filename in ${strainFolder}/*.ffn; do
			if [[ -f ${filename} ]]; then
				cat ${filename} >> temp/${specLabel}/BLAST/${strainLabel}.ffn
				countFFNs=$(( ${countFFNs}+1 ))
			fi
		done
		if (( countFFNs > 1 )); then
			echo "Forwarded ${strainLabel} to BLAST step. Combined ${countFFNs} .ffn files."
		else
			echo "Forwarded ${strainLabel} to BLAST step."
		fi
	done
fi

