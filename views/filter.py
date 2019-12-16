import tkinter as tk
from tkinter import ttk
from tkinter import filedialog 
from tkinter.scrolledtext import ScrolledText
import os
from pathlib import Path

from mods.prcfilter import PrcFilter

class ViewFilter():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="Project Filter",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        self.list_txt = []
        self.list_txt_c = []
        self.prc = []

        corpus_path_windows = "C:\corpus"
        home = str(Path.home())
        corpus_path_unix = "%s/.wine/drive_c/corpus"%home
        if os.path.isdir(corpus_path_windows):
            self.initdir = corpus_path_windows
        elif os.path.isdir(corpus_path_unix):
            self.initdir = corpus_path_unix
        else:
            self.initdir = "."
        
        #Frame project
        Fr1 = tk.Frame(self.parent)
        Fr1.pack(anchor=tk.W)

        bnPrc = tk.Button(Fr1, text=u"Select project",
            command=self.sel_PRC)
        bnPrc.pack(side=tk.LEFT)

        self.choosenPRC = tk.StringVar()
        PRC_entry = tk.Entry(Fr1, width=62,
            textvariable=self.choosenPRC)
        PRC_entry.pack(side=tk.LEFT)

        bnDir = tk.Button(Fr1, text=u"Select directory", 
            command=self.sel_dir)
        bnDir.pack(side=tk.LEFT)
        
        #Frame corpus/anticorpus
        Fr2 = tk.LabelFrame(self.parent, 
            text="corpus/anticorpus", borderwidth=1)
        Fr2.pack(fill=tk.X)
        self.Corpus_list = ScrolledText(Fr2)
        self.Corpus_list.pack(side=tk.LEFT)
        self.Acorpus_list = ScrolledText(Fr2)
        self.Acorpus_list.pack(side=tk.LEFT)

        self.progressbar = ttk.Progressbar(self.parent, mode='determinate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        #Frame theme, parameters, logs
        Fr3 = tk.Frame(self.parent, padx =10, pady=10)
        Fr3.pack(fill=tk.X)
        
        fr31 = tk.LabelFrame(Fr3, text="theme", padx=10)
        fr31.pack(anchor=tk.N, side=tk.LEFT)
        self.L_presents = tk.Listbox(fr31)
        self.L_presents.pack(fill=tk.X)
        self.L_presents.insert(0, "toujours")
        self.L_presents.insert(0, "jamais")
        self.L_presents.insert(0, "parfois")
        bn_del = tk.Button(fr31, text=u"del", command=self.theme_remove)
        bn_del.pack(anchor=tk.W)
        P312 = tk.PanedWindow(fr31)
        P312.pack()
        self.w_add_Entry = tk.Entry(P312)
        self.w_add_Entry.pack(side=tk.LEFT)
        self.bn_add = tk.Button(P312, text=u"add",
                           command=self.theme_add)
        self.bn_add.pack()
##        bn_sav = tk.Button(fr31, text=u"save theme")
##        bn_sav.pack()

        fr32 = tk.Frame(Fr3, padx=10)
        fr32.pack(anchor=tk.N, side=tk.LEFT)
        P321 = tk.PanedWindow(fr32)
        P321.pack(anchor=tk.W)
        lb_sc = tk.Label(P321, text=u"total score >=")
        lb_sc.pack(side=tk.LEFT)
        self.entry_Score = tk.Entry(P321)
        self.entry_Score.pack()
        self.entry_Score.insert(0, "4")
        P322 = tk.PanedWindow(fr32)
        P322.pack()
        lb_dep = tk.Label(P322,text="components >=")
        lb_dep.pack(side=tk.LEFT)
        self.entry_Dep = tk.Entry(P322)
        self.entry_Dep.pack()
        self.entry_Dep.insert(0, "2")
        
        bn_proc = tk.Button(fr32, text=u"theme evaluation",
                    command=self.evaluation)
        bn_proc.pack(anchor=tk.W)
        
        P323 = tk.PanedWindow(fr32)
        P323.pack(pady=10, anchor=tk.W)
        bn_save_corpus = tk.Button(P323, text="save corpus",
                                   command=self.save_corpus)
        bn_save_corpus.pack(side=tk.LEFT)
        bn_save_anticorpus = tk.Button(P323, text="save anticorpus",
                                   command=self.save_acorpus)
        bn_save_anticorpus.pack()
        
        fr33 = tk.Frame(Fr3)
        fr33.pack(side=tk.RIGHT)
        self.result = ScrolledText(fr33, height=15, bg="black", fg="orange")
        self.result.pack()
         
        
    def sel_PRC(self):
        self.choosenPRC.set("")
        p = filedialog.askopenfilename(
            filetypes=[("project file","*.prc")],
            title='Select a project',
            initialdir=self.initdir)
        self.choosenPRC.set(p)

        self.result.delete(1.0, "end")

        with open(p, 'r', encoding='iso-8859-1') as f:
            self.prc = f.readlines()
            self.list_txt = [l[:-1] for l in self.prc[6:-1]]

        for txt in self.list_txt:
            self.Corpus_list.insert("end", u"%s\n"%txt)
        self.result.insert(1.0,
                u"Found %d .txt(s) in %s\n"%(len(self.list_txt), p))

        self.Acorpus_list.delete(1.0, "end")
        self.progressbar['value'] = 0
        self.progressbar['maximum'] =  len(self.list_txt)

    def sel_dir(self):
        directory = filedialog.askdirectory(title="Choose directory",
                                               initialdir=self.initdir)
        self.choosenPRC.set(directory)
        self.result.delete(1.0, "end")

        self.list_txt = []
        for root, rep, files in os.walk(directory):
            self.list_txt.extend([os.path.join(root, name) 
                for name in files 
                if os.path.splitext(name)[1] in [".txt", ".TXT"]
                ])

        for txt in self.list_txt:
            self.Corpus_list.insert("end", u"%s\n"%txt)
        self.result.insert(1.0,
                u"Found %d .txt(s) in %s\n"%(len(self.list_txt), directory))

    def theme_add(self):
        item = self.w_add_Entry.get()
        if item != "":
            if (item in self.L_presents.get(0, 'end')):
                self.result.insert(1.0, u"%s already in theme\n"%item)
            else:
                self.L_presents.insert("end", u"%s"%item)
                self.result.insert(1.0, u"[%s] added to theme\n"%item)
                self.w_add_Entry.delete(0, "end")

    def theme_remove(self):
        selected = self.L_presents.curselection()
        if (selected):
            item = self.L_presents.get(selected)
            self.L_presents.delete(selected)
            self.result.insert(1.0, u"%s removed from theme\n"%item)

    def evaluation(self):
        self.result.delete(1.0, "end")
        if not len(self.list_txt):
            self.result.insert(1.0, u"no txt to evaluate\n")
        theme = self.L_presents.get(0, "end")
        if not len(theme):
            self.result.insert(1.0, u"no theme to evaluate\n")
        if len(self.list_txt) and len(theme):
            self.list_txt_c = []
            self.list_txt_ac = []
            self.list_txt_absent = []
            self.Corpus_list.delete(1.0, "end")
            self.Acorpus_list.delete(1.0, "end")
            Eval = PrcFilter()
            Eval.theme = theme
            Eval.score = int(self.entry_Score.get())
            Eval.dep = int(self.entry_Dep.get())
            
            for c, txt in enumerate(self.list_txt):
                self.progressbar['value'] = c+1
                self.parent.update()
                if os.path.isfile(txt):
                    with open(txt, "r", encoding='iso-8859-1') as f:
                        b = f.read()
                    ev = Eval.eval_theme(b)
                    if ((ev[1][0] >= Eval.score) and (ev[1][1] >= Eval.dep)):
                        self.Corpus_list.insert("end", u"%s %s\n"%(txt, ev[0]))
                        self.list_txt_c.append(txt)
                    else:
                        self.Acorpus_list.insert("end", u"%s %s\n"%(txt, ev[0]))
                        self.list_txt_ac.append(txt)
                else:
                    self.result.insert(1.0, "%s: no such file\n"%txt)
                    self.list_txt_absent.append(txt)
                
            self.result.insert(1.0, "%d text(s) positive, %d negative, %d file(s) not found\n"\
                               % (len(self.list_txt_c),
                len(self.list_txt_ac), len(self.list_txt_absent)))

    def save_corpus(self):
        if len(self.list_txt_c):
            self.save_PRC(self.list_txt_c, "pos")
        
    def save_acorpus(self):
        if len(self.list_txt_c):
            self.save_PRC(self.list_txt_ac, "neg")

    def save_PRC(self, list_txt, suf):
        if len(list_txt):
            p = self.choosenPRC.get()
            if os.path.splitext(p)[1] not in [".prc", ".PRC"]:
                p = "%s.prc" % os.path.split(p)[1]
                
            if (self.prc):
                lines = self.prc[:6]
            else:
                lines = ["projet0005\r\n", 
                    "\r\n", "\r\n", "\r\n", "\r\n", "\r\n"]
            lines.extend([txt+"\r\n" for txt in list_txt])
            lines.append("ENDFILE")
            fichier = filedialog.asksaveasfile(mode='w',
                        filetypes=[("","*.prc")],
                        defaultextension = ".prc",
                        initialdir=self.initdir,
                        initialfile="%s_filtered_%s%s"%(p[:-4], suf, p[-4:]))
            fichier.writelines(lines)
            fichier.close()
