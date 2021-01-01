#!/usr/bin/env python

import sys
import gzip
import logging
from collections import Counter

# Create and configure logger
# https://docs.python.org/3/howto/logging.html,
# https://stackoverflow.com/a/56144390/
logging.basicConfig(level=logging.NOTSET)  # configure root logger
logger = logging.getLogger(__name__)  # create custom logger
# Logging levels: DEBUG/INFO/WARNING/ERROR/CRITICAL
logger.setLevel(logging.INFO)  # set logging level for our logger

# Variable definition

func_categories_file = sys.argv[1]
func_file = sys.argv[2]
# func_file = sys.stdin
cog_file = sys.argv[3]

# Initialize variables
category2description = {}
cog2category = {}
category2count = Counter()
my_cogs = set()
result = []

logger.info(f"Start reading files: {func_categories_file}, {func_file} and {cog_file}")

# Step 1: Read description of functional categories
with open(func_categories_file) as fin: 
    for lin in fin:
        if lin.startswith(" ["):
            splitat = 3  # position where to split the line
            ID, category = lin[splitat-1:splitat], lin[splitat+2:]
            category2description[ID] = category


# Step 2: Read file with OGs of interest
with open(cog_file) as fin:  
    for lin in fin:
        cog = lin.split("\t")[0]
        my_cogs.add(cog)
        

# Step 3: Read file with functional annotations
# and remember those for OGs of interest
# gzip: "rt" required for text mode, see https://docs.python.org/3/library/gzip.html
with gzip.open(func_file, "rt") as fin:
    for lin in fin:
        lin_split = lin.split("\t")
        cog = lin_split[1]
        ID = lin_split[2]
        if cog in my_cogs:
            cog2category[cog] = ID
        
logger.info(f"Start countig the frequency of the categories.")

# Step 4: Count and output the categories for OGs of interest

# counting the categories
category2count = Counter(cog2category.values())

# gives which categories occur in both datasets
intersection = category2description.keys() & category2count.keys()

# This produces nice but unsorted output
# for key in intersection:
#     print(counted_categories[key], category2description[key])

# This produces sorted list but it is not as nicely outputed
for key in intersection:
    result.append((category2count[key], category2description[key]))

result = sorted(result, key=lambda x: x[0], reverse=True)

# Write output as file directly
with open("results/cogs_arachaea_os97_functional_categories.txt", "w") as output:
    for row in result:
        s = " ".join(map(str, row))
        output.write(s)
        

logger.info(f"Whole program is done. The produced output for the last step is in the file results/cogs_arachaea_os97_functional_categories.txt. Exiting program.")
