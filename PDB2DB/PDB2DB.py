#!/usr/bin/python
import requests
import os, sys
class PDB2DB:
    def pdb2db(self, file_path, first_form=True):
        url = "http://major.iric.ca/~blanchmf/pdb2db_v2/upload.cgi"
        files = {'referencepdb': (os.path.basename(file_path), open(file_path, 'rb'), 'application/x-pdb', {'Expires': '0'})}
        data = {'nbcombinedlayers': '1',
                'nbsplitlayers': '0'}

        response = requests.post(url, data=data, files=files)

        out = response.text.replace("<pre>", "")
        out = out.replace("</pre>", "")

        dot_brackets = {}

        try:
            if first_form and out:
                lines = out.splitlines()
                for i in range(0, len(lines), 3):
                    line = lines[i].lstrip()
                    print line
                    polymer_id = line[6] + line[7] # >1QC0:1
                    print polymer_id
                    if polymer_id != "1:":
                        break
                    else:
                        chain_id = line[8] # >1QC0:1:A
                        dot_brackets[chain_id] = lines[i + 2]
        except:
            print "PDB2DB Error!"

        return dot_brackets

if __name__ == "__main__":
    pdb = PDB2DB()
    try:
        print pdb.pdb2db(sys.argv[1])
    except:
        print "Usage : pdb2db.py filename.pdb"
