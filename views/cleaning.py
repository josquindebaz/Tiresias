"""Viewer for cleaning module
Josquin Debaz
GPL3
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from threading import Thread

from mod.cleaning import list_files
from mod.cleaning import Cleaner


class ViewCleaning:
    """cleaning window"""

    def __init__(self, parent):
        self._thread = None
        self.query = None
        self.parent = parent
        window_title = tk.Label(parent,
                                text="Character Cleaning",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        # Frame directory
        fr1 = tk.Frame(parent)
        fr1.pack(anchor=tk.W)

        button_directory = tk.Button(fr1,
                                     text="Select directory",
                                     command=self.sel_dir)
        button_directory.pack(side=tk.LEFT)

        self.chosen_directory = tk.StringVar()
        dir_entry = tk.Entry(fr1,
                             width=52,
                             textvariable=self.chosen_directory)
        self.chosen_directory.set(r"C:\corpus")
        dir_entry.pack(side=tk.LEFT)

        self.is_recursive = tk.BooleanVar()
        button_recursive = tk.Checkbutton(fr1,
                                          text='recursive',
                                          variable=self.is_recursive)
        button_recursive.select()
        button_recursive.pack(side=tk.LEFT)

        self.test = tk.BooleanVar()
        bn_test = tk.Checkbutton(fr1,
                                 text='test only',
                                 variable=self.test)
        # bn_test.select()
        bn_test.pack(side=tk.LEFT)

        button_action = tk.Button(fr1,
                                  text="Process cleaning",
                                  command=self.t_action)
        button_action.pack(side=tk.LEFT)

        # Frame Options
        fr2 = tk.LabelFrame(parent,
                            text="Options",
                            borderwidth=1)
        fr2.pack()
        self.utf = tk.BooleanVar()
        bn_utf = tk.Checkbutton(fr2,
                                text='Utf8 to Latin1',
                                variable=self.utf)
        bn_utf.select()
        bn_utf.pack(side=tk.LEFT)
        self.ascii = tk.BooleanVar()
        bn_ascii = tk.Checkbutton(fr2,
                                  text='ascii',
                                  variable=self.ascii)
        bn_ascii.select()
        bn_ascii.pack(side=tk.LEFT)
        self.char_replace = tk.BooleanVar()
        bn_char_replace = tk.Checkbutton(fr2,
                                         text='special chars',
                                         variable=self.char_replace)
        bn_char_replace.select()
        bn_char_replace.pack(side=tk.LEFT)

        self.html_chars = tk.BooleanVar()
        bn_html_unescape = tk.Checkbutton(fr2,
                                          text='html chars',
                                          variable=self.html_chars)
        bn_html_unescape.select()
        bn_html_unescape.pack(side=tk.LEFT)

        self.split = tk.BooleanVar()
        bn_split = tk.Checkbutton(fr2,
                                  text='split numbers',
                                  variable=self.split)
        bn_split.select()
        bn_split.pack(side=tk.LEFT)
        self.hyphens = tk.BooleanVar()
        bn_hyphens = tk.Checkbutton(fr2,
                                    text='hyphenations',
                                    variable=self.hyphens)
        bn_hyphens.select()
        bn_hyphens.pack(side=tk.LEFT)
        self.html_tags = tk.BooleanVar()
        bn_html_tags = tk.Checkbutton(fr2,
                                      text='html tags',
                                      variable=self.html_tags)
        bn_html_tags.select()
        bn_html_tags.pack(side=tk.LEFT)
        self.parity_marks = tk.BooleanVar()
        bn_parity_marks = tk.Checkbutton(fr2,
                                         text='parity marks',
                                         variable=self.parity_marks)
        bn_parity_marks.select()
        bn_parity_marks.pack(side=tk.LEFT)
        self.dashes = tk.BooleanVar()
        bn_dashes = tk.Checkbutton(fr2,
                                   text='dashes',
                                   variable=self.dashes)
        bn_dashes.select()
        bn_dashes.pack(side=tk.LEFT)
        self.footnotes = tk.BooleanVar()
        bn_footnotes = tk.Checkbutton(fr2,
                                      text='footnotes',
                                      variable=self.footnotes)
        bn_footnotes.select()
        bn_footnotes.pack(side=tk.LEFT)

        # Progress bar
        self.progressbar = ttk.Progressbar(parent)
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        # Results
        self.result = ScrolledText(parent,
                                   bg="black",
                                   fg="orange")
        self.result.pack(fill=tk.X)

    def t_action(self):
        """execute cleaning"""
        self.query = []
        self.result.delete(1.0, "end")
        self.result.insert("end", "Listing text files\n")
        self.parent.update()

        self._thread = Thread(target=self.list_txt)
        self._thread.start()
        while not self.query:
            self.parent.update()
        self._thread = None

        if len(self.query) > 0:
            self.result.insert("end",
                               "%d file(s) found\n" % len(self.query))
            if self.test.get():
                self.result.insert("end", "only testing\n")
            else:
                self.result.insert("end",
                                   "Processing text cleaning\n")
            self.progressbar['mode'] = 'determinate'
            self.progressbar['maximum'] = len(self.query)
            n = 0
            for c, txt in enumerate(self.query):
                n += self.clean_txt(txt)
                self.progressbar['value'] = c
                self.parent.update()
                self.result.see("end")

            self.result.insert("end", "%d file(s) cleaned\n" % n)

        else:
            self.result.insert("end", "Nothing found\n")

    def clean_txt(self, txt):
        with open(txt, 'rb') as f:
            b = f.read()

        options = ""
        if self.utf.get():
            options += "u"
        if self.ascii.get():
            options += "a"
        if self.char_replace.get():
            options += "c"
        if self.html_chars.get():
            options += "e"
        if self.split.get():
            options += "s"
        if self.hyphens.get():
            options += "h"
        if self.html_tags.get():
            options += "t"
        if self.parity_marks.get():
            options += "p"
        if self.dashes.get():
            options += "d"
        if self.footnotes.get():
            options += "f"

        c = Cleaner(b, options)

        if not set([x for x in c.log.values()]) == {0}:
            # if something has to be corrected
            self.result.insert("end", "%s  " % txt)
            self.result.insert("end",
                               "%s\n" % "; ".join(["%s: %s" % (x, y)
                                                   for x, y in c.log.items()
                                                   if y != 0]))
            if not self.test.get():
                # if not in test mode
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
        rep = self.chosen_directory.get()
        if rep == '':
            self.result.insert("end", "No directory selected")
        else:
            self.query = list_files(rep=rep,
                                    recursive=self.is_recursive.get())
        self.progressbar.stop()

    def sel_dir(self):
        self.chosen_directory.set("")
        self.result.delete(1.0, "end")
        self.progressbar['value'] = 0
        rep = filedialog.askdirectory(title="Choose directory",
                                      initialdir=r"C:\corpus")
        self.chosen_directory.set(rep)
