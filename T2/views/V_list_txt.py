import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from threading import Thread

from mod.cleaning import list_files

class V_list_txt():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text=".txt and .TXT List",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        #Frame 1
        Fr1 = tk.Frame(self.parent)
        Fr1.pack(anchor=tk.W)

        bnDir = tk.Button(Fr1, text="Select directory",
            command=self.sel_dir)
        bnDir.pack(side=tk.LEFT)

        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(Fr1, width=52,
            textvariable=self.choosenDir)
        self.choosenDir.set("C:\corpus")
        dir_entry.pack(side=tk.LEFT)

        self.Recursive = tk.BooleanVar()
        bnRecursive = tk.Checkbutton(Fr1, 
            text='recursive', var=self.Recursive)
        bnRecursive.select()
        bnRecursive.pack(side=tk.LEFT)

        bnAction = tk.Button(Fr1, text="List",
            command=self._t_Action)
        bnAction.pack(side=tk.LEFT, padx=20)
        bnCopy = tk.Button(Fr1, text="Copy",
            command=self.CopyToClipboard)
        bnCopy.pack()

        #Frame 2
        Fr2 = tk.LabelFrame(self.parent, 
            text="Replace path", borderwidth=1)
        Fr2.pack(anchor=tk.W)

        LabFrom = tk.Label(Fr2, text='from')
        LabFrom.pack(side=tk.LEFT)
        self.EntryFrom = tk.Entry(Fr2, width=30)
        self.EntryFrom.pack(side=tk.LEFT)
        LabTo = tk.Label(Fr2, text='to')
        LabTo.pack(side=tk.LEFT)
        self.EntryTo = tk.Entry(Fr2, width=30)
        self.EntryTo.pack(side=tk.LEFT)
        self.Slash = tk.BooleanVar()
        bnSlash = tk.Checkbutton(Fr2, padx=30,
            text='replace / with \\', var=self.Slash)
        bnSlash.select()
        bnSlash.pack(side=tk.RIGHT)

        self.progressbar = ttk.Progressbar(self.parent,
            mode='indeterminate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        self.result = ScrolledText(self.parent)
        self.result.pack(fill=tk.X)

    def sel_dir(self):
        self.choosenDir.set("")
        self.result.delete(1.0, "end")
        self.progressbar['value'] = 0
        dir = filedialog.askdirectory(title="Choose directory",
            initialdir="C:\corpus")
        self.choosenDir.set(dir)

    def _t_Action(self):
        self._thread = Thread(target=self.Action)
        self._thread.start()

    def Action(self):
        self.result.delete(1.0, "end")
        rep = self.choosenDir.get()
        if rep == '':
            self.result.insert(1.0, "No directory selected")
        else:
            self.progressbar.start()

            try:
                fr = self.EntryFrom.get()
                
                if (fr):
                    to = self.EntryTo.get()
                    repl = [fr, to]
                else:
                    repl = []
                    
                if (self.Slash.get()):
                    slash = True
                else:
                    slash = False
                    
                query = list_files(rep, [".txt", ".TXT"],
                            self.Recursive.get(), slash, repl)
                
                if len(query) > 0:
                    self.result.insert(1.0, "\n".join(query))
                else:
                    self.result.insert(1.0, "Nothing found")
                    
            except:
                self.result.insert(1.0, "Execution problem")
            self.progressbar.stop()
            self.progressbar['mode'] = 'determinate'
            self.progressbar['value'] = 100 
        
    def CopyToClipboard(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.result.get(1.0, "end"))



