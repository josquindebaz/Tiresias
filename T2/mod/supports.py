import re
import os

class publi(object):
    def __init__(self):
        self.codex = {}

        if os.path.isfile("data/support.publi"):
            with open("data/support.publi", 'rb') as f:
                b = (f.read().decode())
        else:
            with open("../data/support.publi", 'rb') as f:
                b = (f.read().decode())
        lines = re.split('\r*\n', b)

        for l in lines:
            s = l.split(";")
            if (len(s) == 4):
                self.codex[s[0]] = {
                    'source': s[1].strip(),
                    'type': s[2].strip(),
                    'abr': s[3].strip()
                    }
