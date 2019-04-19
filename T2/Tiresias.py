# Author Josquin Debaz
# GPL 3

import urllib.request
import time
import webbrowser
import tkinter as tk

import views.V_list_txt
import views.V_cleaning
import views.V_filter
import views.V_QP
import views.V_Europresse

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

        PRCmodif = self.addmenu("Project")
        PRCmodif.add_command(label="Filter",
                             command=self.C_filter)

        PRCmodif = self.addmenu("Databases")
        PRCmodif.add_command(label="Questions parlementaires",
                             command=self.C_QP)
        PRCmodif.add_command(label="Europresse",
                             command=self.C_EP)
        
    def addmenu(self, lab):
        men = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=lab, menu=men)
        return men

    def C_list_txt(self):
        self.reset_view()
        views.V_list_txt.V_list_txt(self)
        
    def C_cleaning(self):
        self.reset_view()
        views.V_cleaning.V_cleaning(self)

    def C_filter(self):
        self.reset_view()
        views.V_filter.V_filter(self)
        
    def C_QP(self):
        self.reset_view()
        views.V_QP.V_QP(self)

    def C_EP(self):
        self.reset_view()
        views.V_Europresse.V_E(self)
        
    def reset_view(self):
        for p in self.slaves():
            p.destroy()

    def test_version(self):
        try:
            url = "https://raw.githubusercontent.com/josquin\
debaz/Tiresias/master/CHANGELOG.txt"
            with urllib.request.urlopen(url) as p:
                b = p.read()
                last = time.strptime(b[:10].decode('ascii'), "%d/%m/%Y")
            with open("CHANGELOG.txt", 'rb') as f:
                bl = f.read().decode()
                print(bl)
                loc = time.strptime(bl[:10], "%d/%m/%Y")
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
