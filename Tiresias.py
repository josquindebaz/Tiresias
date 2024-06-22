# Author Josquin Debaz
# GPL 3

import urllib.request
import re
import time
import webbrowser
import tkinter as tk
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
import views.heatmap
import views.capitals
import views.openbooks
import views.convert


def get_new_version():
    webbrowser.open("https://github.com/josquindebaz/Tiresias", 0, True)


def check_for_update():
    try:
        last_on_remote = get_last_on_remote()
        last_on_local = get_last_on_local()

        if last_on_remote > last_on_local:
            return "A new version is available"

        return "Your version is up to date"

    except Exception as e:
        return "Can't retrieve last version: %s" % e


def get_last_on_remote():
    url = "https://raw.githubusercontent.com/josquindebaz/Tiresias/master/CHANGELOG.txt"
    with urllib.request.urlopen(url) as page:
        buf = page.read().decode()
    return time.strptime(re.findall(r"\d{2}/\d{2}/\d{4}", buf)[0], "%d/%m/%Y")


def get_last_on_local():
    with open("CHANGELOG.txt", 'rb') as file:
        buf = file.read().decode()
    buf = "test"
    return time.strptime(re.findall(r"\d{2}/\d{2}/\d{4}", buf)[0], "%d/%m/%Y")


class MainView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Tirésias")
        self.protocol('WM_DELETE_WINDOW', self.parent.destroy)

        with open("README.md", 'rb') as f:
            welcome_txt = f.read().decode()
        welcome_txt = "test"
        welcome_txt = re.sub(r"[\r\n]+", "\n", welcome_txt)
        welcome = tk.Message(self,
                             bg="white",
                             width=1024,
                             text=welcome_txt)
        welcome.pack()

        self.update_string = tk.StringVar()
        version = tk.Label(self, textvariable=self.update_string)
        version.pack()
        self._thread = Thread(target=self.show_update())
        self._thread.start()

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        file_menu = self.add_menu("Files")
        file_menu.add_command(label="List .txt",
                              command=self.corrector_list_txt)
        file_menu.add_command(label="Go to code repository",
                              command=get_new_version)
        file_menu.add_command(label="Quit",
                              command=self.parent.destroy)

        corrector_menu = self.add_menu("Corrections")
        corrector_menu.add_command(label="Character cleaning",
                                   command=self.corrector_cleaning)
        corrector_menu.add_command(label="Word replace",
                                   command=self.corrector_replace)
        corrector_menu.add_command(label="Case change",
                                   command=self.corrector_case_change)

        prc_menu = self.add_menu("Projects")
        prc_menu.add_command(label="Filter",
                             command=self.corrector_filter)

        database_menu = self.add_menu("Databases")
        database_menu.add_command(label=u"Questions parlementaires",
                                  command=self.database_qp)
        database_menu.add_command(label="Europresse",
                                  command=self.database_europresse)
        database_menu.add_command(label="Scopus",
                                  command=self.database_scopus)
        database_menu.add_command(label="Factiva",
                                  command=self.database_factiva)
        database_menu.add_command(label="Lexis Nexis",
                                  command=self.database_lexis)
        database_menu.add_command(label="Newton",
                                  command=self.database_newton)
        database_menu.add_command(label="books.openedition",
                                  command=self.database_openbooks)

        dataviz_menu = self.add_menu("Dataviz")
        dataviz_menu.add_command(label="QP Atlas",
                                 command=self.dataviz_qp_atlas)
        dataviz_menu.add_command(label="Cited years timeline",
                                 command=self.dataviz_cited_years)
        dataviz_menu.add_command(label="Month heatmap",
                                 command=self.dataviz_heatmap)

        conversion_menu = self.add_menu("Conversions")
        conversion_menu.add_command(label="Convert csv to txt/ctx",
                                    command=self.convert_convert)

    def add_menu(self, lab):
        menu = tk.Menu(self.menubar,
                       tearoff=0)
        self.menubar.add_cascade(label=lab,
                                 menu=menu)
        return menu

    def corrector_list_txt(self):
        self.reset_view()
        views.listtxt.ViewListTxt(self)

    def corrector_cleaning(self):
        self.reset_view()
        views.cleaning.ViewCleaning(self)

    def corrector_replace(self):
        self.reset_view()
        views.wordreplace.ViewReplacer(self)

    def corrector_case_change(self):
        self.reset_view()
        views.capitals.ViewCap(self)

    def corrector_filter(self):
        self.reset_view()
        views.filter.ViewFilter(self)

    def database_qp(self):
        self.reset_view()
        views.qp.ViewQP(self)

    def database_europresse(self):
        self.reset_view()
        views.europresse.ViewEuropresse(self)

    def database_scopus(self):
        self.reset_view()
        views.scopus.ViewScopus(self)

    def database_factiva(self):
        self.reset_view()
        views.factiva.ViewFactiva(self)

    def database_lexis(self):
        self.reset_view()
        views.lexis.ViewLexis(self)

    def database_newton(self):
        self.reset_view()
        views.newton.ViewNewton(self)

    def database_openbooks(self):
        self.reset_view()
        views.openbooks.ViewOpenbooks(self)

    def dataviz_qp_atlas(self):
        self.reset_view()
        views.qpmap.ViewPaster(self)

    def dataviz_cited_years(self):
        self.reset_view()
        views.cited_years.ViewYears(self)

    def dataviz_heatmap(self):
        self.reset_view()
        views.heatmap.ViewPaster(self)

    def convert_convert(self):
        self.reset_view()
        views.convert.ViewConvert(self)

    def reset_view(self):
        for process in self.slaves():
            process.destroy()

    def show_update(self):
        self.update_string.set("Checking for a newer version")
        self.update_string.set(check_for_update())


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = MainView(root)
    root.mainloop()
