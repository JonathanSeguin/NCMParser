# Dot-Bracket NCM Parser and Statistical Analysis Pipeline
This project aims to provide an automated pipeline for the statistical analysis of the NCM (nucleotide cyclic motif) content in PDB structures.

## Content
#### **PDB2DB**
Wrapper for the PDB2DB script running at http://major.iric.ca/~blanchmf/pdb2db_v2/.

##### Usage (standalone)

    $PDB2DB.py 2KUU.pdb

##### Usage (class)

    pdb = PDB2DB()
    out = pdb.pdb2db("2KUU.pdb")


#### **NCMParser**

##### Usage (standalone)

    $NCMParser.py dotbracket_file.db

##### Usage (class)

    parser = NCMParser()
    parser.ncmparser(".(.(...)))")
    out = parser.ncms

#### **main.py**
Pipeline script wrapping PDB2DB, NCMParser, ProDy PDB parsing and MC-Annotate.

##### Usage
Simply set the various variables in the script header (location of the MC-Annotate executable, list of PDB IDs etc...) and run.

#### **pdb.csv**
List of 531 "non redundant" PDB IDs as found in the Supplementary Methods of the 2008 Nature paper by Marc Parisien and Francois Major (*Parisien, Marc, and Francois Major. "The MC-Fold and MC-Sym pipeline infers RNA structure from sequence data." Nature 452.7183 (2008): 51-55*)

----------

Jonathan Seguin (2015).
