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
        self.fields = []
        
        w_title = tk.Label(parent,
                           text="Codex management",
                           font=("Helvetica", 12, "bold"))
        w_title.pack(fill=tk.X)

        self.f_sources = tk.LabelFrame(parent,
                                  text="Sources",
                                  padx=10,
                                  background='red')
        self.f_sources.pack()
        
        p_top = tk.PanedWindow(self.f_sources,
                               background='blue')
        p_top.pack()
        
        vsb = ttk.Scrollbar(p_top,
                            orient="vertical",)
        self.tree = ttk.Treeview(p_top,
                                 selectmode="browse",
                                 height=10,
                                 yscrollcommand = vsb.set)
        self.tree.heading("#0", text="radical")
        self.tree.column("#0", width=60)
        self.tree.pack(side=tk.LEFT)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        vsb.config(command=self.tree.yview)
        vsb.pack(side=tk.LEFT, fill=tk.Y)

        self.populate_source_tree()


        p_buttons = tk.PanedWindow(self.f_sources,
                                   background='yellow')
        p_buttons.pack(fill=tk.X)

        b_search = tk.Button(p_buttons, text="Search")
        b_search.pack(side=tk.LEFT, anchor=tk.N)
        b_add = tk.Button(p_buttons, text="b_add")
        b_add.pack(side=tk.LEFT, anchor=tk.N)
        b_del = tk.Button(p_buttons, text="b_del")
        b_del.pack(side=tk.LEFT, anchor=tk.N)
        b_edit = tk.Button(p_buttons, text="b_edit")
        b_edit.pack(side=tk.LEFT, anchor=tk.N)
        
        b_merge = tk.Button(p_buttons,
                            text="Merge",
                            command=self.sel_file_merge)
        b_merge.pack(side=tk.LEFT, anchor=tk.N)

        b_save = tk.Button(p_buttons, text="b_save")
        b_save.pack(side=tk.RIGHT, anchor=tk.N)
        b_pull = tk.Button(p_buttons, text="b_pull")
        b_pull.pack(side=tk.RIGHT, anchor=tk.N)
        b_push = tk.Button(p_buttons, text="b_push")
        b_push.pack(side=tk.RIGHT, anchor=tk.N)

        p_details = tk.PanedWindow(self.f_sources,
                                   background='cyan')
        p_details.pack(fill=tk.X)
        self.tree_details = ttk.Treeview(p_details, height=11)
        self.tree_details.pack(side=tk.LEFT)
        self.tree_details.heading("#0", text="field")
        self.tree_details["columns"]=("values")
        self.tree_details.heading("values", text="values")
        self.tree_details.bind("<Double-1>", self.tree_details_event)

        
    def populate_source_tree(self):
        """feed the source list"""
        self.f_sources.config(text="%d source(s)"%len(self.manager.codex))
        
        #clean the tree
        self.tree.delete(*self.tree.get_children())

        #get field list and set columns
        self.fields = self.manager.get_fields()
        self.tree["columns"]=(' '.join(map(lambda string: '"%s"'%string,
                                           self.fields)))
        for field in self.fields:
            self.tree.heading(field, text=field)
            if field == 'forms':
                self.tree.column(field, width=200)
            else:
                self.tree.column(field, width=120)
            
        for source in sorted(self.manager.codex):
            values = ""
            for field in self.fields:
                if field in self.manager.codex[source]:
                    if field == 'forms':
                        values += '"%s" '%\
                                  "|".join(self.manager.codex[source][field])
                    else:
                        values += '"%s" '%self.manager.codex[source][field]
                else:
                    values += '" " '
            self.tree.insert("", "end", text=source, values=values)
            
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
        
    def on_tree_select(self, event):
        """selected on first tree populate the detailed list"""
        self.tree_details.delete(*self.tree_details.get_children())

        current = self.tree.item(self.tree.focus())
        self.tree_details.insert("", "end",
                                 text="radical",
                                 values=current['text'])
        for index, value in enumerate(current['values']):
            self.tree_details.insert("", "end",
                                 text=self.fields[index],
                                 values=(value,) )           

    def tree_details_event(self, event):
        item = self.tree_details.selection()[0]
        print("you clicked on", self.tree_details.item(item,"text")
)
