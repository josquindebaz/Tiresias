import datetime
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from mod.wordreplace import *


class ViewReplacer:
    def __init__(self, parent):
        self.config = None
        self.parent = parent
        self.HISTORY_JSON = ".wordreplace_history.json"

        window_title = tk.Label(self.parent, text="Replace words",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        # Frame 1
        frame_1 = tk.Frame(self.parent)
        frame_1.pack(anchor=tk.W)

        bn_dir = tk.Button(frame_1, text="Select directory",
                           command=self.sel_dir)
        bn_dir.pack(side=tk.LEFT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(frame_1, width=52,
                             textvariable=self.choosenDir)
        # self.choosenDir.set("C:\\corpus\\test")
        dir_entry.pack(side=tk.LEFT)

        self.Recursive = tk.BooleanVar()
        bn_recursive = tk.Checkbutton(frame_1,
                                     text='recursive', variable=self.Recursive)
        bn_recursive.select()
        bn_recursive.pack(side=tk.LEFT)

        self.test = tk.BooleanVar()
        bn_test = tk.Checkbutton(frame_1,
                                 text='test only', variable=self.test)
        bn_test.select()
        bn_test.pack(side=tk.LEFT)

        # Frame 2
        fr2 = tk.PanedWindow(self.parent)
        fr2.pack(anchor=tk.W)

        fr21 = tk.LabelFrame(fr2,
                             text="From patterns", padx=10)
        fr21.pack(anchor=tk.N, side=tk.LEFT)
        self.ListFrom = tk.Listbox(fr21)
        self.ListFrom.pack(fill=tk.X)
        bn_del = tk.Button(fr21, text=u"del",
                           command=self.from_remove)
        bn_del.pack(anchor=tk.W)
        p21 = tk.PanedWindow(fr21)
        p21.pack()
        self.w_add_Entry = tk.Entry(p21)
        self.w_add_Entry.pack(side=tk.LEFT)
        self.bn_add = tk.Button(p21, text=u"add",
                                command=self.from_add)
        self.bn_add.pack()
        self.Marks = tk.BooleanVar()
        bn_m = tk.Checkbutton(fr21, padx=30,
                             text='with marks', variable=self.Marks)
        bn_m.select()
        bn_m.pack()

        fr22 = tk.LabelFrame(fr2,
                             text="To", padx=10)
        fr22.pack(anchor=tk.N, side=tk.LEFT)

        self.EntryTo = tk.Entry(fr22, width=30)
        self.EntryTo.pack()

        bn_proc = tk.Button(fr22, text="Replace",
                            command=self.process)
        bn_proc.pack(pady=10)

        fr23 = tk.LabelFrame(fr2,
                             text="History", padx=10)
        fr23.pack()
        self.history = tk.Listbox(fr23, width=45)
        self.history.pack()
        self.history_populate()
        recall_bn = tk.Button(fr23, text='Recall',
                              command=self.recall)
        recall_bn.pack()

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
        if selected:
            # item = self.ListFrom.get(selected)
            self.ListFrom.delete(selected)
            # self.result.insert(1.0, "%s removed from From list\n"%item)

    def from_add(self):
        item = self.w_add_Entry.get()
        if item != "":
            if item in self.ListFrom.get(0, 'end'):
                self.result.insert(1.0, u"%s already in From list\n" % item)
            else:
                self.ListFrom.insert("end", u"%s" % item)
                # self.result.insert(1.0, "[%s] added to From list\n"%item)
                self.w_add_Entry.delete(0, "end")

    def history_populate(self):
        try:
            with open(self.HISTORY_JSON, 'r') as F:
                self.config = json.load(F)
            self.history.delete(0, "end")
            for date in sorted(self.config['WR']['H'].keys()):
                self.history.insert(0, self.config['WR']['H'][date])
        except:
            print('pb loading history')
            pass

    def history_add(self, value):
        if not hasattr(self, 'config'):
            self.config = {'WR': {'H': {}}}
        exists = [d for d, v in self.config['WR']['H'].items()
                  if (v == value)]
        if exists:
            del (self.config['WR']['H'][exists[0]])
        self.config['WR']['H'][str(datetime.datetime.now())] = value
        try:
            with open(self.HISTORY_JSON, 'w') as f:
                json.dump(self.config, f)
        except:
            print('pb saving history')
        self.history_populate()

    def recall(self):
        selected = self.history.curselection()
        if selected:
            rec = self.history.get(selected)
            self.ListFrom.delete(0, "end")
            self.EntryTo.delete(0, "end")
            self.EntryTo.insert(0, rec[0])
            for f in rec[1:]:
                self.ListFrom.insert("end", f)

    def process(self):
        folder = self.choosenDir.get()
        to_replace = self.ListFrom.get(0, 'end')
        replacing_form = self.EntryTo.get()
        if to_replace:
            if replacing_form in to_replace:
                self.result.insert(1.0,
                                   "Error: [%s] is in to_replace list\n" % replacing_form)
            else:
                to_from = [replacing_form]
                to_from.extend(to_replace)
                self.history_add(to_from)

                text_list = list_files(folder, recursive=self.Recursive.get())
                self.result.insert(1.0,
                                   "Found %d .txt file(s)\n" % len(text_list))
                self.progressbar['value'] = 0
                self.progressbar['maximum'] = len(text_list)
                cpt = 0

                processor = Replacer()
                processor.set_motif(to_from, with_marks=self.Marks.get())

                for c, txt in enumerate(text_list):
                    self.progressbar['value'] = c + 1
                    with open(txt, 'rb') as f:
                        buf = f.read()
                    processor.set_content(buf)
                    processor.process()
                    if processor.log:
                        if not self.test.get():
                            buf = bytes(processor.content, 'latin-1')
                            with open(txt, 'wb') as f:
                                f.write(buf)
                            cpt += 1
                        self.result.insert(1.0,
                                           "%d match(es) in %s\n" % (processor.log, txt))
                    self.parent.update()
                self.result.insert(1.0, "%d file(s) edited\n" % cpt)
