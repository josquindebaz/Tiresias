import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#from tkinter.scrolledtext import ScrolledText

from mods.codex import Codex

class ViewCodex():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent,
                               text="Codex management",
                               font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        Fr2 = tk.LabelFrame(self.parent,
                            text="Sources",
                            padx=10)
        Fr2.pack(anchor=tk.W)
        self.list_sources = tk.Listbox(Fr2)
        self.list_sources.pack(fill=tk.X)

        self.CODEX = Codex("data/codex.json")
        self.populate()


    def populate(self):
        self.list_sources.delete(0, "end")
        for source in sorted(self.CODEX.codex):
            self.list_sources.insert(tk.END, source)
