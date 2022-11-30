import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from threading import Thread

from mod.cleaning import list_files


class ViewListTxt:
    def __init__(self, parent):
        self.parent = parent
        window_title = tk.Label(self.parent,
                                text=".txt and .TXT List",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        # Frame 1
        frame1 = tk.Frame(self.parent)
        frame1.pack(anchor=tk.W)

        bn_dir = tk.Button(frame1,
                           text="Select directory",
                           command=self.sel_dir)
        bn_dir.pack(side=tk.LEFT)

        self.chosen_dir = tk.StringVar()
        dir_entry = tk.Entry(frame1,
                             width=52,
                             textvariable=self.chosen_dir)
        self.chosen_dir.set(r"C:\corpus")
        dir_entry.pack(side=tk.LEFT)

        self.Recursive = tk.BooleanVar()
        bn_recursive = tk.Checkbutton(frame1,
                                      text='recursive',
                                      var=self.Recursive)
        bn_recursive.select()
        bn_recursive.pack(side=tk.LEFT)

        bn_action = tk.Button(frame1,
                              text="List",
                              command=self._t_action)
        bn_action.pack(side=tk.LEFT, padx=20)
        bn_copy = tk.Button(frame1,
                            text="Copy",
                            command=self.copy_to_clipboard)
        bn_copy.pack()

        # Frame 2
        frame2 = tk.LabelFrame(self.parent,
                               text="Replace path",
                               borderwidth=1)
        frame2.pack(anchor=tk.W)

        label_from = tk.Label(frame2, text='from')
        label_from.pack(side=tk.LEFT)
        self.EntryFrom = tk.Entry(frame2, width=30)
        self.EntryFrom.pack(side=tk.LEFT)
        label_to = tk.Label(frame2, text='to')
        label_to.pack(side=tk.LEFT)
        self.EntryTo = tk.Entry(frame2, width=30)
        self.EntryTo.pack(side=tk.LEFT)
        self.Slash = tk.BooleanVar()
        bn_slash = tk.Checkbutton(frame2,
                                  padx=30,
                                  text='replace / with \\',
                                  var=self.Slash)
        bn_slash.select()
        bn_slash.pack(side=tk.RIGHT)

        self.progressbar = ttk.Progressbar(self.parent,
                                           mode='indeterminate')
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        self.result = ScrolledText(self.parent)
        self.result.pack(fill=tk.X)

    def sel_dir(self):
        self.chosen_dir.set("")
        self.result.delete(1.0, "end")
        self.progressbar['value'] = 0
        directory = filedialog.askdirectory(title="Choose directory", initialdir=r"C:\corpus")
        self.chosen_dir.set(directory)

    def _t_action(self):
        self._thread = Thread(target=self.action)
        self._thread.start()

    def action(self):
        self.result.delete(1.0, "end")

        rep = self.chosen_dir.get()
        if rep == '':
            self.result.insert(1.0, "No directory selected")
        else:
            self.progressbar.start()

            try:
                fr = self.EntryFrom.get()

                if fr:
                    to = self.EntryTo.get()
                    repl = [fr, to]
                else:
                    repl = []

                slash = True if self.Slash.get() else False

                query = list_files(rep,
                                   [".txt", ".TXT"],
                                   self.Recursive.get(),
                                   slash,
                                   repl)

                if len(query) > 0:
                    self.result.insert(1.0, "\n".join(query))
                else:
                    self.result.insert(1.0, "Nothing found")

            except Exception as e:
                self.result.insert(1.0, "Execution problem: %s" % e)

            self.progressbar.stop()
            self.progressbar['mode'] = 'determinate'
            self.progressbar['value'] = 100

    def copy_to_clipboard(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.result.get(1.0, "end"))
