import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import os
import re
from pathlib import Path

accents = ["à", "á", "â", "ã", "ä", "å", "æ", "ã", "ç",
           "è", "é", "ê", "ë",
           "ì", "í", "î", "ï", "ĩ",
           "ð", "ò", "ó", "ô", "õ", "ö", "õ", "ø", "ñ",
           "ù", "ú", "û", "ü", "ũ", "ý", "þ", "ÿ"]
upper_accents = [letter.upper() for letter in accents]


class ViewCap():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="Case changes",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        self.list_txt = []
        self.list_txt_c = []
        self.prc = []

        corpus_path_windows = "C:\corpus"
        try:
            home = str(Path.home())
            corpus_path_unix = "%s/.wine/drive_c/corpus"%home
        except:
            corpus_path_unix = "/home"
        if os.path.isdir(corpus_path_windows):
            self.initdir = corpus_path_windows
        elif os.path.isdir(corpus_path_unix):
            self.initdir = corpus_path_unix
        else:
            self.initdir = "."

        """Frame project / directory"""
        Fr1 = tk.Frame(self.parent)
        Fr1.pack(anchor=tk.W)

        bnPrc = tk.Button(Fr1,
                          text="Select project",
                          command=self.sel_PRC)
        bnPrc.pack(side=tk.LEFT)

        self.choosenPRC = tk.StringVar()
        PRC_entry = tk.Entry(Fr1, width=62,
            textvariable=self.choosenPRC)
        PRC_entry.pack(side=tk.LEFT)

        bnDir = tk.Button(Fr1,
                          text="Select directory",
                          command=self.sel_dir)
        bnDir.pack(side=tk.LEFT)


        """Frame parameters"""
        Fr2 = tk.LabelFrame(self.parent,
                            text="Search parameters",
                            borderwidth=1)
        Fr2.pack(fill=tk.X)

        lb_min = tk.Label(Fr2, text="minimum")
        lb_min.pack(side=tk.LEFT)
        self.entry_min = tk.Entry(Fr2, width=5)
        self.entry_min.pack(side=tk.LEFT)
        self.entry_min.insert(0, "3")
        lb_max = tk.Label(Fr2 ,text="maximum")
        lb_max.pack(side=tk.LEFT)
        self.entry_max = tk.Entry(Fr2, width=5)
        self.entry_max.pack(side=tk.LEFT)
        self.entry_max.insert(0, "100")
        self.bn_list = tk.Button(Fr2,
                                 text="list uppercase groups",
                                 command=self.list_groups)
        self.bn_list.pack(side=tk.LEFT)
        self.bn_list_capz = tk.Button(Fr2,
                                      text="list first letter capitalised terms",
                                      command=self.list_caps)
        self.bn_list_capz.pack(side=tk.RIGHT)

        """Frame lists"""
        Fr3 = tk.LabelFrame(self.parent,
                            text="Term selection",
                            borderwidth=1)
        Fr3.pack(fill=tk.X)
        self.found_list = tk.Listbox(Fr3,
                                     height=20,
                                     width=60)
        self.found_list.pack(side=tk.LEFT)
        self.found_list_scrollbar = ttk.Scrollbar(Fr3,
                                                  orient="vertical",
                                                  command=self.found_list.yview)
        self.found_list.configure(yscrollcommand=self.found_list_scrollbar.set)
        self.found_list_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.found_list.bind('<ButtonRelease-1>', self.found_list_clic)

        paned_buttons = ttk.PanedWindow(Fr3, orient=tk.VERTICAL)
        paned_buttons.pack(side=tk.LEFT, anchor=tk.N)
        self.bn_sel_all = tk.Button(paned_buttons,
                                    text="Select all",
                                    command=self.sel_all)
        self.bn_sel_all.pack()
        self.bn_desel_all = tk.Button(paned_buttons,
                                      text="Deselect all",
                                      command=self.desel_all)
        self.bn_desel_all.pack()

        self.selected_list = tk.Listbox(Fr3,
                                        height=20,
                                        width=60)
        self.selected_list.pack(side=tk.LEFT)
        self.selected_list_scrollbar = ttk.Scrollbar(Fr3,
                                                     orient="vertical",
                                                     command=self.selected_list.yview)
        self.selected_list.configure(yscrollcommand=self.selected_list_scrollbar.set)
        self.selected_list_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.selected_list.bind('<ButtonRelease-1>', self.selected_list_clic)

        """Frame actions"""
        Fr4 = tk.LabelFrame(self.parent,
                            text="Actions",
                            borderwidth=1)
        Fr4.pack(fill=tk.X)
        self.bn_minz = tk.Button(Fr4,
                                 text="Lower case",
                                 command=self.lower_case)
        self.bn_minz.pack(side=tk.LEFT)
        self.bn_capz = tk.Button(Fr4,
                                 text="Capitalize",
                                 command=self.capitalize_case)
        self.bn_capz.pack(side=tk.LEFT)
        self.bn_upz = tk.Button(Fr4,
                                text="Upper case",
                                 command=self.upper_case)
        self.bn_upz.pack(side=tk.LEFT)

        self.progressbar = ttk.Progressbar(self.parent, mode='determinate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        fr_logs = tk.Frame(self.parent)
        fr_logs.pack(fill=tk.X)
        self.result = ScrolledText(fr_logs,
                                   height=15,
                                   bg="black",
                                   fg="orange")
        self.result.pack(fill=tk.X)


    def sel_PRC(self):
        self.choosenPRC.set("")
        p = filedialog.askopenfilename(
            filetypes=[("project file","*.prc")],
            title='Select a project',
            initialdir=self.initdir)

        if p:
            self.choosenPRC.set(p)
            self.result.delete(1.0, tk.END)

            with open(p, 'r', encoding='iso-8859-1') as f:
                self.prc = f.readlines()
            candidates = [l[:-1] for l in self.prc[6:-1]]
            self.list_txt = [txt for txt in candidates if os.path.isfile(txt)]
            absents = set(candidates)-set(self.list_txt)

            self.result.insert(1.0,
                               "Found %d .txt(s)\
in %s\n"%(len(self.list_txt), p))
            if absents:
                self.result.insert(1.0,
                                   "warning !\
 %d .txt cannot be found: %s\n"%(len(absents), " ".join(absents)))


            self.progressbar['value'] = 0
            self.progressbar['maximum'] =  len(self.list_txt)

    def sel_dir(self):
        directory = filedialog.askdirectory(title="Choose directory",
                                               initialdir=self.initdir)

        self.choosenPRC.set(directory)
        self.result.delete(1.0, tk.END)

        self.list_txt = []
        for root, rep, files in os.walk(directory):
            self.list_txt.extend([os.path.join(root, name)
                for name in files
                if os.path.splitext(name)[1] in [".txt", ".TXT"]
                ])

        self.result.insert(1.0,
                           "Found %d .txt(s) in %s\n"%(len(self.list_txt),
                                                       directory))

    def show_groups(self, groups):
        self.found_list.delete(0, tk.END)
        self.selected_list.delete(0, tk.END)

        self.result.insert(1.0, "Found %d term(s)\n"%len(groups))
        if len(groups):
            for found in sorted(groups):
                self.found_list.insert('end', found)

    def list_groups(self):
        self.result.insert(1.0, "Searching for uppercase groups\n")
        self.progressbar['value'] = 0
        self.parent.update()
        minimum = int(self.entry_min.get())
        maximum = int(self.entry_max.get())
        aggregate = set([])
        motif = re.compile(r"[A-Z%s\-]{%d,%d}"%("".join(upper_accents),
                                                minimum,
                                                maximum))
        for c, filename in enumerate(self.list_txt):
            self.progressbar['value'] = c+1
            self.parent.update()
            with open(filename, 'r') as pointer:
                content = pointer.read()
            aggregate.update(set(motif.findall(content)))
        self.show_groups(list(aggregate))

    def list_caps(self):
        self.result.insert(1.0,
                           "Searching for terms with first letter capitalized\n")
        self.progressbar['value'] = 0
        self.parent.update()
        aggregate = set([])
        motif = re.compile(r"[A-Z%s][a-z%s]+"%("".join(upper_accents),
                                               "".join(accents)))
        for c, filename in enumerate(self.list_txt):
            self.progressbar['value'] = c+1
            self.parent.update()
            with open(filename, 'r') as pointer:
                content = pointer.read()
            aggregate.update(set(motif.findall(content)))
        self.show_groups(list(aggregate))

    def found_list_clic(self, something):
        select = self.found_list.curselection()
        self.selected_list.insert(tk.END,
                                  self.found_list.get(select))
        self.sort_listbox(self.selected_list)
        self.found_list.delete(select)

    def selected_list_clic(self, something):
        select = self.selected_list.curselection()
        self.found_list.insert(tk.END,
                                  self.selected_list.get(select))
        self.sort_listbox(self.found_list)
        self.selected_list.delete(select)

    def sort_listbox(self, listbox):
        """
        function to sort listbox items
        """
        temp_list = list(listbox.get(0, tk.END))
        temp_list.sort()
        listbox.delete(0, tk.END)
        for item in temp_list:
            listbox.insert(tk.END, item)

    def sel_all(self):
        for item in list(self.found_list.get(0, tk.END)):
            self.selected_list.insert(tk.END, item)
            self.found_list.delete(0)

    def desel_all(self):
        for item in list(self.selected_list.get(0, tk.END)):
            self.found_list.insert(tk.END, item)
            self.selected_list.delete(0)

    def lower_case(self):
        selected = list(self.selected_list.get(0, tk.END))
        if selected and self.list_txt:
            self.result.insert(1.0, "Lowering case\n")
            self.transform(selected, "lower")
        else:
            self.result.insert(1.0, "Nothing selected\n")            

    def capitalize_case(self):
        selected = list(self.selected_list.get(0, tk.END))
        if selected and self.list_txt:
            self.result.insert(1.0, "Capitalizing\n")
            self.transform(selected, "capitalize")
        else:
            self.result.insert(1.0, "Nothing selected\n")
            
    def upper_case(self):
        selected = list(self.selected_list.get(0, tk.END))
        if selected and self.list_txt:
            self.result.insert(1.0, "Uppering case\n")
            self.transform(selected, "upper")
        else:
            self.result.insert(1.0, "Nothing selected\n")
            
    def transform(self, selected, action):
        self.selected_list.delete(0, tk.END)
        self.found_list.delete(0, tk.END)
        self.progressbar['value'] = 0
        self.parent.update()
        for c, filename in enumerate(self.list_txt):
            self.progressbar['value'] = c+1
            self.parent.update()
            with open(filename, 'r') as pointer:
                content = pointer.read()
            change = 0
            for item in selected:
                count = len(re.findall(item, content))
                if count:
                    change += count
                    self.result.insert(1.0,
                                       "%s %d [%s] in %s\n"%(action,
                                                             count,
                                                             item,
                                                             filename))
                    if action == 'lower':
                        corrected = item.lower()
                    elif action == "capitalize":
                        corrected = item.capitalize()
                    elif action == "upper":
                        corrected = item.upper()
                    content = re.sub(item, corrected, content)
            if change:
                with open(filename, 'w') as pointer:
                    pointer.write(content)
