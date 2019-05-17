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

class Replacer(object):
    def __init__(self):
        self.log = None
        self.content = None
        self.motif = None
        self.repl = None

    def set_content(self, content):
        self.content = content.decode('latin-1') #byte to str

    def set_motif(self, tofrom, m=True):
        if (m):
            marks = '\s"'+re.escape(".,;!?':¿(){}[]-")
        else:
            marks = "\s"
        From = [re.escape(i) for i in tofrom[1:]]
        From = "(^|[%s])(%s)([%s]|$)" % (marks,
                                        '|'.join(From), marks)
        self.motif = re.compile(From)
        self.repl = r"\g<1>%s\g<3>"%tofrom[0]

    def process(self):  
        self.log = 0
        while(self.motif.search(self.content)):
            self.content = self.motif.sub(self.repl, self.content, 1)
            self.log += 1
       
              
    
if __name__ == '__main__':
    list_TXT = list_files(".")
    for txt in list_TXT:
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


        if (C.log):
            print (C.log)
            buf = bytes(C.content, 'latin-1')
            print(str(buf))
            #with open(txt, 'wb') as f:
            #    f.write(buf)
        


