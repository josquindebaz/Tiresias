""" Word Replacer
Author Josquin Debaz
GPL 3
"""
import os
import re

def list_files(rep='.', exts=('.txt', '.TXT'), recursive=True):
    """List txt files"""
    txt_files = []
    for roots, _, files in os.walk(u'%s'%rep):
        txt_files.extend([os.path.join(roots, f) for f in files \
            if os.path.splitext(f)[1] in exts])
        if not recursive:
            break
    return txt_files

class Replacer():
    """Replace froms with To"""
    def __init__(self):
        self.log = None
        self.content = None
        self.motif = None
        self.repl = None

    def set_content(self, content):
        """byte to str"""
        self.content = content.decode('latin-1')

    def set_motif(self, tofrom, with_marks=True):
        """Compile from and to"""
        if with_marks:
            marks = r'\s"' + re.escape(".,;!?':¿(){}[]-")
        else:
            marks = r"\s"
        froms = [re.escape(i) for i in tofrom[1:]]
        froms = "(^|[%s])(%s)([%s]|$)" % (marks,
                                          '|'.join(froms), marks)
        self.motif = re.compile(froms)
        self.repl = r"\g<1>%s\g<3>"%tofrom[0]

    def process(self):
        """execute replacements"""
        self.log = 0
        while self.motif.search(self.content):
            self.content = self.motif.sub(self.repl, self.content, 1)
            self.log += 1

if __name__ == '__main__':
    for txt in list_files("."):
        print(txt)
        C = Replacer()
        list_motif = ["6TEST", "ta", "*", "19", "{"]
        print(list_motif)
        C.set_motif(list_motif) #To, From1, From2...
        with open(txt, 'rb') as f:
            buf = f.read()
            C.set_content(buf)
            C.process()
        print(buf)


        if C.log:
            print(C.log)
            buf = bytes(C.content, 'latin-1')
            print(str(buf))
            #with open(txt, 'wb') as f:
            #    f.write(buf)
