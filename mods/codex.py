"""Metadata management of supports
by Josquin Debaz
GPL3
16/12/2019"""

import re
import json

def parse_supports_publi(supports_path):
    """get the supports from support.publi"""
    with open(supports_path, "r") as buf:
        return {item[3]: {'medium': item[1],
                          'author': item[1],
                          'media-type': item[2]}
                for item in [re.split(r"\s*;\s*", line)
                             for line in re.split(r"\r?\n", buf.read())
                             if not re.match(r"^\s*$", line)
                             and len(re.split(r"\s*;\s*", line)) == 4]}

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


def save_codex_json(codex, filename):
    """save codex as json in filename"""
    with open(filename, 'w') as codexfile:
        json.dump(codex, codexfile, indent=4, sort_keys=True)

if __name__ == "__main__":
##    supports = parse_supports_publi("../data/support.publi")
##    save_codex_json(supports, "codex.json")

    supports = parse_codex_cfg(r"C:\Program Files (x86)\Doxa\Prospéro-I\codex.cfg")
    save_codex_json(supports, "codex.json")
