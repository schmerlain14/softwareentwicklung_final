#!/usr/bin/env python

import sys
import gzip
from collections import Counter

func_categories_file = sys.argv[1]
func_file = sys.argv[2]
# func_file = sys.stdin
cog_file = sys.argv[3]

# Initialize variables
category2description = {}
cog2category = {}
category2count = Counter()
my_cogs = set()


# Step 1: Read description of functional categories
with open(func_categories_file) as fin:
    pass


# Step 2: Read file with OGs of interest
with open(cog_file) as fin:
    pass


# Step 3: Read file with functional annotations
# and remember those for OGs of interest
# gzip: "rt" required for text mode, see https://docs.python.org/3/library/gzip.html
with gzip.open(func_file, "rt") as fin:
    pass


# Step 4: Count and output the categories for OGs of interest
