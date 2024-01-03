import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import os
from pathlib import Path

from mod.prcfilter import PrcFilter


class ViewFilter:
    def __init__(self, parent):
        self.list_txt_absent = None
        self.list_txt_ac = None
        self.parent = parent
        window_title = tk.Label(self.parent,
                                text="Project Filter",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        self.list_txt = []
        self.list_txt_c = []
        self.prc = []

        corpus_path_windows = r"C:\corpus"
        try:
            home = str(Path.home())
            corpus_path_unix = "%s/.wine/drive_c/corpus" % home
        except:
            corpus_path_unix = "/home"
        if os.path.isdir(corpus_path_windows):
            self.init_dir = corpus_path_windows
        elif os.path.isdir(corpus_path_unix):
            self.init_dir = corpus_path_unix
        else:
            self.init_dir = "."

        # Frame project
        frame1 = tk.Frame(self.parent)
        frame1.pack(anchor=tk.W)

        select_prc_button = tk.Button(frame1,
                                      text="Select project",
                                      command=self.select_prc)
        select_prc_button.pack(side=tk.LEFT)

        self.chosen_prc = tk.StringVar()
        prc_entry = tk.Entry(frame1,
                             width=62,
                             textvariable=self.chosen_prc)
        prc_entry.pack(side=tk.LEFT)

        select_directory_button = tk.Button(frame1,
                                            text=u"Select directory",
                                            command=self.sel_dir)
        select_directory_button.pack(side=tk.LEFT)

        # Frame corpus/anticorpus
        frame2 = tk.LabelFrame(self.parent,
                               text="corpus/anticorpus",
                               borderwidth=1,
                               height=100)
        frame2.pack(fill=tk.X)
        self.Corpus_list = ScrolledText(frame2,
                                        height=15,
                                        font=("Helvetica", 9))
        self.Corpus_list.pack(side=tk.LEFT)
        self.anti_corpus_list = ScrolledText(frame2,
                                             height=15,
                                             font=("Helvetica", 9))
        self.anti_corpus_list.pack(side=tk.LEFT)

        self.progressbar = ttk.Progressbar(self.parent, mode='determinate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        # Frame theme, parameters, logs
        frame3 = tk.Frame(self.parent, padx=10, pady=10)
        frame3.pack(fill=tk.X)

        fr31 = tk.LabelFrame(frame3, text="theme", padx=10)
        fr31.pack(anchor=tk.N, side=tk.LEFT)
        self.L_presents = tk.Listbox(fr31)
        self.L_presents.pack(fill=tk.X)
        self.L_presents.insert(0, "toujours")
        self.L_presents.insert(0, "jamais")
        self.L_presents.insert(0, "parfois")
        bn_del = tk.Button(fr31, text=u"del", command=self.theme_remove)
        bn_del.pack(anchor=tk.W)
        paned312 = tk.PanedWindow(fr31)
        paned312.pack()
        self.w_add_Entry = tk.Entry(paned312)
        self.w_add_Entry.pack(side=tk.LEFT)
        self.bn_add = tk.Button(paned312,
                                text=u"add",
                                command=self.theme_add)
        self.bn_add.pack()

        fr32 = tk.Frame(frame3, padx=10)
        fr32.pack(anchor=tk.N, side=tk.LEFT)
        paned321 = tk.PanedWindow(fr32)
        paned321.pack(anchor=tk.W)
        lb_sc = tk.Label(paned321, text=u"total score >=")
        lb_sc.pack(side=tk.LEFT)
        self.entry_Score = tk.Entry(paned321)
        self.entry_Score.pack()
        self.entry_Score.insert(0, "4")
        paned322 = tk.PanedWindow(fr32)
        paned322.pack()
        lb_dep = tk.Label(paned322,
                          text="components >=")
        lb_dep.pack(side=tk.LEFT)
        self.entry_Dep = tk.Entry(paned322)
        self.entry_Dep.pack()
        self.entry_Dep.insert(0, "2")

        bn_proc = tk.Button(fr32,
                            text=u"theme evaluation",
                            command=self.evaluation)
        bn_proc.pack(anchor=tk.W)

        paned323 = tk.PanedWindow(fr32)
        paned323.pack(pady=10, anchor=tk.W)
        bn_save_corpus = tk.Button(paned323,
                                   text="save corpus",
                                   command=self.save_corpus)
        bn_save_corpus.pack(side=tk.LEFT)
        bn_save_anticorpus = tk.Button(paned323,
                                       text="save anticorpus",
                                       command=self.save_anti_corpus)
        bn_save_anticorpus.pack()

        fr33 = tk.Frame(frame3)
        fr33.pack(side=tk.RIGHT)
        self.result = ScrolledText(fr33,
                                   height=15,
                                   bg="black",
                                   fg="orange")
        self.result.pack()

    def select_prc(self):
        self.chosen_prc.set("")
        p = filedialog.askopenfilename(
            filetypes=[("project file", "*.prc")],
            title='Select a project',
            initialdir=self.init_dir)
        self.chosen_prc.set(p)

        self.result.delete(1.0, "end")

        with open(p, 'r', encoding='iso-8859-1') as f:
            self.prc = f.readlines()
            self.list_txt = [list_txt[:-1] for list_txt in self.prc[6:-1]]

        for txt in self.list_txt:
            self.Corpus_list.insert("end", u"%s\n" % txt)
        self.result.insert(1.0,
                           u"Found %d .txt(s) in %s\n" % (len(self.list_txt), p))

        self.anti_corpus_list.delete(1.0, "end")
        self.progressbar['value'] = 0
        self.progressbar['maximum'] = len(self.list_txt)

    def sel_dir(self):
        directory = filedialog.askdirectory(title="Choose directory",
                                            initialdir=self.init_dir)
        self.chosen_prc.set(directory)
        self.result.delete(1.0, "end")

        self.list_txt = []
        for root, rep, files in os.walk(directory):
            self.list_txt.extend(
                [os.path.join(root, name) for name in files if os.path.splitext(name)[1] in [".txt", ".TXT"]])

        for txt in self.list_txt:
            self.Corpus_list.insert("end", u"%s\n" % txt)
        self.result.insert(1.0,
                           u"Found %d .txt(s) in %s\n" % (len(self.list_txt), directory))

    def theme_add(self):
        item = self.w_add_Entry.get()
        if item != "":
            if item in self.L_presents.get(0, 'end'):
                self.result.insert(1.0, u"%s already in theme\n" % item)
            else:
                self.L_presents.insert("end", u"%s" % item)
                self.result.insert(1.0, u"[%s] added to theme\n" % item)
                self.w_add_Entry.delete(0, "end")

    def theme_remove(self):
        selected = self.L_presents.curselection()
        if selected:
            item = self.L_presents.get(selected)
            self.L_presents.delete(selected)
            self.result.insert(1.0, u"%s removed from theme\n" % item)

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
            self.anti_corpus_list.delete(1.0, "end")
            eval = PrcFilter()
            eval.theme = theme
            eval.score = int(self.entry_Score.get())
            eval.dep = int(self.entry_Dep.get())

            for c, txt in enumerate(self.list_txt):
                self.progressbar['value'] = c + 1
                self.parent.update()
                if os.path.isfile(txt):
                    with open(txt, "r", encoding='iso-8859-1') as f:
                        b = f.read()
                    ev = eval.eval_theme(b)
                    if (ev[1][0] >= eval.score) and (ev[1][1] >= eval.dep):
                        self.Corpus_list.insert("end", u"%s %s\n" % (txt, ev[0]))
                        self.list_txt_c.append(txt)
                    else:
                        self.anti_corpus_list.insert("end", u"%s %s\n" % (txt, ev[0]))
                        self.list_txt_ac.append(txt)
                else:
                    self.result.insert(1.0, "%s: no such file\n" % txt)
                    self.list_txt_absent.append(txt)

            self.result.insert(1.0,
                               "%d text(s) positive, %d negative, %d file(s) not found\n"
                               % (len(self.list_txt_c),
                                  len(self.list_txt_ac), len(self.list_txt_absent)))

    def save_corpus(self):
        if len(self.list_txt_c):
            self.save_prc(self.list_txt_c, "pos")

    def save_anti_corpus(self):
        if len(self.list_txt_c):
            self.save_prc(self.list_txt_ac, "neg")

    def save_prc(self, list_txt, suf):
        if len(list_txt):
            p = self.chosen_prc.get()
            if os.path.splitext(p)[1] not in [".prc", ".PRC"]:
                p = "%s.prc" % os.path.split(p)[1]

            if self.prc:
                lines = self.prc[:6]
            else:
                lines = ["projet0005\r\n",
                         "\r\n", "\r\n", "\r\n", "\r\n", "\r\n"]
            lines.extend([txt + "\r\n" for txt in list_txt])
            lines.append("ENDFILE")
            fichier = filedialog.asksaveasfile(mode='w',
                                               filetypes=[("", "*.prc")],
                                               defaultextension=".prc",
                                               initialdir=self.init_dir,
                                               initialfile="%s_filtered_%s%s" % (p[:-4], suf, p[-4:]))
            fichier.writelines(lines)
            fichier.close()
