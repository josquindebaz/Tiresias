"""Metadata management by supports
by Josquin Debaz
GPL3
16/12/2019"""

import re
import json
import os

def parse_supports_publi(supports_path):
    """get the supports from support.publi"""
    sources = {}
    with open(supports_path, "r") as buf:
        source_list = [item for item
                       in [re.split(r"\s*;\s*", line)
                           for line in re.split(r"\r?\n", buf.read())
                           if not re.match(r"^\s*$", line)
                           and len(re.split(r"\s*;\s*", line)) == 4]
                       ]
    for item in source_list[0:15]:
        if item[3] in sources:
            sources[item[3]]['forms'].append(item[0])
        else:
            sources[item[3]] = {'medium': item[1],
                                'author': item[1],
                                'media-type': item[2],
                                'forms': [item[0]]}
    return sources


def parse_codex_cfg(codex_path):
    """get the supports from codex.cfg"""
    codex = {}
    transpose = {
        "ABREV": "ABREV",
        "AUTEUR": "author",
        "SUPPORT": "medium",
        "TYPE-SUPPORT": "media-type",
        "STATUT-AUTEUR": "authorship",
        "LIEU-EMISSION": "localisation",
        "CHAMP-1": "open-field-1",
        "CHAMP-2": "open-field-2",
        "OBSERVATION": "observations",
        "DATE": "date"
        }

    with open(codex_path, "r") as buf:
        for support in [re.split(r"\r?\n", item)
                        for item in re.split(r"#{2,}", buf.read())
                        if not re.match(r"^\s*$", item)]:

            values = {transpose[key[0].strip()]: key[1].strip()
                      for key in [re.split(r"\s*:\s*", item, 1)
                                  for item in support
                                  if item]}

            codex[values["ABREV"]] = {key: value
                                      for key, value
                                      in values.items()
                                      if key != "ABREV"}
    return codex

class CodexManager():
    def __init__(self, codexpath=""):
        self.conflicts = []
        self.codex = {}

        if os.path.isfile(codexpath):
            with open(codexpath, 'r') as filepointer:
                self.codex = json.load(filepointer)

    def get_fields(self):
        fields = []
        for item in self.codex.values():
           for key in item.keys():
                if key not in fields:
                    fields.append(key)
        return fields
    
    def save_codex_json(self, filename):
        """save codex as json in filename"""
        with open(filename, 'w') as codexfile:
            json.dump(self.codex, codexfile, indent=4, sort_keys=True)
        
    def merge_codex(self, candidate):
        """merge candidate with local and keep conflict"""
        for support in candidate:
            if support not in self.codex:
                self.codex[support] = candidate[support]
            elif candidate[support] != self.codex[support]:
                self.conflicts.append(support)
    
if __name__ == "__main__":
    supports_publi = parse_supports_publi("../data/support.publi")
    m = CodexManager()
    m.merge_codex(supports_publi)
    m.save_codex_json("codex.json")

##    supports_codex = parse_codex_cfg(r"C:\Program Files (x86)\Doxa\Prospéro-I\codex.cfg")
##    save_codex_json(supports_codex, "codex.json")
##    Merger = Merger(supports_publi, supports_codex)
##    Merger.merge_codex()
##    for conflict in Merger.conflicts:
##        print("Conflict for ", conflict)
##        print("reference: ", supports_publi[conflict])
##        print("candidate: ", supports_codex[conflict])
##        pass
        
