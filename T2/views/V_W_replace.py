import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from threading import Thread

from mod.word_replace import *

import json
import datetime

class V_WR():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="Replace words",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        #Frame 1
        Fr1 = tk.Frame(self.parent)
        Fr1.pack(anchor=tk.W)

        bnDir = tk.Button(Fr1, text="Select directory",
            command=self.sel_dir)
        bnDir.pack(side=tk.LEFT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(Fr1, width=52,
            textvariable=self.choosenDir)
        self.choosenDir.set("C:\\corpus\\test")
        dir_entry.pack(side=tk.LEFT)

        self.Recursive = tk.BooleanVar()
        bnRecursive = tk.Checkbutton(Fr1, 
            text='recursive', var=self.Recursive)
        bnRecursive.select()
        bnRecursive.pack(side=tk.LEFT)

        self.test = tk.BooleanVar()
        bn_test = tk.Checkbutton(Fr1, 
            text='test only', var=self.test)
        bn_test.select()
        bn_test.pack(side=tk.LEFT)

        #Frame 2
        Fr2 = tk.PanedWindow(self.parent)
        Fr2.pack(anchor=tk.W)
        
        Fr21 = tk.LabelFrame(Fr2, 
            text="From patterns", padx=10)
        Fr21.pack(anchor=tk.N, side=tk.LEFT)
        self.ListFrom = tk.Listbox(Fr21)
        self.ListFrom.pack(fill=tk.X)
        bn_del = tk.Button(Fr21, text=u"del",
                           command=self.from_remove)
        bn_del.pack(anchor=tk.W)
        P21 = tk.PanedWindow(Fr21)
        P21.pack()
        self.w_add_Entry = tk.Entry(P21)
        self.w_add_Entry.pack(side=tk.LEFT)
        self.bn_add = tk.Button(P21, text=u"add",
                           command=self.from_add)
        self.bn_add.pack()
        self.Marks = tk.BooleanVar()
        bnM = tk.Checkbutton(Fr21, padx=30,
            text='with marks', var=self.Marks)
        bnM.select()
        bnM.pack()

        Fr22 = tk.LabelFrame(Fr2, 
            text="To", padx=10)
        Fr22.pack(anchor=tk.N, side=tk.LEFT)
        
        self.EntryTo = tk.Entry(Fr22, width=30)
        self.EntryTo.pack()
        
        bn_proc = tk.Button(Fr22, text="Replace",
                    command=self.process)
        bn_proc.pack(pady=10)

        Fr23 = tk.LabelFrame(Fr2, 
            text="History", padx=10)
        Fr23.pack()
        self.history = tk.Listbox(Fr23)
        self.history.pack()
        self.history_populate()
        recallBn = tk.Button(Fr23, text='Recall',
            command=self.Recall)
        recallBn.pack()
        
        self.progressbar = ttk.Progressbar(self.parent,
            mode='determinate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        frlogs = tk.Frame(self.parent)
        frlogs.pack(fill=tk.X)
        self.result = ScrolledText(frlogs, height=15, bg="black", fg="orange")
        self.result.pack()        

    def sel_dir(self):
        self.choosenDir.set("")
        self.result.delete(1.0, "end")
        self.progressbar['value'] = 0
        dir = filedialog.askdirectory(title="Choose directory",
            initialdir="C:\corpus")
        self.choosenDir.set(dir)

    def from_remove(self):
        selected = self.ListFrom.curselection()
        if (selected):
            item = self.ListFrom.get(selected)
            self.ListFrom.delete(selected)
            #self.result.insert(1.0, "%s removed from From list\n"%item)
            
    def from_add(self):
        item = self.w_add_Entry.get()
        if item != "":
            if (item in self.ListFrom.get(0, 'end')):
                self.result.insert(1.0, u"%s already in From list\n"%item)
            else:
                self.ListFrom.insert("end", u"%s"%item)
                #self.result.insert(1.0, "[%s] added to From list\n"%item)
                self.w_add_Entry.delete(0, "end")

    def history_populate(self):
        try:
            with open("param.json", 'r') as F:
                self.config = json.load(F)
            self.history.delete(0, "end")
            for date in sorted(self.config['WR']['H'].keys()):
                self.history.insert(0, self.config['WR']['H'][date])
        except:
            #print('pb loading history')
            pass
        
    def history_add(self, value):
        if not hasattr(self, 'config'):
            self.config = {'WR': {'H': {}}}
        exists = [d for d, v in self.config['WR']['H'].items()
                    if (v  == value)] 
        if (exists):
            del(self.config['WR']['H'][exists[0]])
        self.config['WR']['H'][str(datetime.datetime.now())] = value
        try:
            with open("param.json", 'w') as f:
                json.dump(self.config, f)
        except:
            print('pb saving history')
        self.history_populate()

    def Recall(self): 
        selected = self.history.curselection()
        if (selected):
            rec = self.history.get(selected)
            self.ListFrom.delete(0, "end")
            self.EntryTo.delete(0, "end")
            self.EntryTo.insert(0, rec[0])
            for f in rec[1:]:
                self.ListFrom.insert("end", f)
 
    def process(self):
        folder = self.choosenDir.get()
        From = self.ListFrom.get(0, 'end')
        To = self.EntryTo.get()
        if (From):
            if To in From:
                self.result.insert(1.0,
                    "Error: [%s] is in From list\n"%To)
            else:
                ToFrom = [To]
                ToFrom.extend(From)
                self.history_add(ToFrom)

                text_list = list_files(folder, recursive=self.Recursive.get())
                self.result.insert(1.0, "Found %d .txt file(s)\n"%len(text_list))
                self.progressbar['value'] = 0
                self.progressbar['maximum'] =  len(text_list)
                cpt = 0

                P = WR()
                P.set_motif(ToFrom, m=self.Marks.get())
                
                for c, txt in enumerate(text_list):
                    self.progressbar['value'] = c+1
                    with open(txt, 'rb') as f:
                        buf = f.read()
                    P.set_content(buf)
                    P.process()
                    if (P.log):
                        if not self.test.get():
                            buf = bytes(P.content, 'latin-1')
                            with open(txt, 'wb') as f:
                                f.write(buf)
                            cpt +=1
                        self.result.insert(1.0,
                            "%d match(es) in %s\n"%(P.log, txt))
                    self.parent.update()
                self.result.insert(1.0, "%d file(s) edited\n"%cpt)
