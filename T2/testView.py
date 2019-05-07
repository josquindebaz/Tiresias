import tkinter as tk

import views.V_list_txt
import views.V_cleaning
import views.V_filter
import views.V_QP
import views.V_Europresse
import views.V_W_replace

class MainView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("T2:MVC")
        self.protocol('WM_DELETE_WINDOW', self.
                      parent.destroy)

        #views.V_list_txt.V_list_txt(self)
        #views.V_cleaning.V_cleaning(self)
        #views.V_filter.V_filter(self)
        #views.V_QP.V_QP(self)
        #views.V_Europresse.V_E(self)
        views.V_W_replace.V_WR(self)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = MainView(root)
    root.mainloop()
