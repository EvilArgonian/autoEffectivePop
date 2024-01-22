Purpose: To determine (for a provided category of species, represented as an input folder) the Core Genes, which are the genes found within every member species. Basic premise:
- Start with a list of consensus gene sequences for each species, and some pre-established arrangements of which species belong to which categories.
- Process a whole category at once; a single run of a category will take a random 90% of the species, and test each gene for its presence within it each species. Genes not found in every member of the 90% are eliminated.
- Genes that survive the whole run are then compared to the survivors of all other runs for the category. Those genes that consistently survived regardless of the random 90% are considered the true Core Genes. NOTE: For a gene to be compared to itself between runs, the gene has to have a non-arbitrary-name - essentially, it has to have some distinguishing identifier so that it is actually known to be the same gene as the one being compared to. The process of finding and labeling non-arbitrary-names has thus far proven to be the most complicating factor of this program.
- Once lists of Core Genes are established for each category, we can make meaningful conclusions based on the subsets of core genes shared by different categories.

All files and folders displayed as if from the Core_Gene_Finder superfolder.

Files:

- setupCategories.py	-	A helper file, ran before the main coreGeneFinder.sh file. Refers to the consensus sequences of the main program (autoEffectivePop) final_output folder, and to an input text file that describes which categories different species belong to, and uses this information to establish correctly initialized category folders for coreGeneFinder.sh to run from.
- reference.txt	-	 Tab-delimited table of species and the various categories they belong to. Meant to be passed to setupCategories.py
- referenceSimple.txt	-	As reference.txt, but without certain categories included.
- coreGeneFinder.sh	-	This is the main script, which sets up and calls other files.
- initialGeneSetup.py	-	Establishes the means of determining if a gene is in fact the same as another gene by giving each a non-arbitrary name (used as the file name). Refers back to the outside ../temp/<species>/muscle_output/<gene_ref> to find and record tagged details such as the labeled gene, locus_tag, protein_id, and protein. Can be setup to use different tags or other details for its different names, and should it fail to produce a meaningful feature to make a name out of, will instead name the gene 'Arbitrary_Gene_<#>' (while the process can proceed for other genes, this is a failure state, as it can no longer adequately verify that the arbitrarily named gene actually matches other genes in other runs).
- cog-20.cog.csv	-	A file used as a reference for one mode of non-arbitrary-naming performed in initialGeneSetup.py
- passGene.py	-	Compares a still-surviving gene to the genes of the next species in the category. If that gene is also found in that species, it flags as passing (surviving), else it flags as not passing and therefore not a core gene for this run.


Folders:
- consensus_input/	-	A folder where consensus sequences produced by the main program (autoEffectivePop) are held. These are used to describe the genes belonging to each species. Notably, these will not consists of all genes in the species, but rather, only the genes that belonged to the single-copy-orthogroups processed in the main program.
- core_genes/<category>/<Run_#>	-	Holds output core gene information, sorted by category into runs. A category is ran X times (an input given to coreGeneFinder, and the concluded true core genes are those that appear in all X runs.
- core_genes/<category>/Core_Genes.txt	-	Records the core genes shared by all runs of the category. This is the final output of the Core Gene Finder program.

Notes:
- It appears that an idea to move the non-arbitrary-naming done by initialGeneSetup to the end of a run instead of the start was considered, but not implemented. Doing so would reduce the amount of effort it would take to do the non-arbitrary-naming, since the non-surviving genes could be skipped.
- It appears that an idea to use InterProScan for non-arbitrary-naming was considered but also not implemented.