#!/usr/bin/bash
###### Use the eggNOG 5.0 database to identify conserved single-copy genes.
set -eu -o pipefail  # options for safe Bash scripting

### Variable section
# base directory
DATADIR=eggnog_data

# members files
bacteria=$DATADIR/2_members.tsv.gz
archaea=$DATADIR/2157_members.tsv.gz
eukaryota=$DATADIR/2759_members.tsv.gz
# The file names correspond to NCBI taxonomy identifiers (taxids)
# of these groups. E.g., 2157 is the archaea taxid:
# https://www.ncbi.nlm.nih.gov/taxonomy/?term=2157

# annotations files
archaea_fct=$DATADIR/2157_annotations.tsv.gz
func_categories=$DATADIR/eggnog4.functional_categories.txt
# eggNOG 5.0 doesn't provide a "functional_categories" file, so we're using
# the file from eggNOG 4.5
###

### Set up environment
mkdir -p $DATADIR
if [ -z "$(ls $DATADIR)" ]; then
    # Download data from eggNOG (e.g. using wget)
    # http://eggnog5.embl.de/download/eggnog_5.0/
    pushd $DATADIR
    echo "Downloading required data files..."
    # Your code here
    popd
fi

### 1. Which genes (OGs) occur in at least 99% of all genomes in the eggNOG5 database
# in each domain of life, respectively?
# (For large gzipped files, reading from stdin is usually faster than using the "gzip"
# module in Python)
zcat $bacteria | ./read_members_file.py -min_occurence 99 > cogs_bacteria_o99.txt
zcat $archaea | ./read_members_file.py -min_occurence 99 > cogs_archaea_o99.txt
zcat $eukaryota | ./read_members_file.py -min_occurence 99 > cogs_eukaryota_o99.txt

### 2. Which bacterial genes occur in at least 50% of all bacterial genomes, and in
# at least 99% thereof as single-copy?
zcat $bacteria | ./read_members_file.py -min_occurence 50 -min_uniqueness 99 > cogs_bacteria_o50_u99.txt
# How many of these OGs were also identified as universal bacterial OGs (from previous question)?
comm -12 cogs_bacteria_o99.txt cogs_bacteria_o50_u99.txt

### 3. Identify all OGs that occur as single-copy in at least 97% of all archaea
zcat $archaea | ./read_members_file.py -min_occurence_as_singlecopy 97 > cogs_archaea_os97.txt
# Are there archaea which lack 4 or more of those universal OGs?
zcat $archaea | ./read_members_file.py -min_occurence_as_singlecopy 97 -missing 4

### 4. Compile an overview of the functional categories of these 121 archaeal OGs
./annotate_cogs.py $func_categories $archaea_fct cogs_archaea_os97.txt
