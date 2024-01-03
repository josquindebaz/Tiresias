import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from mod.cited_years import find_years


class ViewYears:
    def __init__(self, parent):
        self.parent = parent
        window_title = tk.Label(self.parent,
                                text="Data for cited years timeline",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        # Frame 1
        fr1 = tk.Frame(self.parent)
        fr1.pack(anchor=tk.W)
        welcome = tk.Message(fr1, bg="white", width=800,
                             font=('times', 16),
                             text="In Prospéro, compute ref_temporelles.frm \
(find it in the frm directory of Tiresias), copy the result of the formula \
\"recup\" and paste it in the left column of this window, \
then click on calculate.\nCopy the transformed data from the right column and \
paste it in your favorite spreadsheet")
        welcome.pack()

        # Frame 2
        fr2 = tk.Frame(self.parent)
        fr2.pack(anchor=tk.W)
        fr_pane = tk.PanedWindow(fr2)
        fr_pane.pack(anchor=tk.W)

        # Frame left
        fr_paste_list = tk.Frame(fr_pane)
        fr_paste_list.pack(side=tk.LEFT, anchor=tk.N)
        self.paste_list = ScrolledText(fr_paste_list, width=50)
        self.paste_list.pack()
        bn_paste = tk.Button(fr_paste_list, text="Paste",
                             command=self.paste_from_clipboard)
        bn_paste.pack()

        # middle Frame
        fr_calc = tk.Frame(fr_pane)
        fr_calc.pack(side=tk.LEFT)

        bn_calculate = tk.Button(fr_calc, text="Calculate",
                                 command=self.process)
        bn_calculate.pack(padx=20)

        # Frame right
        fr_result_list = tk.Frame(fr_pane)
        fr_result_list.pack(side=tk.RIGHT, anchor=tk.N)

        self.result_list = ScrolledText(fr_result_list, width=50)
        self.result_list.pack()
        bn_copy = tk.Button(fr_result_list,
                            text="Copy for spreadsheet",
                            command=self.copy_to_clipboard)
        bn_copy.pack()

    def copy_to_clipboard(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.result_list.get(1.0, "end"))

    def paste_from_clipboard(self):
        self.paste_list.delete(1.0, "end")
        self.paste_list.insert("end", self.paste_list.clipboard_get())

    def process(self):
        content = self.paste_list.get(1.0, "end")
        self.result_list.delete(1.0, "end")
        try:
            years = find_years(content)
            for year in sorted(years.keys()):
                self.result_list.insert("end", "%s\t%s\n" % (year, years[year]))
        except:
            pass
