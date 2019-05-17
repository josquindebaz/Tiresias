import re
import os

class Publi(object):
    def __init__(self):
        self.codex = {}
        self.sources = {}

        path1 = "data/support.publi"
        path2 = "../data/support.publi"

        if os.path.isfile(path1):
            with open(path1, 'rb') as f:
                self.path = path1
                b = (f.read().decode('cp1252'))
        else:
            with open(path2, 'rb') as f:
                self.path = path2
                b = (f.read().decode('cp1252'))
        lines = re.split('\r*\n', b)

        for l in lines:
            s = l.split(";")
            if (len(s) == 4):
                self.codex[s[0]] = {
                    'source': s[1].strip(),
                    'type': s[2].strip(),
                    'abr': s[3].strip()
                    }
                self.sources[s[1].strip()] = {
                    'type': s[2].strip(),
                    'abr': s[3].strip()
                    }

    def add(self, k, s, t , a):
        self.codex[k] = {
            'source': s,
            'type': t,
            'abr': a
            }
        if s not in self.sources.keys():
            self.sources[s] = {
                'type': t,
                'abr': a,
            }

    def write(self):
        L = sorted(["%s; %s; %s; %s\r\n" %(k, 
                v['source'], v['type'], v['abr']) 
                for k, v in self.codex.items() ])
        with open(self.path, 'w') as f:
            f.writelines(L)
 
