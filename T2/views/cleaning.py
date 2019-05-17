import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from threading import Thread

from mod.cleaning import list_files
from mod.cleaning import Cleaner

class ViewCleaning():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(parent, text="Character Cleaning",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        #Frame directory
        Fr1 = tk.Frame(parent)
        Fr1.pack(anchor=tk.W)

        bnDir = tk.Button(Fr1, text=u"Select directory",
            command=self.sel_dir)
        bnDir.pack(side=tk.LEFT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(Fr1, width=52,
            textvariable=self.choosenDir)
        self.choosenDir.set(u"C:\corpus")
        dir_entry.pack(side=tk.LEFT)

        self.Recursive = tk.BooleanVar()
        bnRecursive = tk.Checkbutton(Fr1, 
            text='recursive', var=self.Recursive)
        bnRecursive.select()
        bnRecursive.pack(side=tk.LEFT)

        self.test = tk.BooleanVar()
        bn_test = tk.Checkbutton(Fr1, 
            text='test only', var=self.test)
        #bn_test.select()
        bn_test.pack(side=tk.LEFT)

        bnAction = tk.Button(Fr1, text=u"Process cleaning",
                             command=self._t_Action)
        bnAction.pack(side=tk.LEFT)

        #Frame Options
        Fr2 = tk.LabelFrame(parent, 
            text="Options", borderwidth=1)
        Fr2.pack()
        self.utf = tk.BooleanVar()
        bn_utf = tk.Checkbutton(Fr2,
            text='Utf8 to Latin1', var=self.utf)
        bn_utf.select()
        bn_utf.pack(side=tk.LEFT)        
        self.ascii = tk.BooleanVar()
        bn_ascii = tk.Checkbutton(Fr2,
            text='ascii', var=self.ascii)
        bn_ascii.select()
        bn_ascii.pack(side=tk.LEFT)
        self.char_replace = tk.BooleanVar()
        bn_char_replace = tk.Checkbutton(Fr2,
            text='special chars', var=self.char_replace)
        bn_char_replace.select()
        bn_char_replace.pack(side=tk.LEFT)  
        self.split = tk.BooleanVar()
        bn_split = tk.Checkbutton(Fr2,
            text='splitted numbers', var=self.split)
        bn_split.select()
        bn_split.pack(side=tk.LEFT)  
        self.hyphens = tk.BooleanVar()
        bn_hyphens = tk.Checkbutton(Fr2,
            text='hyphenations', var=self.hyphens)
        bn_hyphens.select()
        bn_hyphens.pack(side=tk.LEFT)  
        self.html_tags = tk.BooleanVar()
        bn_html_tags = tk.Checkbutton(Fr2,
            text='html tags', var=self.html_tags)
        bn_html_tags.select()
        bn_html_tags.pack(side=tk.LEFT)
        self.parity_marks = tk.BooleanVar()
        bn_parity_marks = tk.Checkbutton(Fr2,
            text='parity marks', var=self.parity_marks)
        bn_parity_marks.select()
        bn_parity_marks.pack(side=tk.LEFT)
        self.dashs = tk.BooleanVar()
        bn_dashs = tk.Checkbutton(Fr2,
            text='dashes', var=self.dashs)
        bn_dashs.select()
        bn_dashs.pack(side=tk.LEFT)
        self.footnotes = tk.BooleanVar()
        bn_footnotes = tk.Checkbutton(Fr2,
            text='footnotes', var=self.footnotes)
        bn_footnotes.select()
        bn_footnotes.pack(side=tk.LEFT)

        #Progress bar
        self.progressbar = ttk.Progressbar(parent)
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        #Results
        self.result = ScrolledText(parent, bg="black", fg="orange")
        self.result.pack(fill=tk.X)

    def _t_Action(self):
        self.query = None
        self.result.delete(1.0, "end")
        self.result.insert("end", "Listing text files\n")
        self.parent.update()

        self._thread = Thread(target=self.list_txt)
        self._thread.start()
        while(self.query == None):
            self.parent.update()
        self._thread = None

        if len(self.query) > 0:
            self.result.insert("end", u"%d file(s) found\n"%len(self.query))
            if (self.test.get()):
                self.result.insert("end", u"only testing\n")
            else:
                self.result.insert("end",
                    u"Processing text cleaning\n")
            self.progressbar['mode'] = 'determinate'
            self.progressbar['maximum'] =  len(self.query)
            n = 0
            for c, txt in enumerate(self.query):
                n += self.clean_txt(txt)
                self.progressbar['value'] = c
                self.parent.update()
                self.result.see("end")

            self.result.insert("end", u"%d file(s) cleaned\n"%n)

        else:
            self.result.insert("end", u"Nothing found\n")
            

    def clean_txt(self, txt):
        with open(txt, 'rb') as f:
            b = f.read()

        options = ""
        if self.utf.get():
            options += "u"      
        if self.ascii.get() :
            options += "a"
        if self.char_replace.get():
            options += "c"
        if self.split.get():
            options += "s"
        if self.hyphens.get():
            options += "h"
        if self.html_tags.get():
            options += "t"      
        if self.parity_marks.get():
            options += "p"
        if self.dashs.get():
            options += "d"
        if self.footnotes.get():
            options += "f"

        c = Cleaner(b, options)

        if not set([x for x in c.log.values()]) == set([0]):
            """if something has to be corrected"""
            self.result.insert("end", "%s  "%txt)
            self.result.insert("end",
                "%s\n"%"; ".join(["%s: %d"%(x, y)
                                  for x, y in c.log.items() if y != 0]))
            if (not self.test.get()):
                """if not test mode"""
                buf = bytes(c.content, 'latin-1')   
                with open(txt, 'wb') as f:
                    f.write(buf)
            return 1
        else:
            return 0
                   

    def list_txt(self):
        self.progressbar['mode'] = 'indeterminate'
        self.progressbar['maximum'] = 100
        self.progressbar.start(50)
        self.parent.update()
        rep = self.choosenDir.get()
        if rep == '':
            self.result.insert("end", "No directory selected")
        else:
            self.query = list_files(rep=rep,
                    recursive=self.Recursive.get())
        self.progressbar.stop()

        
    def sel_dir(self):
        self.choosenDir.set("")
        self.result.delete(1.0, "end")
        self.progressbar['value'] = 0
        dir = filedialog.askdirectory(title=u"Choose directory",
            initialdir="C:\corpus")
        self.choosenDir.set(dir)

