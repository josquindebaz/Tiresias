import tkinter as tk

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

class MainView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("T2:MVC")
        self.protocol('WM_DELETE_WINDOW', self.
                      parent.destroy)

        #views.newton.ViewNewton(self)
        #views.uncapitalise.ViewReplacer(self)
        views.capitals.ViewCap(self)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = MainView(root)
    root.mainloop()
