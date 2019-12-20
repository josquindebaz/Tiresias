"""Viewer for codex management"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
#from tkinter.scrolledtext import ScrolledText

from mods.codex import *

class ViewCodex():
    """Viewer for Codex"""
    def __init__(self, parent):
        self.manager = CodexManager("data/codex.json")
        
        w_title = tk.Label(parent,
                           text="Codex management",
                           font=("Helvetica", 12, "bold"))
        w_title.pack(fill=tk.X)

        self.f_sources = tk.LabelFrame(parent,
                                  text="Sources",
                                  padx=10,
                                  background='red')
        self.f_sources.pack()
        
        P_top = tk.PanedWindow(self.f_sources,
                               background='blue')
        P_top.pack()
        
        vsb = ttk.Scrollbar(P_top,
                            orient="vertical",)
        self.tree = ttk.Treeview(P_top,
                                 selectmode="browse",
                                 height=20,
                                 yscrollcommand = vsb.set)
        self.tree.pack(side=tk.LEFT,)
        vsb.config(command=self.tree.yview)
        vsb.pack(side=tk.LEFT, fill=tk.Y)

        self.populate_source_tree()


        P_buttons = tk.PanedWindow(self.f_sources,
                                   background='yellow')
        P_buttons.pack(fill=tk.X)

        b_search = tk.Button(P_buttons, text="Search")
        b_search.pack(side=tk.LEFT, anchor=tk.N)
        b_add = tk.Button(P_buttons, text="b_add")
        b_add.pack(side=tk.LEFT, anchor=tk.N)
        b_del = tk.Button(P_buttons, text="b_del")
        b_del.pack(side=tk.LEFT, anchor=tk.N)
        b_edit = tk.Button(P_buttons, text="b_edit")
        b_edit.pack(side=tk.LEFT, anchor=tk.N)
        
        b_merge = tk.Button(P_buttons,
                            text="Merge",
                            command=self.sel_file_merge)
        b_merge.pack(side=tk.LEFT, anchor=tk.N)

        b_save = tk.Button(P_buttons, text="b_save")
        b_save.pack(side=tk.RIGHT, anchor=tk.N)
        b_pull = tk.Button(P_buttons, text="b_pull")
        b_pull.pack(side=tk.RIGHT, anchor=tk.N)
        b_push = tk.Button(P_buttons, text="b_push")
        b_push.pack(side=tk.RIGHT, anchor=tk.N)
        
    def populate_source_tree(self):
        """feed the source list"""
        self.f_sources.config(text="%d source(s)"%len(self.manager.codex))
        
        #clean the tree
        self.tree.delete(*self.tree.get_children())

        #get field list and set columns
        fields = self.manager.get_fields()
        #fields.remove('forms')
        self.tree["columns"]=(' '.join(map(lambda string: '"%s"'%string,
                                           fields)))
        for field in fields:
            self.tree.heading(field, text=field)
            
        for source in sorted(self.manager.codex):
            values = ""
            for field in fields:
                if field in self.manager.codex[source]:
                    values += '"%s" '%self.manager.codex[source][field]
                else:
                    values += '" " '
            id_line = self.tree.insert("", "end", text=source, values=values)
            
            
    def sel_file_merge(self):
        message = "Select a codex.json, support.publi or codex.cfg file"
        filename = fd.askopenfilename(title=message,
                                      filetypes=[('json, publi or cfg',
                                                  '*json *.publi *.cfg'),
                                                 ('All files','*.*')])

        if os.path.splitext(filename)[1] == '.publi':
            candidate = parse_supports_publi(filename)
        elif os.path.splitext(filename)[1] == '.cfg':
            candidate = parse_codex_cfg(filename)
            
        self.manager.merge_codex(candidate)
        self.populate_source_tree()

