"""Viewer for question parlementaire map module
Josquin Debaz
GPL3
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

from mod.qpmap import Mapper

import webbrowser


class ViewPaster:
    """Paste window"""

    def __init__(self, parent):
        self.parent = parent
        windowtitle = tk.Label(parent,
                               text="QP Atlas",
                               font=("Helvetica", 12, "bold"))
        windowtitle.pack(fill=tk.X)

        fr1 = tk.Frame(parent)
        fr1.pack(anchor=tk.W)

        welcome = tk.Message(fr1,
                             bg="white",
                             text="Paste list: department[tabulation]value",
                             width=1000)
        welcome.pack(anchor=tk.W)

        self.data_list = ScrolledText(fr1)
        self.data_list.pack(fill=tk.X)

        fr2 = tk.Frame(parent)
        fr2.pack(anchor=tk.W, fill=tk.X)
        bn_paste = tk.Button(fr2,
                             text="Paste", command=self.paste_list)
        bn_paste.pack(side=tk.LEFT)
        bn_reset = tk.Button(fr2,
                             text="Reset", command=self.reset)
        bn_reset.pack(side=tk.LEFT)

        bn_process = tk.Button(fr2,
                               text="Draw atlas", command=self.process)
        bn_process.pack(side=tk.LEFT)

        fr3 = tk.LabelFrame(fr2, text="Method", borderwidth=1)
        fr3.pack(anchor=tk.E)
        self.method = tk.StringVar()
        r1_method = tk.Radiobutton(fr3,
                                   text="Cumulated fourth",
                                   variable=self.method,
                                   value="cumulated_fourth")
        r1_method.pack(side=tk.LEFT)
        r2_method = tk.Radiobutton(fr3,
                                   text="Quartiles",
                                   variable=self.method,
                                   value="quartiles")
        r2_method.pack(side=tk.LEFT)
        r3_method = tk.Radiobutton(fr3,
                                   text="Quarter",
                                   variable=self.method,
                                   value="fourth")
        r3_method.pack(side=tk.LEFT)
        r4_method = tk.Radiobutton(fr3,
                                   text="Proportional",
                                   variable=self.method,
                                   value="graduated")
        r4_method.pack()
        self.method.set("cumulated_fourth")

    def paste_list(self):
        self.reset()
        self.data_list.insert("end", self.data_list.clipboard_get())

    def reset(self):
        self.data_list.delete(1.0, "end")

    def process(self):
        data = self.data_list.get(1.0, "end")
        if data != "\n":
            filename = filedialog.asksaveasfilename(
                title="Save as",
                initialdir="C:\corpus",
                initialfile="QpAtlas.svg",
                filetypes=[("svg Files", "*.svg")])

            PROCESS = Mapper(data)
            method = self.method.get()
            if method == "graduated":
                atlas = PROCESS.draw_map_graduated()
            else:
                PROCESS.make_legend(method=method)
                atlas = PROCESS.draw_map()
            with open(filename, 'wb') as pointer:
                pointer.write(atlas.encode('utf-8'))
            webbrowser.open(filename, 0, True)
