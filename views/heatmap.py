"""Viewer for month heatmap
Josquin Debaz
GPL3
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

from mod.heatmap import parse_data
from mod.heatmap import create_svg

import webbrowser

class ViewPaster():
    """Paste window"""
    def __init__(self, parent):
        self.parent = parent
        windowtitle = tk.Label(parent,
                               text="Month heatmap",
                               font=("Helvetica", 12, "bold"))
        windowtitle.pack(fill=tk.X)

        fr1 = tk.Frame(parent)
        fr1.pack(anchor=tk.W)

        welcome = tk.Message(fr1,
                             bg="white",
                             text="Paste list:month[tabulation]value",
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
                               text="Draw heatmap", command=self.process)
        bn_process.pack(side=tk.LEFT)

        
    def paste_list(self):
        self.reset()
        self.data_list.insert("end", self.data_list.clipboard_get())

    def reset(self):
        self.data_list.delete(1.0, "end")

    def process(self):
        data = self.data_list.get(1.0, "end")
        if (data != "\n"): 
            filename = filedialog.asksaveasfilename(\
                title="Save as",
                initialdir="C:\corpus",
                initialfile="MonthHeatmap.svg",
                filetypes = [("svg Files","*.svg")])

            values = parse_data(data)
            svg = create_svg(values)
            with open(filename, 'wb') as pointer:
                pointer.write(svg.encode('utf-8'))
            webbrowser.open(filename, 0, 1)

