""" Clean text files for Prospero
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
        self.capitalList = []
        self.capitals = "A-ZÉÈÜÄËÖÊ" 

    def set_content(self, content):
        """byte to str"""
        return content.decode('latin-1')

    def listCapitals(self, buf):
        buf = self.set_content(buf)
        tempList = re.findall(r"([%s]{2,})[^%s]"%\
            (self.capitals, self.capitals), buf)
        self.capitalList = set(tempList).union(self.capitalList)
 

if __name__ == '__main__':
    #for txt in list_files(os.getcwd()):
    C = Replacer()
    for txt in list_files("/home/josquin/corpus"):
        print(txt)
        with open(txt, 'rb') as f:
            buf = f.read()
        C.listCapitals(buf)
    print(C.capitalList)
        
 
