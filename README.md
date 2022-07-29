# autoEffectivePop
This is a pipeline for calculating effective population size (and relevant statistics such as Watterson's theta) for bacterial species.

This pipeline uses the following other programs:
- NCBI's BLAST
- Orthofinder
- MUSCLE
- Dendropy

- - - -

### Input: 
- An input species will include ffn files for the genomes of all strains of that species to be calculated.
- A value for the mutation rate of the species, listed in the 'mutation_rates.txt' file. Can be omitted, in which case effective population size is not determined, though relevant statistics are still calculated.

### Output:
- Watterson's Theta (calculated for all, synonomous, and non-synonymous sites)
- Nucleotide Diversity (Pi) (calculated for all, synonomous, and non-synonymous sites)
- Nucleotide Diversity as alternatively calculated by Dendropy
- Effective Population Size (Ne)

- - - -

### Process Steps
#### Step 0: 
Change Evaluation; the input data folders are scanned for changes in structure since last run; if no changes are found for a given species, Steps 1 through 5 are skipped.
- Utilizes the 'find' bash command to compare structure
- Prior structure stored in text file AlreadyProcessed.txt
- This comparison is still somewhat weighty, but a *lot* faster than rerunning each step 1 through 5.

#### Step 1: 
Input organization; data is concatenated into single files of nucleotide sequences for each strain, which are sent to temp/<SpeciesLevelFolder>/BLAST
- Requires input data to be placed into input/\<SpeciesLevelFolder\>/\<StrainLevelFolder\>/
- Data can be ffn's, tgz's containing ffn's that will be unpacked, or fna.gz's that will be unzipped and changed to ffn's.
- Concatenated files are named based on the StrainLevelFolder name
- Different species data do not interact, but different strains of the same species do; the species level distinction only exists for performing the process en masse.

#### Step 2: 
BLAST filtering; data in temp/<SpeciesLevelFolder>/BLAST is first processed into strain-level databases, then queried against each other database within the species. Alternatively, if there are a significant number of strains (more than 400), a less rigorous but faster comparison will first filter strains to a more managable amount. Surviving data is sent to temp/\<SpeciesLevelFolder\>/Nucleotide
- Data points are a statistic referred to as identity; it is a function of total length minus total mismatches, and that difference over total length: id = (len - mm)/len.
- Note that data points are not the same %identity as returned by BLAST.
- Filtering is done in two steps, both using statistical hypothesis testing
  - Each BLAST of one strain against another (a 1v1 data point) is recorded to a dictionary (Key: String indicating the two strains s1_vs_s2, Value: Float indicating identity)
  - The data points are analyzed to obtain a sample size, mean, and standard error
  - The first hypothesis test poses the null hypothesis that each strain is acceptably dissimilar from each other.
  - The second hypothesis test poses the null hypothesis that each strain is acceptably similar to each other.
  - Both tests are performed with an alpha of .0001, and the second test recalculates sample size, mean, and standard error after the filtering of too similar strains from the first test
  - Test one compares each 1v1 against a critical upper boundary; if it is higher than this value, it is too similar, and the first of the two strains is removed*.
    - *The first of the two strains is not removed if the second of the two was already removed.
    - Critical upper boundary calculation: sample mean + ([absolute value of a z or t score with respect to alpha of .0001] * sample standard error)
      - t score, derived from student t distribution using degrees of freedom equal to one less than the sample size, is used if the sample size is less than 30
  - Test two compares the average of each* 1v1 involving a particular strain against a critical value; if that average is lower than this value, the strain is too dissimilar and removed.
    - *The average of each 1v1 for a given strain is only calculated from 1v1s of and against surviving strains that weren't removed in the prior test
    - Critical value calculation: sample mean - ([absolute value of a z or t score with respect to alpha of .001] * sample standard error)
      - t score, derived from student t distribution using degrees of freedom equal to one less than the sample size, is used if the sample size is less than 30
  - Each test separately prints a report of filtration information to a file; RemovalForSimilarity.txt and RemovalForDissimilarity.txt
  - Filtered strain files are copied to temp/\<SpeciesLevelFolder\>/Filtered; this is also where the filtration information reports go. Should memory prove to be a limiting factor, the strains do not need to be copied to here.

#### Step 3: 
Indexing; All gene headers and their line indexes are saved for each strain ffn file, for the purposes of a faster assembly of sequences into their orthogroups after the Orthofinder step.
- Note that this step takes place within 'orthofinding.sh', rather than having its own call in the outer 'autoEffLaunch.sh' program.

#### Step 4: 
Orthofinder; All surviving strains are plugged into Orthofinder, which processes up until it determines the Orthogroups.
- This step used to require translation to protein sequences rather than nucleotide, but updates to Orthofinder have since allowed us to plug in nucleotide sequences directly.
- Orthofinder outputs a file for single copy orthogroups, but this file only includes orthogroups for which all species contribute exactly once, and excludes any with non-contributors. This is not as useful to us as it might appear, because we are accepting of orthogroups with non-contributors.

#### Step 5: 
Single-Copy Orthogroup Filtering; Orthofinder's resulting Orthogroups.tsv file is used to determine all orthogroups for which all species contribute exactly 0 or 1 times. The nucleotide sequences for the genes in these orthogroups are gathered into files (one file per orthogroup), which are sent to muscle_input/\<SpeciesLevelFolder\>.
- Even using the previously established index file, this step is still somewhat long.

#### Step 6: 
MUSCLE alignment; files in muscle_input/<SpeciesLevelFolder> are ran through MUSCLE and outputted to muscle_output/<SpeciesLevelFolder>.
- Results are one alignment file per orthogroup

#### Step 7: 
Calculations; alignment files of muscle_output/<SpeciesLevelFolder> are processed to calculate Watterson's Theta, ThetaS, Theta N, Pi, PiS, and PiN. Additionally, the dendropy python module is used to calculate Dendropy's version of Theta and Pi (a slightly different algorithm).
-Theta or Pi without a letter represents 'All' meaning as calculated at all sites. S or N represent as calculated at Synonymous or Non-synonymous sites only, respectively.
- These numbers are calculated for each orthogroup. Then, all orthogroups with the same number of strains have their numbers averaged, and finally, all those averages are themselves averaged. This results in the final Thetas and Pis that are used to determine the NE for the whole species.
- Values of our Thetas (All, S, and N) per orthogroup can be found under final_output/\<SpeciesLevelFolder\>/wattersonsThetaValues.txt
- Similarly, values of our Pis (All, S, and N) per orthogroup can be found under final_output/\<SpeciesLevelFolder\>/piValues.txt
- Similarly, Dendropy's Theta and Pi values can be found under final_output/\<SpeciesLevelFolder\>/dendropyValues.txt

#### Step 8: 
Mutation Rate Fetch and Final NE Output; Mutation rates are pulled from mutation_rates.txt (currently, the rate must be manually entered here before running; this file is not altered, so this only needs to occur once, and should be treated as part of the input), and used with the species-level average Thetas and Pis to determine the NE, which is saved to final_output/Effective_Population_Sizes.txt.
- Mutation rates can be marked as "Unknown", which also results in "Unknown" being written into the final output.
- If a mutation rate is not indicated in the mutation_rates.txt file, the final output will also be marked as "Unknown".

- - - -

### Folder/file structure:
Root of all automated elements is currently called autoEffectivePop/. (PWD: /home/pmele/autoEffectivePop)

#### Programs/resources written explicitly for this process:
File | Description
-- | --
autoEffectivePop/fetchInput.sh | (A shell script for running fetchInput.py and the subsequent temporary shell scripts; fetches specified input species from NCBI databases)
autoEffectivePop/fetchInput.py | (Scans NCBI databases for the provided species name, locates the relevant files to pull as input, and writes a temporary shell script to wget anything relevant and store into the input folder)
autoEffectivePop/massFetch.sh | (A shell script that launches massFetch.py and forwards its output to fetchInput.sh for mass collection)
autoEffectivePop/massFetch.py | (Scans NCBI bacteria databases for every unique species name, reporting them in a massive list to be output to fetchInput.sh)
autoEffectivePop/autoEffLaunch.sh | (The main program; contains the calls for each sub-script, broken down in steps for ease of reading)
autoEffectivePop/inputProcessing.sh | (Prepares files in input folder; if a change occurs since last run, updates BLAST folder)
autoEffectivePop/blastFiltering.sh | (Performs actual BLASTing, then launches filterByIdentity.py for calculations)
autoEffectivePop/blastFilteringLite.sh | (Performs actual BLASTing, then launches filterByIdentityLite.py for fast calculations, then filterByIdentity.py on remaining)
autoEffectivePop/filterByIdentity.py | (Logic for filtering strains based on BLAST results.)
autoEffectivePop/filterByIdentityLite.py | (Logic for filtering strains based on BLAST results using a faster method meant for many species)
autoEffectivePop/orthofinding.sh | (Launches index.py for each strain, then runs Orthofinder, and finally launches gatherSingleCopyOrthogroups.py)
autoEffectivePop/getResultsFolder.py | (Logic for automating access to Orthofinder's results folders, which are named by date)
autoEffectivePop/index.py | (Logic for storing references to each sequence in a strain by the sequence header location)
autoEffectivePop/gatherSingleCopyOrthogroups.py | (Logic for determining all non-paralogous orthogroups via Orthofinder's orthogroups.tsv)
autoEffectivePop/findingOrthogroups.sh | (Launches gatherOrthogroupSequences.py)
autoEffectivePop/gatherOrthogroupSequences.py | (Logic for pulling and concatenating all sequences belonging to each orthogroup via the index file)
autoEffectivePop/muscleAligning.sh | (Calls muscle for aligning each orthogroup file)
autoEffectivePop/manualCalculations.py | (Logic for calculating Thetas and Pis, then averaging amongst same strain orthogroups, then final averaging)
autoEffectivePop/getMutationRate.py | (Logic for retrieving mutation rate data for a given species from mutation_rates.txt)
autoEffectivePop/calcEffPopSize.py | (Logic for calculating and outputting NE from Thetas/Pis and mutation rate)
autoEffectivePop/mutation_rates.txt | (Basic text file containing species names and their mutation rates in two tab-separated columns; considered as input)

#### Programs being utilized in this process, not written for it:
- autoEffectivePop/ncbi-blast-2.10.1+ 
- autoEffectivePop/Orthofinder 
- autoEffectivePop/muscle3.8.31_i86linux64 

#### Folders involved:
Folder | Description
-- | --
autoEffectivePop/input/\<SpeciesLevelFolder\>/\<StrainLevelFolder\>/ | (Nearly all base input data, with the exception of mutation rate information, is placed in sorted folders in input)
autoEffectivePop/temp/\<SpeciesLevelFolder\>/ | (Most internal processing steps use these folders and subfolders)
autoEffectivePop/temp/\<SpeciesLevelFolder\>/BLAST/ | (Where input data is placed in preparation for BLAST step)
autoEffectivePop/temp/\<SpeciesLevelFolder\>/Nucleotide/ | (Where surviving filtered BLASTed data is placed in preparation for Orthofinder step)
autoEffectivePop/temp/\<SpeciesLevelFolder\>/Error/ | (Where error messages from various points in the process are placed)
autoEffectivePop/temp/\<SpeciesLevelFolder\>/Filtered/ | (Where strains filtered for being too similar or dissimilar are placed)
autoEffectivePop/muscle_input/ | (Where gathered non-paralog orthogroup nucleotide sequences are placed in preparation for muscle step)
autoEffectivePop/muscle_output/ | (Where aligned sequences are placed in preparation for the Thetas/Pis calculation step)
autoEffectivePop/final_output/ | (Where final results are placed)
