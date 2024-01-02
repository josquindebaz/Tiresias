import os
import re


def read_publi_file():
    path = "data/support.publi"
    path = path if os.path.isfile(path) else "../data/support.publi"

    with open(path, 'rb') as handle:
        buf = (handle.read().decode('cp1252'))

    return buf, path


def parse_publi(publi_content):
    codex = {}
    sources = {}

    for line in re.split('\r*\n', publi_content):
        source = line.split(";")
        if not len(source) == 4:
            continue

        stripped = list(map(lambda item: item.strip(), source))
        codex[source[0]] = {
            'source': stripped[1],
            'type': stripped[2],
            'abr': stripped[3]
        }

        sources[stripped[1]] = {
            'type': stripped[2],
            'abr': stripped[3]
        }

    return codex, sources


class SupportPubliManager:
    """Deal with support.publi"""

    def __init__(self):
        self.path = None
        self.codex = {}
        self.sources = {}

        buf, self.path = read_publi_file()
        self.codex, self.sources = parse_publi(buf)

    def add(self, k, source, typ, abbr):
        """add a source to the dic"""
        self.codex[k] = {
            'source': source,
            'type': typ,
            'abr': abbr
        }
        if source not in self.sources.keys():
            self.sources[source] = {
                'type': typ,
                'abr': abbr
            }

    def write(self):
        """write as file"""
        sources = sorted(["%s; %s; %s; %s\n" % \
                          (k, v['source'], v['type'], v['abr']) \
                          for k, v in self.codex.items()])
        with open(self.path, 'w', encoding='cp1252') as handle:
            handle.writelines(sources)

    def fusion(self, candidats_file):
        with open(candidats_file, 'rb') as handle:
            buf = (handle.read().decode('cp1252'))
        lines = re.split('\r*\n', buf)
        for candidat in [re.split(r";\s+", support) for support in lines]:
            if len(candidat) == 4:
                if candidat[0] not in self.codex:
                    self.add(candidat[0],
                             candidat[1],
                             candidat[2],
                             candidat[3])
