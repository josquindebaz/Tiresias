# -*- coding: utf-8 -*-
# Author Josquin Debaz
# GPL 3
import os
import re


class PrcFilter(object):
    def __init__(self):
        self.list_txt = []
        self.theme = []
        self.score = 0
        self.dep = 0
        self.corpus = {}
        self.anticorpus = {}
        
    def openPRC(self, path):
        with open(path, 'r') as f:
            b = f.readlines()
        self.list_txt = [txt[:-1] for txt in b[6:-1]]
        self.prc_param = b[1:6]

    def eval_corpus(self):
        for txt in self.list_txt:
            if os.path.isfile(txt):
                with open(txt, "r") as f:
                    content = f.read()
                ev = self.eval_theme(content)
                if (ev[1][0] >= self.score) and (ev[1][1] >= self.dep):
                    self.corpus[txt] = ev
                else:
                    self.anticorpus[txt] = ev
            else:
                self.anticorpus[txt] = False
                
    def eval_theme(self, text):
        if len(self.theme) > 1:
            tests = []
            testsResults = ""

            for item in self.theme:
                #punctuation Before or after
                BeAf = "[\s\.,;!\?\"']"
                index = "(^|(%s))(%s)((%s)|$)" % (BeAf, item, BeAf) 
                index = re.compile(index)

                test = len(index.findall(text))
                if test > 0 :
                    testsResults += "[%s:%d]" % (item, test)
                    tests.append(test)
                    
            evaluation = [sum(tests), sum(1 for x in tests if x > 0)]
            return testsResults, evaluation

    def save_PRC(self, path, txts):
        lines = ["projet0005\n"]
        lines.extend(self.prc_param)
        lines.extend([txt+"\n" for txt in txts])
        lines.append("ENDFILE")
        with open(path, "w") as f:
            f.writelines(lines)
        
        

if __name__ == '__main__':
    test = PrcFilter()
    test.openPRC("C:/corpus/atmosphere/socle.prc")
    test.theme=[
        "test",
        "jamais"
        ]
    test.score = 4
    test.dep = 2
    test.eval_corpus()
    for t in test.corpus.items():
        print (t)
    test.save_PRC("test.prc", test.corpus.keys())   

    

    
