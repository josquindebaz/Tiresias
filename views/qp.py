import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

import webbrowser
import time

from mod.qp import *
from mod.cleaning import Cleaner


class ViewQP:
    def __init__(self, parent):
        self.AssListQ = None
        self.SenatListQ = None
        self.dicQ = None
        self.parent = parent
        window_title = tk.Label(self.parent, text="Questions parlementaires",
                                font=("Helvetica", 12, "bold"))
        window_title.pack(fill=tk.X)

        # Frame keywords
        fr_kw = tk.Frame(self.parent)
        fr_kw.pack(anchor=tk.W)
        lab_kw = tk.Label(fr_kw, text="keywords")
        lab_kw.pack(side=tk.LEFT)
        self.KW_entry = tk.Entry(fr_kw, width=62)
        self.KW_entry.pack(side=tk.LEFT)
        bn_search = tk.Button(fr_kw, text="Search",
                              command=self.search)
        bn_search.pack(side=tk.LEFT)

        # Frame specific parameters
        fr2 = tk.PanedWindow(self.parent)
        fr2.pack(fill=tk.X)

        # Frame Sénat
        fr_senat = tk.LabelFrame(fr2, text="Sénat", borderwidth=1)
        fr_senat.pack(side=tk.LEFT, anchor="n", padx=5)

        lab_from = tk.Label(fr_senat, text="from")
        lab_from.pack(anchor="w")
        self.entrFrom = tk.Entry(fr_senat)
        self.entrFrom.pack(anchor="w")
        self.entrFrom.insert(0, "20/06/2017")
        lab_to = tk.Label(fr_senat, text="to")
        lab_to.pack(anchor="w")
        self.entrTo = tk.Entry(fr_senat)
        self.entrTo.pack(anchor="w")
        self.entrTo.insert(0, time.strftime("%d/%m/%Y"))

        fr_slb = tk.Frame(fr_senat)
        fr_slb.pack(pady=(67, 0))
        self.Senat_list = tk.Listbox(fr_slb,
                                     height=20, width=100, selectmode=tk.EXTENDED)
        self.Senat_list.pack(side=tk.LEFT)
        sb_s = tk.Scrollbar(fr_slb)
        sb_s.pack(side=tk.RIGHT, fill=tk.Y)
        sb_s.configure(command=self.Senat_list.yview)
        self.Senat_list.configure(yscrollcommand=sb_s.set)
        self.Senat_list.bind('<Double-Button-1>', self.senat_dc)

        # Frame Assemblée
        fr_ass = tk.LabelFrame(fr2,
                               text="Assemblée", borderwidth=1)
        fr_ass.pack(side=tk.LEFT, padx=5)

        self.Ass_legs_list = tk.Listbox(fr_ass,
                                        width=30, height=9, selectmode=tk.EXTENDED)

        self.Ass_legs_list.pack(anchor='nw')
        [self.Ass_legs_list.insert('end',
                                   leg) for leg in [
             "7e : 02/07/1981 - 01/04/1986",
             "8e : 02/04/1986 - 14/05/1988",
             "9e : 23/06/1988 - 01/04/1993",
             "10e : 02/04/1993 - 21/04/1997",
             "11e : 01/06/1997 - 18/06/2002",
             "12e : 19/06/2002 - 19/06/2007",
             "13e : 20/06/2007 - 19/06/2012",
             "14e : 20/06/2012 - 20/06/2017",
             "15e : 20/06/2017 -"
         ]
         ]
        self.Ass_legs_list.selection_set(first=8)

        fr_alb = tk.Frame(fr_ass)
        fr_alb.pack()
        self.Ass_list = tk.Listbox(fr_alb,
                                   height=20, width=100, selectmode=tk.EXTENDED)
        self.Ass_list.pack(side=tk.LEFT)
        sb_a = tk.Scrollbar(fr_alb)
        sb_a.pack(side=tk.RIGHT, fill=tk.Y)
        sb_a.configure(command=self.Ass_list.yview)
        self.Ass_list.configure(yscrollcommand=sb_a.set)
        self.Ass_list.bind('<Double-Button-1>', self.ass_dc)

        # progressbar
        self.progressbar = ttk.Progressbar(self.parent)
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        # file parameters and logs
        fr3 = tk.Frame(self.parent)
        fr3.pack()

        bn_dir = tk.Button(fr3, text=u"Corpus File Directory",
                           command=self.sel_dir)
        bn_dir.pack(side=tk.LEFT, anchor="n")
        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(fr3, width=52,
                             textvariable=self.choosenDir)
        dir_entry.pack()

        self.CleaningVal = tk.BooleanVar()
        bn_cleaning = tk.Checkbutton(fr3,
                                     text="clean texts",
                                     variable=self.CleaningVal)
        bn_cleaning.select()
        bn_cleaning.pack(side=tk.LEFT)

        bn_process = tk.Button(fr3,
                               text="Process selected questions",
                               command=self.process)
        bn_process.pack(anchor='e')

        fr4 = tk.Frame(self.parent)
        fr4.pack()
        self.log = ScrolledText(fr4, height=10, bg="black", fg="orange")
        self.log.pack()

    def sel_dir(self):
        self.choosenDir.set("")
        dir = filedialog.askdirectory(title=u"Choose directory",
                                      initialdir=r"C:\corpus")
        self.choosenDir.set(dir)

    def search(self):
        kw = self.KW_entry.get()
        senat_from = self.entrFrom.get()
        senat_to = self.entrTo.get()
        ass_legs = self.Ass_legs_list.curselection()
        ass_legs = [str(l + 7) for l in ass_legs]

        if kw:
            self.dicQ = {}
            self.Senat_list.delete(0, 'end')
            self.Ass_list.delete(0, 'end')

            self.search_senat(kw, senat_from, senat_to)
            self.search_ass(kw, ass_legs)

        else:
            self.log.insert(1.0, "No keyword\n")

    def search_senat(self, kw, f, t):
        self.log.insert(1.0,
                        f"Searching for [{kw}] in Sénat DB from {f} to {t})")
        self.parent.update()
        senat_crawler = CrawlSenat(kw, f, t)
        self.log.insert(1.0, "Found %s question(s)\n" % len(senat_crawler.dicQ))
        self.SenatListQ = []
        for k, e in senat_crawler.dicQ.items():
            self.dicQ[k] = e
            self.SenatListQ.append(k)
            item = "%s %s" % (e['date'], e['number'])
            item += "+R   " if (e['response']) else "   "
            item += "%s : %s" % (e['senator'], e['title'])
            self.Senat_list.insert("end", item)
            self.parent.update()

    def senat_dc(self, _):
        current_selection = self.Senat_list.curselection()
        if len(current_selection) == 1:
            q = self.SenatListQ[int(current_selection[0])]
            url = "https://www.senat.fr/basile/visio.do?id=%s" % q
            webbrowser.open(url, 0, True)

    def search_ass(self, kw, legs):
        self.AssListQ = []
        for leg in legs:
            self.log.insert(1.0,
                            f"Searching for [{kw}] in Assemblée DB for legislation {leg}\n")
            self.parent.update()
            ass_crawler = CrawlAss(leg, kw)
            self.log.insert(1.0, "Found %s question(s)\n" % len(ass_crawler.dicQ))
            for k in sorted(ass_crawler.dicQ.keys(),
                            key=lambda x: time.strptime(ass_crawler.dicQ[x]['date'], "%d/%m/%Y")):
                e = ass_crawler.dicQ[k]
                self.dicQ[k] = e
                self.AssListQ.append(k)
                item = "%s %s" % (e['date'], e['number'])
                item += "+R   " if (e['response']) else "   "
                item += "%s : %s" % (e['depute'], e['title'])
                self.Ass_list.insert("end", item)
                self.parent.update()

    def ass_dc(self, _):
        ass_current_selection = self.Ass_list.curselection()
        if len(ass_current_selection) == 1:
            q = self.AssListQ[int(ass_current_selection[0])]
            url = "http://questions.assemblee-nationale.fr/%s.htm" % q
            webbrowser.open(url, 0, True)

    def process(self):
        self.progressbar['mode'] = 'determinate'
        destination = self.choosenDir.get()
        cl = self.CleaningVal.get()
        if destination:
            l_sen = self.Senat_list.curselection()
            if len(l_sen):
                self.progressbar['maximum'] = len(l_sen)
                for c in l_sen:
                    self.progressbar['value'] = c + 1
                    q = self.SenatListQ[c]
                    self.log.insert(1.0,
                                    "Processing question %s\n" % q)
                    pq = QuestionParlementaire(self.dicQ[q]['url'])
                    pq.retreive()

                    if cl:
                        pq.D['question'] = self.clean(pq.D['question'])
                        pq.D['title'] = self.clean(pq.D['title'])
                        if 'reponse' in pq.D:
                            pq.D['reponse'] = self.clean(pq.D['reponse'])

                    pq.process(dest=destination)
                    self.parent.update()

            l_ass = self.Ass_list.curselection()
            if len(l_ass):
                self.progressbar['maximum'] = len(l_ass)
                for c in l_ass:
                    self.progressbar['value'] = c + 1
                    q = self.AssListQ[c]
                    self.log.insert(1.0,
                                    "Processing question %s\n" % q)
                    pq = QuestionParlementaire(self.dicQ[q]['url'])
                    pq.retreive()

                    if cl:
                        pq.D['question'] = self.clean(pq.D['question'])
                        pq.D['title'] = self.clean(pq.D['title'])
                        if 'reponse' in pq.D:
                            pq.D['reponse'] = self.clean(pq.D['reponse'])

                    try:
                        pq.process(dest=destination)
                    except:
                        self.log.insert(1.0,
                                        "Problem with question %s\n" % q)
                    self.parent.update()
        else:
            self.log.insert(1.0, "Need a destination directory\n")

    def clean(self, text):
        text = text.encode('latin-1', 'xmlcharrefreplace')  # to bytes
        c = Cleaner(text)
        return c.content
