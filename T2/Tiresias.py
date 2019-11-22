# Author Josquin Debaz
# GPL 3

import urllib.request
import re
import time
import webbrowser
import tkinter as tk

import views.listtxt
import views.cleaning
import views.filter
import views.qp
import views.europresse
import views.wordreplace
import views.qpmap


class MainView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Tirésias")
        self.protocol('WM_DELETE_WINDOW', self.parent.destroy)

        with open("README.md", 'rb') as f:
            welcome_txt = f.read().decode()
        welcome = tk.Message(self, bg="white", text=welcome_txt)
        welcome.pack()

        test = self.test_version()
        if (test):
            if (test == -1):
                version = tk.Label(self, text="Can't retrieve last version")
            else:
                version = tk.Button(self,
                    text="A new version is avalaible on \
https://github.com/josquindebaz/Tiresias",
                    foreground="red", 
                    command=self.get_new_version )
        else:
            version = tk.Label(self, text="Your version is up to date")
        version.pack()

   
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        Files = self.addmenu("Files")
        Files.add_command(label="List .txt", command=self.C_list_txt)
        Files.add_command(label="Quit", command=self.parent.destroy)

        Corrector = self.addmenu("Corrections")
        Corrector.add_command(label="Character cleaning",
            command=self.C_cleaning)
        Corrector.add_command(label="Word replace",
            command=self.Word_Replace)
        
        PRCmodif = self.addmenu("Projects")
        PRCmodif.add_command(label="Filter",
                             command=self.C_filter)

        PRCmodif = self.addmenu("Databases")
        PRCmodif.add_command(label="Questions parlementaires",
                             command=self.C_QP)
        PRCmodif.add_command(label="Europresse",
                             command=self.C_EP)

        Viz = self.addmenu("Dataviz")
        Viz.add_command(label="QP Atlas",
                        command=self.QpAtlas)
        
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

    def QpAtlas(self):
        self.reset_view()
        views.qpmap.ViewPaster(self)

        
    def reset_view(self):
        for p in self.slaves():
            p.destroy()

    def test_version(self):
        try:
            url = "https://raw.githubusercontent.com/josquindebaz/Tiresias/master/T2/CHANGELOG.txt"
            #https://raw.githubusercontent.com/josquindebaz/Tiresias/master/CHANGELOG.txt"
            with urllib.request.urlopen(url) as p:
                b = p.read().decode()
                last = time.strptime(re.findall("\d{2}/\d{2}/\d{4}",  b)[0], "%d/%m/%Y")
            with open("CHANGELOG.txt", 'rb') as f:
                bl = f.read().decode()
                loc = time.strptime(re.findall("\d{2}/\d{2}/\d{4}", bl)[0], "%d/%m/%Y")
            if last > loc:
                return 1
            else:
                return 0
        except:
            return -1

    def get_new_version(self):
        webbrowser.open("https://github.com/josquindebaz/Tiresias", 0, 1)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = MainView(root)
    root.mainloop()
