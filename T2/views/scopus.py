import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText

from mod.scopus import ctx_prospero

class ViewScopus():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="csv from Scopus to Prospero",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        #Frame 1
        Fr1 = tk.Frame(self.parent)
        Fr1.pack(anchor=tk.W)

        bn_csv = tk.Button(Fr1, text="Select a csv file",
            command=self.sel_file)
        bn_csv.pack(side=tk.RIGHT)

        self.choosen_file = tk.StringVar()
        csv_entry = tk.Entry(Fr1, width=52,
                             textvariable=self.choosen_file)
        csv_entry.pack()
        
        #Frame 2
        Fr2 = tk.Frame(self.parent)
        Fr2.pack(anchor=tk.W)
        bnDir = tk.Button(Fr2, text="Select directory for Prospero Files",
            command=self.sel_dir)
        bnDir.pack(side=tk.RIGHT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(Fr2, width=52,
            textvariable=self.choosenDir)
        dir_entry.pack()

        #Frame 3
        Fr3 = tk.Frame(self.parent)
        Fr3.pack(anchor=tk.W)
        bn_process = tk.Button(Fr3, text="Process", command=self.process)
        bn_process.pack(side=tk.LEFT)

        #Frame 4
        Fr4 = tk.Frame(self.parent)
        Fr4.pack()
        self.log = ScrolledText(Fr4, height=10, bg="black", fg="orange")
        self.log.pack()

    def sel_file(self):
        self.choosen_file.set("")
        filename = fd.askopenfilename(title = "Select csv file",
                                      filetypes =[("csv Files", "*.csv")])
        self.choosen_file.set(filename)
        
    def sel_dir(self):
        self.choosenDir.set("")
        dir = fd.askdirectory(title="Choose directory")
        self.choosenDir.set(dir)

    def process(self):
        filename = self.choosen_file.get()
        if filename:
            save_dir = self.choosenDir.get()
            if not save_dir:
                save_dir = os.getcwd()
            self.log.insert(1.0, "Processing %s to %s\n"%(filename, save_dir))
            self.parent.update()
            with open(filename, newline='', encoding='utf-8-sig') as csvfile:
                file_count = ctx_prospero(csvfile, save_dir)
            self.log.insert(1.0, "Created %s file(s)\n" %file_count)
        else:
            self.log.insert(1.0, "Missing file to process\n")
        
