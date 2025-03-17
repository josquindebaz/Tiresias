# Author Josquin Debaz
# GPL 3

import sys
import urllib.request
import re
import time
import webbrowser
import tkinter as tk
from tkinterweb import HtmlFrame
from threading import Thread

import markdown


from views import (
    listtxt,
    cleaning,
    filter,
    qp,
    europresse,
    wordreplace,
    qpmap,
    scopus,
    factiva,
    lexis,
    newton,
    cited_years,
    heatmap,
    capitals,
    openbooks,
)
from views.conversions import (
    convert_encode_decode,
    convert_tiresias_to_gargantext,
    convert_to_factiva,
)


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
    with open("CHANGELOG.txt", "rb") as file:
        buf = file.read().decode()
    return time.strptime(re.findall(r"\d{2}/\d{2}/\d{4}", buf)[0], "%d/%m/%Y")


class MainView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Tirésias")
        self.protocol("WM_DELETE_WINDOW", self.parent.destroy)

        self.attributes("-fullscreen", False)
        self.bind("<Escape>", self.exit_fullscreen)

        with open("tiresias/README.md", "r", encoding="utf-8") as f:
            md_text = f.read()

        html_content = markdown.markdown(md_text)

        frame = HtmlFrame(self, messages_enabled=False)
        frame.load_html(html_content)
        frame.pack(fill="both", expand=True)

        self.update_string = tk.StringVar()
        version = tk.Label(self, textvariable=self.update_string)
        version.pack()
        self._thread = Thread(target=self.show_update())
        self._thread.start()

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        file_menu = self.add_menu("Files")
        file_menu.add_command(label="List .txt", command=self.corrector_list_txt)
        file_menu.add_command(label="Go to code repository", command=get_new_version)
        file_menu.add_command(label="Quit", command=self.parent.destroy)

        corrector_menu = self.add_menu("Corrections")
        corrector_menu.add_command(
            label="Character cleaning", command=self.corrector_cleaning
        )
        corrector_menu.add_command(label="Word replace", command=self.corrector_replace)
        corrector_menu.add_command(
            label="Case change", command=self.corrector_case_change
        )

        prc_menu = self.add_menu("Projects")
        prc_menu.add_command(label="Filter", command=self.corrector_filter)

        database_menu = self.add_menu("Databases")
        database_menu.add_command(
            label="Questions parlementaires", command=self.database_qp
        )
        database_menu.add_command(label="Europresse", command=self.database_europresse)
        database_menu.add_command(label="Scopus", command=self.database_scopus)
        database_menu.add_command(label="Factiva", command=self.database_factiva)
        database_menu.add_command(label="Lexis Nexis", command=self.database_lexis)
        database_menu.add_command(label="Newton", command=self.database_newton)
        database_menu.add_command(
            label="books.openedition", command=self.database_openbooks
        )

        dataviz_menu = self.add_menu("Dataviz")
        dataviz_menu.add_command(label="QP Atlas", command=self.dataviz_qp_atlas)
        dataviz_menu.add_command(
            label="Cited years timeline", command=self.dataviz_cited_years
        )
        dataviz_menu.add_command(label="Month heatmap", command=self.dataviz_heatmap)

        conversion_menu = self.add_menu("Conversions")
        conversion_menu.add_command(
            label="Convert csv to txt/ctx", command=self.convert_convert
        )
        conversion_menu.add_command(
            label="Encode/decode file from TYPE to TYPE",
            command=self.convert__encode_decode,
        )
        conversion_menu.add_command(
            label="Convert csv-factiva to tsv-gargantext",
            command=self.convert__tiresias_to_gargantext,
        )

    def exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)
        self.center_window(1100, 500)

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def add_menu(self, lab):
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=lab, menu=menu)
        return menu

    def corrector_list_txt(self):
        self.reset_view()
        listtxt.ViewListTxt(self)

    def corrector_cleaning(self):
        self.reset_view()
        cleaning.ViewCleaning(self)

    def corrector_replace(self):
        self.reset_view()
        wordreplace.ViewReplacer(self)

    def corrector_case_change(self):
        self.reset_view()
        capitals.ViewCap(self)

    def corrector_filter(self):
        self.reset_view()
        filter.ViewFilter(self)

    def database_qp(self):
        self.reset_view()
        qp.ViewQP(self)

    def database_europresse(self):
        self.reset_view()
        europresse.ViewEuropresse(self)

    def database_scopus(self):
        self.reset_view()
        scopus.ViewScopus(self)

    def database_factiva(self):
        self.reset_view()
        factiva.ViewFactiva(self)

    def database_lexis(self):
        self.reset_view()
        lexis.ViewLexis(self)

    def database_newton(self):
        self.reset_view()
        newton.ViewNewton(self)

    def database_openbooks(self):
        self.reset_view()
        openbooks.ViewOpenbooks(self)

    def dataviz_qp_atlas(self):
        self.reset_view()
        qpmap.ViewPaster(self)

    def dataviz_cited_years(self):
        self.reset_view()
        cited_years.ViewYears(self)

    def dataviz_heatmap(self):
        self.reset_view()
        heatmap.ViewPaster(self)

    def convert_convert(self):
        self.reset_view()
        convert_to_factiva.ViewConvert(self)

    def convert__encode_decode(self):
        self.reset_view()
        self.minsize(800, 400)

        convert_encode_decode.ViewConvertEncodeDecode(self)

    def convert__tiresias_to_gargantext(self):
        self.reset_view()
        convert_tiresias_to_gargantext.ViewConvertTiresiasToGargantext(self)

    def reset_view(self):
        for process in self.slaves():
            process.destroy()

    def show_update(self):
        self.update_string.set("Checking for a newer version")
        self.update_string.set(check_for_update())


root = None


def long_task():
    for i in range(5):
        print(f"Long task running: {i + 1}")
        time.sleep(1)

    root.after(0, update_label)


def update_label():
    label.config(text="Long task completed!")


def create_app():
    global label

    try:
        root = tk.Tk()
        root.withdraw()

        app = MainView(root)

        start_button = tk.Button(app, text="Start Long Task", command=start_long_task)
        start_button.pack()

        root.mainloop()
    except Exception as e:
        print("Application terminated by user.")
        root.destroy()
        sys.exit(0)


def start_long_task():
    thread = Thread(target=long_task, daemon=True)
    thread.start()


if __name__ == "__main__":
    create_app()
