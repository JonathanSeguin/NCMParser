import requests
import os
class PDB2DB:
    def pdb2db(self, file_path):
        url = "http://major.iric.ca/~blanchmf/pdb2db_v2/upload.cgi"
        files = {'referencepdb': (os.path.basename(file_path), open(file_path, 'rb'), 'application/x-pdb', {'Expires': '0'})}
        data = {'nbcombinedlayers': '1',
                'nbsplitlayers': '0'}

        response = requests.post(url, data=data, files=files)
        dot_bracket = response.text.replace("<pre>", "")
        dot_bracket = dot_bracket.replace("</pre>", "")

        return dot_bracket

if __name__ == "__main__":
    pdb = PDB2DB()
    pdb.pdb2db("2KUU.pdb")
