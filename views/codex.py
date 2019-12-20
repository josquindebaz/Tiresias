"""Viewer for codex management"""
import tkinter as tk
from tkinter import ttk
#from tkinter import filedialog
#from tkinter.scrolledtext import ScrolledText

from mods.codex import Codex

class ViewCodex():
    """Viewer for Codex"""
    def __init__(self, parent):
        self.codex = Codex("data/codex.json")
        
        w_title = tk.Label(parent,
                           text="Codex management",
                           font=("Helvetica", 12, "bold"))
        w_title.pack(fill=tk.X)

        f_sources = tk.LabelFrame(parent,
                                  text="Sources",
                                  padx=10,
                                  background='red')
        f_sources.pack()

        vsb = ttk.Scrollbar(f_sources,
                            orient="vertical",)
        self.tree = ttk.Treeview(f_sources,
                                 selectmode="browse",
                                 height=30,
                                 yscrollcommand = vsb.set)
        self.tree.pack(side=tk.LEFT,)
        vsb.config(command=self.tree.yview)
        vsb.pack(side=tk.LEFT, fill=tk.Y)
        
        self.tree["columns"]=("author", "medium", "media_type")
##        self.tree.column("author", width=100 )
        self.tree.heading("author", text="author")
        self.tree.heading("medium", text="medium")
        self.tree.heading("media_type", text="media-type")
        
##        id2 = self.tree.insert("", 1, "dir2", text="Dir 2")
##        self.tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
##        ##alternatively:
##        self.tree.insert("", 3, "dir3", text="Dir 3")
##        self.tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

        self.populate_source_tree()


    def populate_source_tree(self):
        """feed the source list"""
        self.tree.delete(*self.tree.get_children())
        for source in sorted(self.codex.codex):
            values = '"%s" "%s" "%s"'%\
                     (self.codex.codex[source]['author'],
                      self.codex.codex[source]['medium'],
                      self.codex.codex[source]['media-type'],)
            self.tree.insert("", "end", text=source, values=values)
            

