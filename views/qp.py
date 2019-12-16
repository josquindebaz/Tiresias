import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

import webbrowser
import time

from mods.qp import *
from mods.cleaning import Cleaner

class ViewQP():
    def __init__(self, parent):
        self.parent = parent
        WindowTitle = tk.Label(self.parent, text="Questions parlementaires",
            font=("Helvetica", 12, "bold"))
        WindowTitle.pack(fill=tk.X)

        #Frame keywords
        Fr_kw = tk.Frame(self.parent)
        Fr_kw.pack(anchor=tk.W)
        labKW = tk.Label(Fr_kw, text="keywords")
        labKW.pack(side=tk.LEFT)
        self.KW_entry = tk.Entry(Fr_kw, width=62)
        self.KW_entry.pack(side=tk.LEFT)
        bn_Search=tk.Button(Fr_kw, text="Search",
                            command=self.Search)
        bn_Search.pack(side=tk.LEFT)

        #Frame specific parameters
        Fr2 = tk.PanedWindow(self.parent)
        Fr2.pack(fill=tk.X)

        #Frame Sénat
        Fr_Senat = tk.LabelFrame(Fr2, text="Sénat", borderwidth=1)
        Fr_Senat.pack(side=tk.LEFT, anchor="n", padx=5)

        labFrom = tk.Label(Fr_Senat, text="from")
        labFrom.pack(anchor="w")
        self.entrFrom = tk.Entry(Fr_Senat)
        self.entrFrom.pack(anchor="w")
        self.entrFrom.insert(0, "20/06/2017")
        labTo = tk.Label(Fr_Senat, text="to")
        labTo.pack(anchor="w")
        self.entrTo = tk.Entry(Fr_Senat)
        self.entrTo.pack(anchor="w")
        self.entrTo.insert(0, time.strftime("%d/%m/%Y" ))

        FrSLB = tk.Frame(Fr_Senat)
        FrSLB.pack(pady=(67, 0))
        self.Senat_list=tk.Listbox(FrSLB,
                            height=20, width=100, selectmode=tk.EXTENDED)
        self.Senat_list.pack(side=tk.LEFT)
        SbS = tk.Scrollbar(FrSLB)
        SbS.pack(side=tk.RIGHT, fill=tk.Y)
        SbS.configure(command=self.Senat_list.yview)
        self.Senat_list.configure(yscrollcommand=SbS.set)
        self.Senat_list.bind('<Double-Button-1>', self.Senat_DC)

        #Frame Assemblée
        Fr_Ass = tk.LabelFrame(Fr2, 
            text="Assemblée", borderwidth=1)
        Fr_Ass.pack(side=tk.LEFT, padx=5)

        self.Ass_legs_list = tk.Listbox(Fr_Ass,
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

        FrALB = tk.Frame(Fr_Ass)
        FrALB.pack()
        self.Ass_list=tk.Listbox(FrALB,
                         height=20, width=100, selectmode=tk.EXTENDED)
        self.Ass_list.pack(side=tk.LEFT)
        SbA = tk.Scrollbar(FrALB)
        SbA.pack(side=tk.RIGHT, fill=tk.Y)
        SbA.configure(command=self.Ass_list.yview)
        self.Ass_list.configure(yscrollcommand=SbA.set)
        self.Ass_list.bind('<Double-Button-1>', self.Ass_DC)

        #progressbar
        self.progressbar = ttk.Progressbar(self.parent)
        self.progressbar.pack(anchor=tk.W, fill=tk.X)

        #file parameters and logs
        Fr3 = tk.Frame(self.parent)
        Fr3.pack()

        bnDir = tk.Button(Fr3, text=u"Corpus File Directory",
            command=self.sel_dir)
        bnDir.pack(side=tk.LEFT, anchor="n")
        self.choosenDir = tk.StringVar()
        dir_entry = tk.Entry(Fr3, width=52,
            textvariable=self.choosenDir)
        dir_entry.pack()


        self.CleaningVal= tk.BooleanVar()
        Bn_Cleaning = tk.Checkbutton(Fr3,
                        text="clean texts",
                        variable=self.CleaningVal)
        Bn_Cleaning.select()
        Bn_Cleaning.pack(side=tk.LEFT)

        bn_Process=tk.Button(Fr3,
                             text="Process selected questions",
                             command=self.process )
        bn_Process.pack(anchor='e')

        Fr4 = tk.Frame(self.parent)
        Fr4.pack()
        self.log = ScrolledText(Fr4, height=10, bg="black", fg="orange")
        self.log.pack()

    def sel_dir(self):
        self.choosenDir.set("")
        dir = filedialog.askdirectory(title=u"Choose directory",
            initialdir="C:\corpus")
        self.choosenDir.set(dir)

    def Search(self):
        kw = self.KW_entry.get()
        Senat_from = self.entrFrom.get()
        Senat_to = self.entrTo.get()
        AssLegs = self.Ass_legs_list.curselection()
        AssLegs = [str(l + 7) for l in AssLegs]

        if (kw):
            self.dicQ = {}
            self.Senat_list.delete(0, 'end')
            self.Ass_list.delete(0, 'end')
          
            self.Search_Senat(kw, Senat_from, Senat_to)
            self.Search_Ass(kw, AssLegs)

        else:
            self.log.insert(1.0, "No keyword\n")

    def Search_Senat(self, kw, f, t):
        self.log.insert(1.0,
            "Searching for [%s] in Sénat DB from %s to %s)"\
            %(kw, f, t))
        self.parent.update()
        S = CrawlSenat(kw, f, t)
        self.log.insert(1.0, "Found %s question(s)\n"%len(S.dicQ))
        self.SenatListQ = []
        for k, e in S.dicQ.items():
            self.dicQ[k] = e
            self.SenatListQ.append(k)
            item = "%s %s" % (e['date'], e['number'])
            item += "+R   " if (e['response']) else "   "
            item += "%s : %s" %(e['senator'], e['title'])                                       
            self.Senat_list.insert("end", item)
            self.parent.update()
        
    def Senat_DC(self, details):
        L = self.Senat_list.curselection()
        if (len(L) == 1) :
            q = self.SenatListQ[int(L[0])]
            url = "https://www.senat.fr/basile/visio.do?id=%s" % q
            webbrowser.open(url, 0, 1)     
            
    def Search_Ass(self, kw, legs):
        self.AssListQ = []
        for leg in legs:
            self.log.insert(1.0,
                "Searching for [%s] in Assemblée DB for legislation %s\n" \
                %(kw, leg) )
            self.parent.update()
            A = CrawlAss(leg, kw)
            self.log.insert(1.0, "Found %s question(s)\n"%len(A.dicQ))
            for k in sorted(A.dicQ.keys(),
                        key=lambda x: time.strptime(A.dicQ[x]['date']
                                                        , "%d/%m/%Y") ):
                e = A.dicQ[k]
                self.dicQ[k] = e
                self.AssListQ.append(k)
                item = "%s %s" % (e['date'], e['number'])
                item += "+R   " if (e['response']) else "   "
                item += "%s : %s" %(e['depute'], e['title'])                                       
                self.Ass_list.insert("end", item)
                self.parent.update()
        
    def Ass_DC(self, details):
        L = self.Ass_list.curselection()
        if (len(L) == 1) :
            q = self.AssListQ[int(L[0])]
            url = "http://questions.assemblee-nationale.fr/%s.htm" % q
            webbrowser.open(url, 0, 1)

    def process(self):
        self.progressbar['mode'] = 'determinate'
        destination = self.choosenDir.get()
        cl = self.CleaningVal.get()
        if (destination):
            LSen = self.Senat_list.curselection()
            if len(LSen) :
                self.progressbar['maximum'] =  len(LSen)
                for c in (LSen):
                    self.progressbar['value'] = c+1
                    q = self.SenatListQ[c]
                    self.log.insert(1.0,
                        "Processing question %s\n"%q )
                    PQ = QuestionParlementaire(self.dicQ[q]['url'])
                    PQ.retreive()
                    
                    if (cl):
                         PQ.D['question'] = self.clean(PQ.D['question'])
                         PQ.D['title'] = self.clean(PQ.D['title'])
                         if ('reponse' in PQ.D):
                             PQ.D['reponse'] = self.clean(PQ.D['reponse'])

                    PQ.process(dest=destination)
                    self.parent.update()

            LAss = self.Ass_list.curselection()
            if len(LAss) :
                self.progressbar['maximum'] =  len(LAss)
                for c in LAss:
                    self.progressbar['value'] = c+1
                    q = self.AssListQ[c]
                    self.log.insert(1.0,
                        "Processing question %s\n"%q )
                    PQ = QuestionParlementaire(self.dicQ[q]['url'])
                    PQ.retreive()
                    
                    if (cl):
                         PQ.D['question'] = self.clean(PQ.D['question'])
                         PQ.D['title'] = self.clean(PQ.D['title'])
                         if ('reponse' in PQ.D):
                             PQ.D['reponse'] = self.clean(PQ.D['reponse'])
                             
                    try:
                        PQ.process(dest=destination)
                    except:
                        self.log.insert(1.0,
                                        "Problem with question %s\n"%q )
                    self.parent.update()        
        else:
            self.log.insert(1.0, "Need a destination directory\n" )            

    def clean(self, text):
        text = text.encode('latin-1', 'xmlcharrefreplace') #to bytes
        c = Cleaner(text)
        return  c.content
