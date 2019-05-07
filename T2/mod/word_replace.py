# Author Josquin Debaz
# GPL 3
import os
import re


def list_files(rep='.', exts=['.txt', '.TXT'], recursive=True):
    L = []
    for roots, dirs, files in os.walk(u'%s'%rep):
        L.extend([os.path.join(roots, f) for f in files \
            if (os.path.splitext(f)[1] in exts)] )
        if recursive == False:
            break        
    return L

class WR(object):
    def __init__(self, content):
        self.content = content.decode('latin-1') #byte to str
        self.log = None

    def process(self, m=True):
        if (m):
            marks = "[\s\.,;!\?\"':¿\(\)]"
        else:
            marks = "\s"
            
        FROM = "(^|%s)(%s)(%s|$)" % (marks, '|'.join(self.TOFROM[1:]), marks)
        
        motif = re.compile(FROM)
        n = len(motif.findall(self.content))
        if (n):
            self.content = motif.sub("\\1%s\\3"%self.TOFROM[0], self.content)
            self.log = n
        
               
    
if __name__ == '__main__':
    list_TXT = list_files(".")
    for txt in list_TXT:
        print(txt)
        with open(txt, 'rb') as f:
            buf = f.read()
        C = WR(buf)
        C.TOFROM = ["TEST", "ta", "to"] #To, From1, From2...
        C.process(m=1)
        if (C.log):
            print (C.log)
            buf = bytes(C.content, 'latin-1')       
            with open(txt, 'wb') as f:
                f.write(buf)
        


