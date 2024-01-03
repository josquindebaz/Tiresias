"""Viewer for month heatmap
Josquin Debaz
GPL3
"""

import tkinter as tk
import webbrowser
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

from mod.HeatmapDataProcessor import parse_data, HeatmapDataProcessor
from mod.HeatmapSvgWriter import HeatmapSvgWriter


class ViewPaster:
    """Paste window"""

    def __init__(self, parent):
        self.parent = parent
        window_title = tk.Label(parent,
                                text="Month heatmap", font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        fr1 = tk.Frame(parent)
        fr1.pack(anchor=tk.W)

        welcome = tk.Message(fr1,
                             bg="white", text="Paste list:month[tabulation]value", width=1000)
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
        if data != "\n":
            filename = filedialog.asksaveasfilename(
                title="Save as",
                initialdir=r"C:\corpus",
                initialfile="MonthHeatmap.svg",
                filetypes=[("svg Files", "*.svg")])

            values = parse_data(data)
            data_processor = HeatmapDataProcessor(values)
            svg_writer = HeatmapSvgWriter(data=data_processor)
            svg = svg_writer.produce_svg()

            with open(filename, 'wb') as pointer:
                pointer.write(svg.encode('utf-8'))
            webbrowser.open(filename, 0, True)
