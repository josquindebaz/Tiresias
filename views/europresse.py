import tkinter as tk
from tkinter import ttk
from pathlib import Path

from mod.europresse import *
from mod.supports import Publi


class ViewEuropresse():
    def __init__(self, parent):
        self.articles_list = None
        self.Supports = None
        self.knownSources = None
        self.list_html = None
        self.parent = parent
        self.htmldirectory = None
        window_title = tk.Label(self.parent, text="Europresse",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        corpus_path_windows = r"C:\corpus"
        try:
            home = str(Path.home())
            corpus_path_unix = "%s/.wine/drive_c/corpus" % home
        except:
            corpus_path_unix = "/home"
        if os.path.isdir(corpus_path_windows):
            self.initdir = corpus_path_windows
        elif os.path.isdir(corpus_path_unix):
            self.initdir = corpus_path_unix
        else:
            self.initdir = "."

        # FrameDir
        frame_dir = tk.Frame(self.parent)
        frame_dir.pack(anchor=tk.W)

        bn_dir = tk.Button(frame_dir,
                           text="Select .html Europresse file directory",
                           command=self.sel_dir_html)
        bn_dir.pack(side=tk.LEFT)

        self.chosen_dir = tk.StringVar()
        dir_entry = tk.Entry(frame_dir, width=52,
                             textvariable=self.chosen_dir)
        dir_entry.pack(side=tk.LEFT)

        bn_scan = tk.Button(frame_dir, text="Read Directory",
                            command=self.get_html_list)
        bn_scan.pack(side=tk.LEFT)

        # Central Frame
        fr_temp = tk.PanedWindow(self.parent)
        fr_temp.pack(anchor=tk.W)

        # Europresse Files
        fr_eur_f = tk.Frame(fr_temp)
        fr_eur_f.pack(side=tk.LEFT, anchor=tk.N)
        self.htm_list = tk.Listbox(fr_eur_f, width=50,
                                   selectmode=tk.EXTENDED)
        self.htm_list.pack()
        bn_test_f = tk.Button(fr_eur_f,
                              text="Analyse selected files",
                              command=self.analyse)
        bn_test_f.pack(anchor=tk.W)

        # Unknown sources
        fr_u = tk.LabelFrame(fr_eur_f, text="Unknown Sources", borderwidth=2, )
        fr_u.pack(side=tk.LEFT, anchor=tk.N)
        self.unknown_list = tk.Listbox(fr_u, width=50)
        self.unknown_list.pack()
        self.unknown_list.bind("<<ListboxSelect>>", self.memo_unknown)
        self.memory_selected_unknown = None

        self.CbS = ttk.Combobox(fr_u)
        self.CbS.pack(anchor=tk.W, fill=tk.X)
        self.CbS.bind("<<ComboboxSelected>>", self.combobox_selector)

        up1 = tk.PanedWindow(fr_u)
        up1.pack(anchor=tk.W, fill=tk.X)
        lab_u_pubname = tk.Label(up1, text="Name")
        lab_u_pubname.pack(side=tk.LEFT)
        self.u_pubname = tk.Entry(up1)
        self.u_pubname.pack(fill=tk.X)
        up2 = tk.PanedWindow(fr_u)
        up2.pack(anchor=tk.W, fill=tk.X)
        lab_u_type = tk.Label(up2, text="Type")
        lab_u_type.pack(side=tk.LEFT)
        self.U_type = tk.Entry(up2)
        self.U_type.pack(fill=tk.X)
        up3 = tk.PanedWindow(fr_u)
        up3.pack(anchor=tk.W, fill=tk.X)
        lab_u_abr = tk.Label(up3, text="Abrv")
        lab_u_abr.pack(side=tk.LEFT)
        self.U_abr = tk.Entry(up3)
        self.U_abr.pack(fill=tk.X)

        bn_u_w = tk.Button(fr_u, text="Add to support.publi",
                           command=self.add_support)
        bn_u_w.pack()

        # article list
        fr_art = tk.LabelFrame(fr_temp, text="Found articles", borderwidth=2)
        fr_art.pack()
        self.art_list = tk.Listbox(fr_art, width=100, height=30,
                                   selectmode=tk.EXTENDED)
        self.art_list.pack(side=tk.LEFT)
        sb_art = tk.Scrollbar(fr_art)
        sb_art.pack(side=tk.RIGHT, fill=tk.Y)
        sb_art.configure(command=self.art_list.yview)
        self.art_list.configure(yscrollcommand=sb_art.set)

        wp2 = tk.PanedWindow(fr_temp)
        wp2.pack(anchor=tk.W, fill=tk.BOTH)
        bn_dir_w = tk.Button(wp2,
                             text="Select Prospero file directory",
                             command=self.sel_dir_w)
        bn_dir_w.pack(side=tk.LEFT)
        self.chosen_dir_w = tk.StringVar()
        dir_w_entry = tk.Entry(wp2, width=52,
                               textvariable=self.chosen_dir_w)
        dir_w_entry.pack(fill=tk.X)

        self.CleaningVal = tk.BooleanVar()
        bn_cleaning = tk.Checkbutton(fr_temp,
                                     text="clean texts",
                                     variable=self.CleaningVal)
        bn_cleaning.select()
        bn_cleaning.pack(side=tk.LEFT)

        bn_process_art = tk.Button(fr_temp,
                                   text="Write selected articles",
                                   command=self.write_articles)
        bn_process_art.pack(side=tk.LEFT, padx=10)

        self.progressbar = ttk.Progressbar(self.parent, mode='determinate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        # Log Frame
        fr_log = tk.Frame(self.parent)
        fr_log.pack(fill=tk.X)
        self.log = tk.scrolledtext.ScrolledText(fr_log,
                                                height=10, bg="black", fg="orange")
        self.log.pack(fill=tk.X)

    def memo_unknown(self, callback):
        self.memory_selected_unknown = self.unknown_list.curselection()

    def combobox_selector(self, callback):
        self.reset_supports()
        index = self.CbS.current()
        if index:
            values = self.knownSources[index].split("; ")
            self.u_pubname.insert(0, values[0])
            self.U_type.insert(0, values[1])
            self.U_abr.insert(0, values[2])

        if self.memory_selected_unknown:
            self.unknown_list.selection_set(self.memory_selected_unknown)

    def add_support(self):
        i = self.unknown_list.curselection()
        if i:
            s = self.unknown_list.get(i)
            n = self.u_pubname.get()
            t = self.U_type.get()
            a = self.U_abr.get()
            self.log.insert(1.0,
                            "Adding to support.publi [%s] as %s; %s; %s\n" % (s, n, t, a))
            self.Supports.add(s, n, t, a)
            self.Supports.write()
            self.populate_supports()
            self.unknown_list.delete(i)

    def sel_dir_html(self):
        self.chosen_dir.set("")
        self.reset_lists()

        self.htmldirectory = tk.filedialog.askdirectory(title="Choose directory")
        self.chosen_dir.set(self.htmldirectory)
        self.get_html_list()
        self.log.insert(1.0,
                        "Found %d .html file(s) in %s\n" % (len(self.list_html),
                                                            self.htmldirectory))

    def reset_lists(self):
        self.unknown_list.delete(0, 'end')
        self.art_list.delete(0, 'end')

    def get_html_list(self):
        self.reset_lists()
        self.htm_list.delete(0, 'end')

        directory = self.chosen_dir.get()
        if directory:
            rule = re.compile(r".*\.htm.", re.IGNORECASE)
            self.list_html = [f for f in os.listdir(directory) if
                              rule.match(f)]
            [self.htm_list.insert("end",
                                  os.path.split(item)[1]) for item in self.list_html]
            self.htm_list.select_set(0, "end")
            if not self.htmldirectory:
                self.htmldirectory = directory

    def reset_supports(self):
        self.u_pubname.delete(0, 'end')
        self.U_type.delete(0, 'end')
        self.U_abr.delete(0, 'end')

    def populate_supports(self):
        self.reset_supports()
        self.knownSources = ["Known sources"]
        self.knownSources.extend(sorted(["%s; %s; %s" % (k,
                                                         self.Supports.sources[k]['type'],
                                                         self.Supports.sources[k]['abr'])
                                         for k in self.Supports.sources]))
        self.CbS['values'] = self.knownSources
        self.CbS.current(0)

    def analyse(self):
        self.reset_lists()

        self.Supports = Publi()
        self.populate_supports()

        unknowns = []
        self.articles_list = []
        for c in self.htm_list.curselection():
            f = self.list_html[c]
            self.log.insert(1.0, 'Analysing %s\n' % f)
            try:
                path = os.path.join(self.htmldirectory, f)
                html_parser = EuropresseHtmlParser(path)
                for a in html_parser.parsed_articles:
                    if a not in self.articles_list:
                        self.articles_list.append(a)
                    if (a['source'] not in self.Supports.codex.keys() and
                            a['source'] not in unknowns):
                        unknowns.append(a['source'])
            except:
                self.log.insert(1.0, 'Analyse problem\n')

        self.log.insert(1.0, 'Found %d compatible \
articles and %d unknown source(s)\n' % (len(self.articles_list), len(unknowns)))
        [self.art_list.insert("end", "%s %s %s" %
                              (a['source'], a['date'], a['title'])) for a in self.articles_list]
        [self.unknown_list.insert("end", u) for u in unknowns]

        self.art_list.select_set(0, "end")

    def sel_dir_w(self):
        memory_selected_articles = self.art_list.curselection()
        self.chosen_dir_w.set("")
        directory = tk.filedialog.askdirectory(title="Choose directory",
                                               initialdir=self.initdir)
        self.chosen_dir_w.set(directory)
        for a in memory_selected_articles:
            self.art_list.selection_set(a)

    def write_articles(self):
        articles = self.art_list.curselection()
        if len(articles):
            self.progressbar['value'] = 0
            self.progressbar['maximum'] = len(articles)
            directory = self.chosen_dir_w.get()
            if not directory:
                self.log.insert(1.0, 'No directory for Prospero files\n')
            else:
                for c, index in enumerate(articles):
                    article = self.articles_list[index]
                    f = ProcessArticle(article, directory,
                                       self.CleaningVal.get())
                    self.log.insert(1.0, 'Writing %s\n' % f.filename)
                    self.progressbar['value'] = c + 1
