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
        self.CleaningVal= tk.BooleanVar()
        Bn_Cleaning = tk.Checkbutton(Fr3,
                        text="clean texts",
                        variable=self.CleaningVal)
        Bn_Cleaning.select()
        Bn_Cleaning.pack(side=tk.LEFT)
        self.brackets= tk.BooleanVar()
        Bn_brackets = tk.Checkbutton(Fr3,
                        text="Remove translations in title",
                        variable=self.brackets)
        Bn_brackets.select()
        Bn_brackets.pack(side=tk.LEFT)
        self.rm_copyright= tk.BooleanVar()
        Bn_rm_copyright = tk.Checkbutton(Fr3,
                        text="Remove copyright",
                        variable=self.rm_copyright)
        Bn_rm_copyright.select()
        Bn_rm_copyright.pack(side=tk.LEFT)    
        self.author_keywords= tk.BooleanVar()
        Bn_author_keywords = tk.Checkbutton(Fr3,
                        text="Add author keywords",
                        variable=self.author_keywords)
        Bn_author_keywords.select()
        Bn_author_keywords.pack(side=tk.LEFT)
        self.index_keywords= tk.BooleanVar()
        Bn_index_keywords = tk.Checkbutton(Fr3,
                        text="Add index keywords",
                        variable=self.index_keywords)
        Bn_index_keywords.select()
        Bn_index_keywords.pack(side=tk.LEFT)
        
        #Frame 4
        Fr4 = tk.Frame(self.parent)
        Fr4.pack(anchor=tk.W)        
        bn_process = tk.Button(Fr4, text="Process", command=self.process)
        bn_process.pack(side=tk.LEFT)

        #Frame 5
        Fr5 = tk.Frame(self.parent)
        Fr5.pack()
        self.log = ScrolledText(Fr5, height=10, bg="black", fg="orange")
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
                file_count, no_abstract =\
                    ctx_prospero(csvfile,
                                 save_dir,
                                 cleaning=self.CleaningVal.get(),
                                 brackets=self.brackets.get(),
                                 rm_copyright= self.rm_copyright.get(),
                                 author_keywords=self.author_keywords.get(),
                                 index_keywords=self.index_keywords.get()
                                 )
            self.log.insert(1.0, "Created %d file(s), \
skipped %d articles with no abstract\n" %(file_count, no_abstract))
        else:
            self.log.insert(1.0, "Missing file to process\n")
        
