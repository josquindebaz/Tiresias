import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText

from mod.openbooks import traite_url


class ViewOpenbooks:
    def __init__(self, parent):
        self.parent = parent
        window_title = tk.Label(self.parent, text="from Openbooks to Prospero",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        # Frame 1
        fr1 = tk.Frame(self.parent)
        fr1.pack(anchor=tk.W)
        bn_dir = tk.Button(fr1, text="Select directory for Prospero Files",
                           command=self.sel_dir)
        bn_dir.pack(side=tk.RIGHT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(fr1, width=52,
                             textvariable=self.choosenDir)
        dir_entry.pack()

        # Frame 2
        fr2 = tk.Frame(self.parent)
        fr2.pack(anchor=tk.W)

        lb_entry = tk.Label(fr2, text="Paste an URL from books.openedition.org")
        lb_entry.pack(side=tk.RIGHT)

        self.choosen_url = tk.StringVar()
        url_entry = tk.Entry(fr2, width=52,
                             textvariable=self.choosen_url)
        url_entry.pack()

        # Frame 3
        fr3 = tk.Frame(self.parent)
        fr3.pack(anchor=tk.W)
        #        self.CleaningVal= tk.BooleanVar()
        #        Bn_Cleaning = tk.Checkbutton(Fr3,
        #                        text="clean texts",
        #                        variable=self.CleaningVal)
        #        Bn_Cleaning.select()
        #        Bn_Cleaning.pack(side=tk.LEFT)
        bn_process = tk.Button(fr3, text="Process", command=self.process)
        bn_process.pack(side=tk.LEFT)

        # Frame 4
        fr4 = tk.Frame(self.parent)
        fr4.pack()
        self.log = ScrolledText(fr4, height=10, bg="black", fg="orange")
        self.log.pack()

    def sel_file(self):
        self.choosen_file.set("")
        filename = fd.askopenfilename(title="Select htm file",
                                      filetypes=[("htm Files", "*.htm")])
        self.choosen_file.set(filename)

    def sel_dir(self):
        self.choosenDir.set("")
        dir = fd.askdirectory(title="Choose directory")
        self.choosenDir.set(dir)

    def process(self):
        url = self.choosen_url.get()
        if url:
            save_dir = self.choosenDir.get()
            if not save_dir:
                save_dir = os.getcwd()
            self.log.insert(1.0, "Processing %s to %s\n" % (url, save_dir))
            self.parent.update()
            traite_url(url, save_dir)
            #            self.log.insert(1.0,
            #                            "%s: found %d article(s)\n"%(filename,
            #                                                       len(parse.content)))
            #            parse.get_supports("data/support.publi")
            #            self.log.insert(1.0,
            #                            "%d unknown(s) source(s)\n" %len(parse.unknowns))
            #            for unknown in parse.unknowns:
            #                self.log.insert(1.0, "unknown: %s\n" % unknown)
            #            parse.write_prospero_files(save_dir, self.CleaningVal.get())
            self.log.insert(1.0, "done\n")
            self.parent.update()
        else:
            self.log.insert(1.0, "Missing URL to process\n")
