#!/usr/local/bin/python
from PDB2DB import PDB2DB
from NCMParser import NCMParser
from prody import parsePDB, writePDB, parsePDBHeader

from operator import itemgetter
from itertools import groupby
from subprocess import call

import urllib
import os
import glob

TMP_DIR = "tmp/"
SUBSET_DIR = "subsets/"
PDB_CSV = "pdb.csv" # Comma delimited list of PDB identifiers
MC_ANNOTATE = "MC-Annotate" # mc-annotate binary

errors = {'PDB2DB': [],
          'NCRN': []}

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

    atoms = parsePDB(pdb_path, model=1)
    pdb_header = parsePDBHeader(pdb_path)

    db_paths = glob.glob(pdb_path + ".*.db")
    dot_brackets = {}
    if not db_paths:
        print "Converting " + pdb_path + " to dot bracket"
        pdb2db = PDB2DB().pdb2db
        dot_brackets = pdb2db(pdb_path)
        if not dot_brackets:
            errors['PDB2DB'].append(pdb_id)
            break
        print dot_brackets

        for p_id in dot_brackets:
            db_path = pdb_path + "." + p_id + ".db" # First polymer
            print "Saving dot bracket to " + db_path
            f = open(db_path, 'w')
            f.write(dot_brackets[p_id])
            f.close()
    else:
        for db_path in db_paths:
            chain_id = db_path[-5]
            f = open(db_path, 'r')
            dot_bracket = f.read()
            dot_brackets[chain_id] = dot_bracket
            f.close()
            print "Found dot bracket at " + db_path

    # Make tmp dir
    if not os.path.exists(SUBSET_DIR):
        os.makedirs(SUBSET_DIR)

    for chain_id, dot_bracket in dot_brackets.iteritems():
        print "Dot bracket : " + dot_bracket
        ncmparser = NCMParser()
        ncmparser.ncmparser(dot_bracket)
        print "NCMs : " + str(ncmparser.ncms)

        first_idx = 1
        try:
            for pol in pdb_header["polymers"]:
                if pol.chid == chain_id:
                    first_idx = pol.dbrefs[0].first[0]
        except:
            pass

        for ncm in ncmparser.ncms:
            for ncm_code in ncm: # just one in each
                reslst = ncm[ncm_code]
                reslst = [x + first_idx for x in reslst]
                reslst = filter(lambda x: x >= 0, reslst)

                subset = atoms.select("resnum " + ' '.join(map(str, reslst))) # hack for negative starting res index (1JU7)

                if subset:
                    # convert ranges
                    ranges = ""
                    for k, g in groupby(enumerate(reslst), lambda (i, x): i - x):
                        cur_range = map(itemgetter(1), g)
                        ranges += str(cur_range[0])
                        ranges += "-"
                        ranges += str(cur_range[len(cur_range) - 1])
                        ranges += "_"
                    ranges = ranges[:-1]

                    subset_filepath = SUBSET_DIR + pdb_id + "." + chain_id + "." + ncm_code + "." + ranges + ".pdb"
                    print "Writing " + str(subset) + " to " + subset_filepath
                    writePDB(subset_filepath, subset)

                    # MC-Annotate
                    mca_subset_filepath = subset_filepath + ".mca"
                    print "Writing MC-Annotate output to " + mca_subset_filepath
                    fout = open(mca_subset_filepath, 'w')
                    call([MC_ANNOTATE, subset_filepath], stdout=fout)
                else:
                    print "ERROR: Non continuous residue numbers" # they exists : 1FG0
                    errors['NCRN'].append(pdb_id)

print errors
