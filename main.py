#!/usr/local/bin/python
from PDB2DB import PDB2DB
from NCMParser import NCMParser
from prody import parsePDB, writePDB, parsePDBHeader

from operator import itemgetter
from itertools import groupby
from subprocess import call

import urllib
import os

TMP_DIR = "tmp/"
SUBSET_DIR = "subsets/"
PDB_CSV = "pdb.csv" # Comma delimited list of PDB identifiers
MC_ANNOTATE = "MC-Annotate" # mc-annotate binary

# Read csv
f = open(PDB_CSV, 'r')
pdb_ids = f.read().splitlines()
pdb_ids = pdb_ids[0].split(",")

# Make tmp dir
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

for pdb_id in pdb_ids:
    print "\n=> %s" % pdb_id
    pdb_file = pdb_id + ".pdb"
    pdb_path = TMP_DIR + pdb_file
    if not os.path.isfile(pdb_path):
        print "Downloading " + pdb_file + " to " + pdb_path
        urllib.urlretrieve("http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId=" + pdb_id, pdb_path)
    else:
        print "Found PDB file at " + pdb_path

    db_path = pdb_path + ".db"
    if not os.path.isfile(db_path):
        print "Converting " + pdb_path + " to dot bracket"
        pdb2db = PDB2DB().pdb2db
        dot_bracket = pdb2db(pdb_path)
        print "Saving dot bracket to " + pdb_path
        f = open(db_path, 'w')
        f.write(dot_bracket)
        f.close()
    else:
        f = open(db_path, 'r')
        dot_bracket = f.read()
        f.close()
        print "Found dot bracket at " + db_path
    print "Dot bracket : " + dot_bracket

    # print "Parsing dot bracket for NCMs"
    ncmparser = NCMParser()
    ncmparser.ncmparser(dot_bracket)

    # Make tmp dir
    if not os.path.exists(SUBSET_DIR):
        os.makedirs(SUBSET_DIR)

    atoms = parsePDB(pdb_path, model=1)
    try:
        first_idx = parsePDBHeader(pdb_path, "polymers")[0].dbrefs[0].first[0]
    except:
        first_idx = 1

    for ncm in ncmparser.ncms:
        for ncm_code in ncm: # just one in each
            reslst = ncm[ncm_code]
            reslst = [x + first_idx for x in reslst]
            subset = atoms.select("resnum " + ' '.join(map(str, reslst)))

            # convert ranges
            ranges = ""
            for k, g in groupby(enumerate(reslst), lambda (i, x): i - x):
                cur_range = map(itemgetter(1), g)
                ranges += str(cur_range[0])
                ranges += "-"
                ranges += str(cur_range[len(cur_range) - 1])
                ranges += "_"
            ranges = ranges[:-1]

            subset_filepath = SUBSET_DIR + pdb_id + "." + ncm_code + "." + ranges + ".pdb"
            print "Writing " + str(subset) + " to " + subset_filepath
            writePDB(subset_filepath, subset)

            # MC-Annotate
            mca_subset_filepath = subset_filepath + ".mca"
            print "Writing MC-Annotate output to " + mca_subset_filepath
            call([MC_ANNOTATE, subset_filepath, ">", mca_subset_filepath])
