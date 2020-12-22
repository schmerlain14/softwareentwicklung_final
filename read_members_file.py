#!/usr/bin/env python

"""Parse eggNOG members files and select OGs based on occurence
and uniqueness."""

import sys
import argparse
import logging
from collections import Counter, defaultdict

# Create and configure logger
# https://docs.python.org/3/howto/logging.html,
# https://stackoverflow.com/a/56144390/
logging.basicConfig(level=logging.NOTSET)  # configure root logger
logger = logging.getLogger(__name__)  # create custom logger
# Logging levels: DEBUG/INFO/WARNING/ERROR/CRITICAL
logger.setLevel(logging.INFO)  # set logging level for our logger

# Global variables
all_taxids = set()
good_cogs = set()
cog2taxids = {}
cog2seqids = {}
taxid2missing_cogs = defaultdict(list)


def uniques(lst):
    """Returns list of elements which occur only once.

    >>> uniques([3,4,5,4,3,4,6])
    [5,6]
    """
    counter = Counter(lst)
    return [el for el, count in counter.items() if count == 1]


def calc_stats(taxids, all_taxids):
    """Calculates occurence and uniqueness of orthologous groups (OGs).

    Args:
        taxids: Taxids of sequences comprising an OG
        all_taxids: All taxids in this taxonomic group

    Returns: A tuple with 3 values,
        - % occurence of this OG (with regard to all taxids comprising
            the tax. group)
        - % uniqueness of this OG (with regard only to the taxids where
            it occurs)
        - % occurence of this OG as single-copy (with regard to all taxids)

    Example:

    >>> calc_stats([2,3,4,4], set([2,3,4,5]))
    (75.0, 66.66666666666667, 50.0)

    The arguments mean:
        (a) the OG consists of 4 sequences in 3 organisms (taxids): [2,3,4,4]
        (b) the taxonomic group consists of 4 organisms (taxids): [2,3,4,5]

    The result means:
        - occurence → 75% (OG is found in 3 out of 4 taxids)
        - uniqueness → 66% (OG is single-copy in 2 out of 3 taxids)
        - occurence_as_singlecopy → 50% (OG occurs as single-copy in 2 out of 4
            taxids)
    """
    # Basic argument checking
    assert len(set(all_taxids)) == len(all_taxids), "Taxids occur more than once?"
    # Your code here
    return (False, False, False)


def parse_members_file(fin):
    """Parses eggNOG 'members' file and remembers taxids and seqids comprising
    each OG.

        Example: Line from eggnog_5.0/per_tax_level/1/1_members.tsv.gz
            1   28H59   4   3   565033.GACE_1005,572546.Arcpr_0848,69014.TK0075,69014.TK0091    565033,572546,69014

        Explanation:
            level "1" (root); OG identifier "28H59"; 4 sequences in 3 organisms;
            sequence identifiers; organism taxids
    """
    logger.info(f"Parsing members file: {fin.name}...")
    for i, line in enumerate(fin):
        level, cog_id, n_seqs, n_taxids, seq_ids, taxids = line.strip().split("\t")

        # Taxids where OG occurs
        taxids = taxids.split(",")
        # simple consistency check
        assert (
            len(taxids) == len(set(taxids)) == int(n_taxids)
        ), f"??? {line}\n {cog_id} -> {len(taxids)}---{len(set(taxids))}---{n_taxids}"

        # Remember all taxids we've seen so far
        all_taxids.update(taxids)

        # Sequences comprising the OG
        seq_ids = seq_ids.split(",")
        assert len(seq_ids) == int(n_seqs)  # consistency check
        seq_ids_taxids = [el.split(".")[0] for el in seq_ids]

        # Remember the important stuff
        assert cog_id not in cog2taxids  # consistency check
        cog2taxids[cog_id] = seq_ids_taxids
        cog2seqids[cog_id] = seq_ids
    logger.info(f"Done. Read {i} lines from {fin.name}")


def missing_taxids(cog, taxids):
    """Determines which OGs are missing from which taxids."""
    logger.debug(f"Determining missing taxids for {cog}")
    # Your code here


