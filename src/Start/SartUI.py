import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.simpledialog import askstring
from . import functions as fn


class StartPage(ttk.Frame):
    def __init__(self, parent, controller, path):
        super().__init__(parent)

        self.controller = controller
        self.rootPath = path
        self.database = fn.getDatabase(self.rootPath)

        customFont = font.Font(family="Arial", size=40, slant="italic")
        self.label = tk.Label(
            self, text="Inventario Wip Feeder", font=customFont)
        # font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=(150, 20))

        buttonFont = font.Font(family="Arial", size=20, slant="italic")
        self.button1 = tk.Button(self, text="Inicio", font=buttonFont, padx=60,
                                 command=self.showInventory)
        self.button1.pack(pady=10)
        self.button2 = tk.Button(self, text="Opciones",
                                 font=buttonFont, padx=60,
                                 command=self.showAdmin)
        self.button2.pack(pady=10)
        self.statusLabel = tk.Label(self, text="", font="Arial 14", fg="red")
        self.statusLabel.pack()

    def showInventory(self):
        isActive = fn.getActiveStatus(self.database)
        if isActive:
            self.controller.show_frame("Inventory")
        else:
            self.statusLabel.config(text="El inventario no esta activo.")

    def showAdmin(self):
        self.statusLabel.config(text="")
        password = askstring(
            "Constraseña", "Contraseña", show='*')
        if password == "310013":
            self.controller.show_frame("Admin")
        elif password is None:
            return
        else:
            self.statusLabel.config(text="Contraseña Incorrecta.")
