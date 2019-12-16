import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

from mods.cited_years import find_years

class ViewYears():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent,
                               text="Data for cited years timeline",
                               font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        #Frame 1
        Fr1 = tk.Frame(self.parent)
        Fr1.pack(anchor=tk.W)
        welcome = tk.Message(Fr1, bg="white", width=800,
                             font=('times', 16),
                             text="In Prospéro, compute ref_temporelles.frm \
(find it in the frm directory of Tiresias), copy the result of the formula \
\"recup\" and paste it in the left column of this window, \
then click on calculate.\nCopy the transformed data from the right column and \
paste it in your favorite spreadsheet")
        welcome.pack()
        
        #Frame 2
        Fr2 = tk.Frame(self.parent)
        Fr2.pack(anchor=tk.W)
        FrPane = tk.PanedWindow(Fr2)
        FrPane.pack(anchor=tk.W)

        #Frame left
        FrPaste_list = tk.Frame(FrPane)
        FrPaste_list.pack(side=tk.LEFT, anchor=tk.N)
        self.paste_list = ScrolledText(FrPaste_list, width=50)
        self.paste_list.pack()
        bn_paste = tk.Button(FrPaste_list, text="Paste",
                             command=self.paste_from_clipboard)
        bn_paste.pack()
        
        #middle Frame
        FrCalc = tk.Frame(FrPane)
        FrCalc.pack(side=tk.LEFT)
        
        bn_calculate = tk.Button(FrCalc, text="Calculate",
                                 command=self.process)
        bn_calculate.pack(padx=20)

        #Frame right
        FrResult_list = tk.Frame(FrPane)
        FrResult_list.pack(side=tk.RIGHT, anchor=tk.N)
        
        self.result_list = ScrolledText(FrResult_list, width=50)
        self.result_list.pack()
        bn_copy = tk.Button(FrResult_list,
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
                self.result_list.insert("end", "%s\t%s\n"%(year, years[year]))
        except:
            pass
