import tkinter as tk
from tkinter import ttk

import glob
import re
import os
from pathlib import Path

from mods.europresse import *
from mods.supports import Publi

class ViewEuropresse():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="Europresse",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        corpus_path_windows = "C:\corpus"
        home = str(Path.home())
        corpus_path_unix = "%s/.wine/drive_c/corpus"%home
        if os.path.isdir(corpus_path_windows):
            self.initdir = corpus_path_windows
        elif os.path.isdir(corpus_path_unix):
            self.initdir = corpus_path_unix
        else:
            self.initdir = "."

        #FrameDir
        FrameDir = tk.Frame(self.parent)
        FrameDir.pack(anchor=tk.W)

        bnDir = tk.Button(FrameDir,
                          text="Select .html Europresse file directory",
                          command=self.sel_dir_html)
        bnDir.pack(side=tk.LEFT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(FrameDir, width=52,
            textvariable=self.choosenDir)
        dir_entry.pack(side=tk.LEFT)

        bnScan = tk.Button(FrameDir, text="Read Directory",
                           command=self.get_html_list)
        bnScan.pack(side=tk.LEFT)        


        #Central Frame
        FrTemp = tk.PanedWindow(self.parent)
        FrTemp.pack(anchor=tk.W)

        #Europresse Files
        FrEurF = tk.Frame(FrTemp)
        FrEurF.pack(side=tk.LEFT, anchor=tk.N)
        self.htm_list=tk.Listbox(FrEurF, width=50,
                                 selectmode=tk.EXTENDED)
        self.htm_list.pack()
        bn_test_f = tk.Button(FrEurF,
                              text="Analyse selected files",
                              command=self.analyse)
        bn_test_f.pack(anchor=tk.W)

        #Unknow sources
        Fr_U = tk.LabelFrame(FrEurF, text="Unknown Sources", borderwidth=2,)
        Fr_U.pack(side=tk.LEFT, anchor=tk.N)
        self.unknown_list=tk.Listbox(Fr_U, width=50)
        self.unknown_list.pack()
        self.unknown_list.bind("<<ListboxSelect>>", self.memoUnknown)
        self.memory_selected_unknown = None

        self.CbS = ttk.Combobox(Fr_U)
        self.CbS.pack(anchor=tk.W, fill=tk.X)
        self.CbS.bind("<<ComboboxSelected>>", self.CbSSel)

        UP1 = tk.PanedWindow(Fr_U)
        UP1.pack(anchor=tk.W, fill=tk.X)
        lab_U_pubname = tk.Label(UP1, text="Name")
        lab_U_pubname.pack(side=tk.LEFT)
        self.U_pubname = tk.Entry(UP1)
        self.U_pubname.pack(fill=tk.X)        
        UP2 = tk.PanedWindow(Fr_U)
        UP2.pack(anchor=tk.W, fill=tk.X)
        lab_U_type = tk.Label(UP2, text="Type")
        lab_U_type.pack(side=tk.LEFT)
        self.U_type = tk.Entry(UP2)
        self.U_type.pack(fill=tk.X)
        UP3 = tk.PanedWindow(Fr_U)
        UP3.pack(anchor=tk.W, fill=tk.X)
        lab_U_abr = tk.Label(UP3, text="Abrv")
        lab_U_abr.pack(side=tk.LEFT)
        self.U_abr = tk.Entry(UP3)
        self.U_abr.pack(fill=tk.X)
        
        bn_U_w = tk.Button(Fr_U, text="Add to support.publi",
            command=self.add_support)
        bn_U_w.pack()

        #article list        
        Fr_art = tk.LabelFrame(FrTemp, text="Found articles", borderwidth=2)
        Fr_art.pack()
        self.art_list=tk.Listbox(Fr_art, width=100, height=30,
                                 selectmode=tk.EXTENDED)
        self.art_list.pack(side=tk.LEFT)
        SB_art = tk.Scrollbar(Fr_art)
        SB_art.pack(side=tk.RIGHT, fill=tk.Y)
        SB_art.configure(command=self.art_list.yview)
        self.art_list.configure(yscrollcommand=SB_art.set)

        WP2 = tk.PanedWindow(FrTemp)
        WP2.pack(anchor=tk.W, fill=tk.BOTH)
        bnDirW = tk.Button(WP2,
                           text="Select Prospero file directory",
                           command=self.sel_dir_w)
        bnDirW.pack(side=tk.LEFT)
        self.choosenDir_w = tk.StringVar()
        dir_w_entry = tk.Entry(WP2, width=52,
            textvariable=self.choosenDir_w)
        dir_w_entry.pack(fill=tk.X)

        self.CleaningVal= tk.BooleanVar()
        Bn_Cleaning = tk.Checkbutton(FrTemp,
                        text="clean texts",
                        variable=self.CleaningVal)
        Bn_Cleaning.select()
        Bn_Cleaning.pack(side=tk.LEFT)
        
        bn_process_art = tk.Button(FrTemp,
                                   text="Write selected articles",
                                   command=self.write_articles)
        bn_process_art.pack(side=tk.LEFT, padx=10)
        

        self.progressbar = ttk.Progressbar(self.parent, mode='determinate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        #Log Frame
        FrLog = tk.Frame(self.parent)
        FrLog.pack(fill=tk.X)
        self.log = tk.scrolledtext.ScrolledText(FrLog,
                            height=10, bg="black", fg="orange")
        self.log.pack(fill=tk.X)
        
    def memoUnknown(self, callback):
        self.memory_selected_unknown = self.unknown_list.curselection()

    def CbSSel(self, callback):
        self.reset_Supports()
        index = self.CbS.current()
        if(index):
            values = self.knownSources[index].split("; ")
            self.U_pubname.insert(0, values[0])
            self.U_type.insert(0, values[1])
            self.U_abr.insert(0, values[2])

        if (self.memory_selected_unknown):
            self.unknown_list.selection_set(self.memory_selected_unknown)

    def add_support(self):
        i = self.unknown_list.curselection()
        if (i):
            s = self.unknown_list.get(i)
            n = self.U_pubname.get()
            t = self.U_type.get() 
            a = self.U_abr.get() 
            self.log.insert(1.0, 
                "Adding to support.publi [%s] as %s; %s; %s\n" % (s, n, t, a))
            self.Supports.add(s, n, t, a)
            self.Supports.write()
            self.populateSupports()
            self.unknown_list.delete(i)

    def sel_dir_html(self):
        self.choosenDir.set("")
        self.reset_lists()

        self.htmldirectory = tk.filedialog.askdirectory(title="Choose directory")
        self.choosenDir.set(self.htmldirectory)
        self.get_html_list()
        self.log.insert(1.0,
                "Found %d .html file(s) in %s\n" %(len(self.list_html),
                                                   self.htmldirectory))

    def reset_lists(self):
        self.unknown_list.delete(0, 'end')
        self.art_list.delete(0, 'end')        

    def get_html_list(self):
        self.reset_lists()
        self.htm_list.delete(0, 'end')
        
        directory = self.choosenDir.get()
        if (directory):
            rule = re.compile(".*\.htm.", re.IGNORECASE)
            self.list_html = [f for f in os.listdir(directory) if
                rule.match(f)]
            [self.htm_list.insert("end",
                    os.path.split(item)[1]) for item in self.list_html]
            self.htm_list.select_set(0, "end")

    def reset_Supports(self): 
        self.U_pubname.delete(0, 'end')
        self.U_type.delete(0, 'end')
        self.U_abr.delete(0, 'end')

    def populateSupports(self):
        self.reset_Supports()
        self.knownSources = ["Known sources"]
        self.knownSources.extend( sorted(["%s; %s; %s" %(k, 
            self.Supports.sources[k]['type'], self.Supports.sources[k]['abr']) 
            for k in self.Supports.sources]) )
        self.CbS['values'] = (self.knownSources)
        self.CbS.current(0)

    def analyse(self):
        self.reset_lists()

        self.Supports = Publi()
        self.populateSupports()
            
        unknowns = []
        self.articles_list = []
        for c in self.htm_list.curselection():
            f = self.list_html[c]
            self.log.insert(1.0, 'Analysing %s\n'%f)
            try:
                p = ParseHtml(os.path.join(self.htmldirectory, f))
                for a in p.parsed_articles:
                    if a not in self.articles_list:
                        self.articles_list.append(a)
                    if (a['source'] not in self.Supports.codex.keys() and
                        a['source'] not in unknowns):
                        unknowns.append(a['source'])
            except:
                self.log.insert(1.0, 'Analyse problem\n')


        self.log.insert(1.0, 'Found %d compatible \
articles and %d unknown source(s)\n'%(len(self.articles_list), len(unknowns)))
        [self.art_list.insert("end", "%s %s %s"%\
            (a['source'], a['date'], a['title'])) for a in self.articles_list]
        [self.unknown_list.insert("end", u) for u in unknowns]

        self.art_list.select_set(0, "end")

    def sel_dir_w(self):
        memory_selected_articles = self.art_list.curselection()
        self.choosenDir_w.set("")
        directory = tk.filedialog.askdirectory(title="Choose directory",
                           initialdir=self.initdir)
        self.choosenDir_w.set(directory)
        for a in memory_selected_articles:
            self.art_list.selection_set(a)
                  
    def write_articles(self):
        articles = self.art_list.curselection()
        if len(articles):
            self.progressbar['value'] = 0
            self.progressbar['maximum'] =  len(articles)
            directory = self.choosenDir_w.get()
            if not (directory):
                self.log.insert(1.0, 'No directory for Prospero files\n')
            else:
                for c, index in enumerate(articles):
                    article =  self.articles_list[index]
                    f = ProcessArticle(article, directory,
                                       self.CleaningVal.get())
                    self.log.insert(1.0, 'Writing %s\n'%f.filename)
                    self.progressbar['value'] = c+1

                    
