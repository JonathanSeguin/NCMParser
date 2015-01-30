#!/usr/local/bin/python
from PDB2DB import PDB2DB
from NCMParser import NCMParser
import urllib
import os

# Read csv
f = open('pdb.csv', 'r')
pdb_ids = f.read().splitlines()
pdb_ids = pdb_ids[0].split(",")

TMP_DIR = "tmp/"

# Make tmp dir
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

for pdb_id in pdb_ids:
    pdb_file = pdb_id + ".pdb"
    pdb_path = TMP_DIR + pdb_file
    if not os.path.isfile(pdb_path):
        print "Downloading " + pdb_file + " to tmp/" + pdb_file
        urllib.urlretrieve("http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId=" + pdb_id, pdb_path)

    print "Converting " + pdb_path + " to dot bracket"
    pdb2db = PDB2DB().pdb2db
    dot_bracket = pdb2db(pdb_path)
    print dot_bracket

    print "Parsing dot bracket for NCMs"
    ncmparser = NCMParser()
    ncmparser.ncmparser(dot_bracket)
    print ncmparser.ncms
