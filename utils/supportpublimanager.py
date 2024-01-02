import os
import re


class SupportPubliManager:
    """Deal with support.publi"""

    def __init__(self):
        self.codex = {}
        self.sources = {}

        path1 = "data/support.publi"
        path2 = "../data/support.publi"

        if os.path.isfile(path1):
            with open(path1, 'rb') as handle:
                self.path = path1
                buf = (handle.read().decode('cp1252'))
        else:
            with open(path2, 'rb') as handle:
                self.path = path2
                buf = (handle.read().decode('cp1252'))
        lines = re.split('\r*\n', buf)

        for line in lines:
            source = line.split(";")
            if len(source) == 4:
                self.codex[source[0]] = {
                    'source': source[1].strip(),
                    'type': source[2].strip(),
                    'abr': source[3].strip()
                }
                self.sources[source[1].strip()] = {
                    'type': source[2].strip(),
                    'abr': source[3].strip()
                }

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
