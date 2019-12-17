# Author Josquin Debaz
# GPL 3

import urllib.request
import re
import time
import webbrowser
import tkinter as tk
import os
from threading import Thread

import views.listtxt
import views.cleaning
import views.filter
import views.qp
import views.europresse
import views.wordreplace
import views.qpmap
import views.scopus
import views.factiva
import views.lexis
import views.newton
import views.cited_years


class MainView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Tirésias")
        self.protocol('WM_DELETE_WINDOW', self.parent.destroy)

        filename = "README.md"
##        if '_MEIPASS2' in os.environ:
##            filename = os.path.join(os.environ['_MEIPASS2'], filename)
        with open(filename, 'rb') as f:
            welcome_txt = f.read().decode()
        welcome = tk.Message(self, bg="white", text=welcome_txt)
        welcome.pack()

        self.update_string = tk.StringVar()
        version = tk.Label(self, textvariable=self.update_string)               
        version.pack()
        self.update_string.set("Checking for a newer version")
        self._thread = Thread(target=self.check_update)
        self._thread.start()
   
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        Files = self.addmenu("Files")
        Files.add_command(label="List .txt", command=self.C_list_txt)
        Files.add_command(label="Go to code repository",
                          command=self.get_new_version)
        Files.add_command(label="Quit", command=self.parent.destroy)

        Corrector = self.addmenu("Corrections")
        Corrector.add_command(label="Character cleaning",
            command=self.C_cleaning)
        Corrector.add_command(label="Word replace",
            command=self.Word_Replace)
        
        PRCmodif = self.addmenu("Projects")
        PRCmodif.add_command(label="Filter",
                             command=self.C_filter)

        PRCdb = self.addmenu("Databases")
        PRCdb.add_command(label="Questions parlementaires",
                             command=self.C_QP)
        PRCdb.add_command(label="Europresse",
                             command=self.C_EP)
        PRCdb.add_command(label="Scopus",
                             command=self.C_scopus)
        PRCdb.add_command(label="Factiva",
                             command=self.C_factiva)
        PRCdb.add_command(label="Lexis Nexis",
                             command=self.C_lexis)
        PRCdb.add_command(label="Newton",
                             command=self.C_newton)
        
        Viz = self.addmenu("Dataviz")
        Viz.add_command(label="QP Atlas",
                        command=self.QpAtlas)
        Viz.add_command(label="Cited years timeline",
                        command=self.cited_years)
        
    def addmenu(self, lab):
        men = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=lab, menu=men)
        return men

    def C_list_txt(self):
        self.reset_view()
        views.listtxt.ViewListTxt(self)
        
    def C_cleaning(self):
        self.reset_view()
        views.cleaning.ViewCleaning(self)

    def Word_Replace(self):
        self.reset_view()
        views.wordreplace.ViewReplacer(self)

    def C_filter(self):
        self.reset_view()
        views.filter.ViewFilter(self)
        
    def C_QP(self):
        self.reset_view()
        views.qp.ViewQP(self)

    def C_EP(self):
        self.reset_view()
        views.europresse.ViewEuropresse(self)

    def C_scopus(self):
        self.reset_view()
        views.scopus.ViewScopus(self)

    def C_factiva(self):
        self.reset_view()
        views.factiva.ViewFactiva(self)

    def C_lexis(self):
        self.reset_view()
        views.lexis.ViewLexis(self)
        
    def C_newton(self):
        self.reset_view()
        views.newton.ViewNewton(self)
        

    def QpAtlas(self):
        self.reset_view()
        views.qpmap.ViewPaster(self)

    def cited_years(self):
        self.reset_view()
        views.cited_years.ViewYears(self)
        
    def reset_view(self):
        for p in self.slaves():
            p.destroy()

    def check_update(self):
        try:
            url = "https://raw.githubusercontent.com/josquindebaz/\
Tiresias/master/CHANGELOG.txt"
            with urllib.request.urlopen(url) as page:
                buf = page.read().decode()
                last = time.strptime(re.findall("\d{2}/\d{2}/\d{4}",
                                                buf)[0], "%d/%m/%Y")
            with open("CHANGELOG.txt", 'rb') as file:
                buf2 = file.read().decode()
                loc = time.strptime(re.findall("\d{2}/\d{2}/\d{4}",
                                               buf2)[0], "%d/%m/%Y")
            if last > loc:
                self.update_string.set("A new version is avalaible")
            else:
                self.update_string.set("Your version is up to date")
        except:
            self.update_string.set("Can't retrieve last version")       

    def get_new_version(self):
        webbrowser.open("https://github.com/josquindebaz/Tiresias", 0, 1)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = MainView(root)
    root.mainloop()