def output_seqids(filename, cogs):
    """Writes seqids to file."""
    logger.info(f"Outputting seqids to: {filename}")
    with open(filename, "w") as fout:
        for cog in cogs:
            for seqid in cog2seqids[cog]:
                # taxid = seqid.split('.')[0]
                print(f"{seqid}\t{cog}", file=fout)


def determine_cogs(args):
    """Identifies OGs matching the criteria."""
    logger.info(
        f"""Got {len(cog2taxids)} OGs. Identifying OGs
        matching the criteria (occurence/uniqueness)..."""
    )
    print("#cog\t%_occurence\tthereof_%_singlecopy\t%_occurence_as_singlecopy")

    good_cogs = set()
    for cog, taxids in cog2taxids.items():
        occurence, uniqueness, occurence_as_singlecopy = calc_stats(taxids, all_taxids)
        logger.debug(
            f"""{cog} → occurence, uniqueness, occurence_as_singlecopy:
            {occurence:.3f}, {uniqueness:.3f}, {occurence_as_singlecopy:.3f}"""
        )

        # if cog == 'COG1841':
        #   print(occurence, uniqueness, occurence_as_singlecopy, file=sys.stderr)
        if (
            (occurence < args.min_occurence)
            or (uniqueness < args.min_uniqueness)
            or (occurence_as_singlecopy < args.min_occurence_as_singlecopy)
        ):
            continue

        missing_taxids(cog, taxids)
        good_cogs.add(cog)
        logger.debug(f"{cog} accepted → num good OGs: {len(good_cogs)}")

        output = "\t".join(
            [
                cog,
                f"{occurence:.1f}",
                f"{uniqueness:.1f}",
                f"{occurence_as_singlecopy:.1f}",
            ]
        )
        print(output)
    logger.info(f"Done. Found {len(good_cogs)} OGs matching criteria.")

    # Output sequence identifiers
    if args.seqids_out:
        output_seqids(args.seqids_out, good_cogs)

    # Output taxids with missing cogs
    if args.missing:
        logger.info(f"Outputting taxids with at least {args.missing} missing OGs.")
        # Your code here
        pass


def main(args):
    """Main function."""
    logger.debug("Executing main function.")
    # ncbi = NCBITaxa(dbfile=args.ete3_db)  # initialize ete3 database
    # logger.info("Reading input...")
    parse_members_file(sys.stdin)
    # logger.info("Outputting results...")
    determine_cogs(args)
    logger.info("Exiting program.")


if __name__ == "__main__":
    # Parse and check arguments
    parser = argparse.ArgumentParser(
        description="""Parse eggNOG file and and select OGs based on occurence
        and uniqueness."""
    )
    parser.add_argument(
        "-min_occurence",
        metavar="PERCENT",
        action="store",
        type=float,
        default=0,
        help="""Minimum occurence (percent of genomes where gene is present);
        should be 0-100, default=0""",
    )
    parser.add_argument(
        "-min_uniqueness",
        metavar="PERCENT",
        action="store",
        type=float,
        default=0,
        help="""Minimum uniqueness if present (percent of genomes where gene
        is present as single-copy); should be 0-100, default=0""",
    )
    parser.add_argument(
        "-min_occurence_as_singlecopy",
        metavar="PERCENT",
        action="store",
        type=float,
        default=0,
        help="""Minimum combined occurence+uniqueness (e.g. single-copy in 97%%
        of all genomes); shouled be 0-100, default=0""",
    )
    parser.add_argument(
        "-seqids_out",
        metavar="filename",
        action="store",
        type=str,
        help="Output seqids of proteins in matching OGs",
    )
    parser.add_argument(
        "-missing",
        metavar="num_missing_OGs",
        action="store",
        type=int,
        default=0,
        help="""If a taxid is lacking at least this number of OGs, output it
        to standard error""",
    )
    args = parser.parse_args()
    # print(args)

    if (args.min_occurence or args.min_uniqueness) and args.min_occurence_as_singlecopy:
        print(
            """It doesn't seem to make sense to set min. occurence/min.
            uniqueness AND min. occurence+uniqueness at the same time. Pick
            one.""",
            file=sys.stderr,
        )
        sys.exit(1)

    logger.warning(f"Program arguments: {args}")
    main(args)
