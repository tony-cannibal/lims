import tkinter as tk
from ttkbootstrap import Style
import os

from Inventory import InventoryUI
from Start import SartUI
from Admin import AdminUI


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Inventario Wip Feeder')
        self.geometry('800x520')
        self.resizable(False, False)
        self.style = Style('darkly')

        self.rootPath = "/".join(os.getcwd().split("\\"))

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both",
                            expand=True, padx=20, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SartUI.StartPage, InventoryUI.Inventory, AdminUI.Admin):
            # page_name = F.__name__
            # frame = F(parent=container, controller=self, path=self.rootPath)
            # self.frames[page_name] = frame
            #
            # # put all of the pages in the same location;
            # # the one on the top of the stacking order
            # # will be the one that is visible.
            # frame.grid(row=0, column=0, sticky="nsew")
            self.addWindow(F)

        # Show The First Page
        self.show_frame("StartPage")

    def addWindow(self, frame):
        frameName = frame.__name__
        window = frame(parent=self.container,
                       controller=self, path=self.rootPath)
        self.frames[frameName] = window
        window.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.changeGeometry(page_name)
        frame = self.frames[page_name]
        frame.tkraise()

    def changeGeometry(self, window):
        if window == "StartPage":
            self.geometry('800x520')
        if window == "Inventory":
            self.geometry('800x560')


if __name__ == '__main__':
    Application().mainloop()
