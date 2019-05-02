import tkinter as tk

import glob
import os

from mod.Europresse import *
from mod.supports import publi

class V_E():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="Europresse",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

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
        self.unknown_list=tk.Listbox(Fr_U, width=40)
        self.unknown_list.pack()

##        UP1 = tk.PanedWindow(Fr_U)
##        UP1.pack(anchor=tk.W, fill=tk.X)
##        lab_U_pubname = tk.Label(UP1, text="Name")
##        lab_U_pubname.pack(side=tk.LEFT)
##        U_pubname = tk.Entry(UP1)
##        U_pubname.pack(fill=tk.X)        
##        UP2 = tk.PanedWindow(Fr_U)
##        UP2.pack(anchor=tk.W, fill=tk.X)
##        lab_U_type = tk.Label(UP2, text="Type")
##        lab_U_type.pack(side=tk.LEFT)
##        U_type = tk.Entry(UP2)
##        U_type.pack(fill=tk.X)
##        UP3 = tk.PanedWindow(Fr_U)
##        UP3.pack(anchor=tk.W, fill=tk.X)
##        lab_U_abr = tk.Label(UP3, text="Abrv")
##        lab_U_abr.pack(side=tk.LEFT)
##        U_abr = tk.Entry(UP3)
##        U_abr.pack(fill=tk.X)
##        
##        bn_U_w = tk.Button(Fr_U, text="Save",)
##        bn_U_w.pack()

##        #FIXME bof
##        Supports = supports()
##        l = [Supports.D[a]['source'] for a in Supports.D.keys()]
##        optionList = (l)
##        v = tk.StringVar()
##        v.set(optionList[0])
##        om = tk.OptionMenu(Fr_U, v, *optionList)
##        om.pack()

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
        

        #Log Frame
        FrLog = tk.Frame(self.parent)
        FrLog.pack(fill=tk.X)
        #TODO for other direct tk too
        self.log = tk.scrolledtext.ScrolledText(FrLog,
                            height=10, bg="black", fg="orange")
        self.log.pack(fill=tk.X)
        
    def sel_dir_html(self):
        self.choosenDir.set("")
        self.reset_lists()

        #TODO for other direct tk too
        directory = tk.filedialog.askdirectory(title="Choose directory")
        self.choosenDir.set(directory)
        self.get_html_list()
        self.log.insert(1.0,
                "Found %d .html file(s) in %s\n" %(len(self.list_html),
                                                   directory))
    def reset_lists(self):
        self.unknown_list.delete(0, 'end')
        self.art_list.delete(0, 'end')        

    def get_html_list(self):
        self.reset_lists()
        self.htm_list.delete(0, 'end')
        
        directory = self.choosenDir.get()
        if (directory):
            self.list_html = glob.glob("%s/*.htm*"%directory)
            [self.htm_list.insert("end",
                    os.path.split(item)[1]) for item in self.list_html]

    def analyse(self):
        self.reset_lists()

        Supports = publi()
        unknowns = []
        self.articles_list = []
        for c in self.htm_list.curselection():
            f = self.list_html[c]
            self.log.insert(1.0, 'Analysing %s\n'%f)
            try:
                p = parse_html(f)
                for a in p.parsed_articles:
                    if a not in self.articles_list:
                        self.articles_list.append(a)
                    if (a['source'] not in Supports.codex.keys() and
                        a['source'] not in unknowns):
                        unknowns.append(a['source'])
            except:
                self.log.insert(1.0, 'Analyse problem\n')


        self.log.insert(1.0, 'Found %d compatible \
articles and %d unknown source(s)\n'%(len(self.articles_list), len(unknowns)))
        [self.art_list.insert("end", "%s %s %s"%\
            (a['source'], a['date'], a['title'])) for a in self.articles_list]

        [self.unknown_list.insert("end", u) for u in unknowns]


    def sel_dir_w(self):
        self.choosenDir_w.set("")
        directory = tk.filedialog.askdirectory(title="Choose directory",
                                               initialdir="C:\corpus")
        self.choosenDir_w.set(directory)
                  
    def write_articles(self):
        articles = self.art_list.curselection()
        if len(articles):
            directory = self.choosenDir_w.get()
            if not (directory):
                self.log.insert(1.0, 'No directory for Prospero files\n')
            else:
                for index in articles:
                    a =  self.articles_list[index]
                    cl = self.CleaningVal.get()
                    f = Process_article(a, directory, cl)
                    self.log.insert(1.0, 'Writing %s\n'%f.filename)

                    
