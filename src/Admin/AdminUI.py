import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog as fd
from pathlib import Path
from . import functions as fn
from . import constants as cn


class Admin(ttk.Frame):
    def __init__(self, parent, controller, path):
        super().__init__(parent)

        self.controller = controller
        self.rootPath = path
        self.database = fn.getDatabase(self.rootPath)

        self.filename = ""

        self.invOptions, self.redOptions = fn.getConfig(self.rootPath)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        #######################################################################
        # Config Tab

        self.configFrame = ttk.Frame(self.notebook)
        self.configFrame.pack(fill='both', expand=True, )
        self.configFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.configFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.inventoryFrame = tk.LabelFrame(
            self.configFrame, text='Inventario')
        self.inventoryFrame.pack(
            fill=tk.BOTH, expand=True, padx=30, pady=(20, 10))

        row1Frame1 = tk.Frame(self.inventoryFrame)
        row1Frame1.pack(fill=tk.BOTH, expand=True)

        self.areaLabel = tk.Label(
            row1Frame1, text='Area :', font='Arial 14')
        self.areaLabel.pack(side='left', fill='x', expand=True)
        self.areaEntry = tk.Entry(
            row1Frame1, font='Arial 14', justify='center')
        self.areaEntry.pack(side='left', fill='x', expand=True, padx=(40, 60))

        row2Frame1 = tk.Frame(self.inventoryFrame)
        row2Frame1.pack(fill=tk.BOTH, expand=True)

        self.estacionLabel = tk.Label(
            row2Frame1, text='Estacion :', font='Arial 14')
        self.estacionLabel.pack(side='left', fill='x', expand=True)
        self.estacionEntry = tk.Entry(
            row2Frame1, font='Arial 14', justify='center')
        self.estacionEntry.pack(side='left', fill='x',
                                expand=True, padx=(10, 60))

        self.invetarioButton = tk.Button(
            self.inventoryFrame, text='Guardar', font='Arial 14',
            command=self.saveInventoryOptions)
        self.invetarioButton.pack(pady=(0, 20), padx=(0, 60), anchor='e')

        self.redFrame = tk.LabelFrame(
            self.configFrame, text='Red')
        self.redFrame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10, 25))

        row1Frame2 = tk.Frame(self.redFrame)
        row1Frame2.pack(fill=tk.BOTH, expand=True)

        self.ipLabel = tk.Label(
            row1Frame2, text='Direccion IP :', font='Arial 14')
        self.ipLabel.pack(side='left', fill='x', expand=True)
        self.ipEntry = tk.Entry(
            row1Frame2, font='Arial 14', justify='center')
        self.ipEntry.pack(side='left', fill='x', expand=True, padx=(30, 60))

        row2Frame2 = tk.Frame(self.redFrame)
        row2Frame2.pack(fill=tk.BOTH, expand=True)

        self.databaseLabel = tk.Label(
            row2Frame2, text='Base de Datos :', font='Arial 14')
        self.databaseLabel.pack(side='left', fill='x', expand=True)
        self.databaseEntry = tk.Entry(
            row2Frame2, font='Arial 14', justify='center')
        self.databaseEntry.pack(side='left', fill='x',
                                expand=True, padx=(10, 60))

        self.redButton = tk.Button(
            self.redFrame, text='Guardar', font='Arial 14',
            command=self.saveRedOptions)
        self.redButton.pack(pady=(0, 20), padx=(0, 60), anchor='e')

        #######################################################################
        # Add Data Tab

        self.addDataFrame = ttk.Frame(self.notebook)
        self.addDataFrame.pack(fill="both", expand=True)

        self.addDataFrame.grid_columnconfigure(
            (0, 1, 2, 3, 4, 5), weight=1, uniform="column")

        customFont = font.Font(family="Arial", size=20, slant="italic")
        self.label = tk.Label(
            self.addDataFrame, text="Subir Wip", font="Arial 40")
        # font=controller.title_font)
        self.label.grid(row=0, column=0, columnspan=6,
                        pady=(20, 30), padx=(10, 0))

        self.directory = tk.Label(
            self.addDataFrame, font=customFont, **cn.labelConf)
        self.directory.grid(row=1, column=0, columnspan=5,
                            sticky="NSEW", padx=(10, 10), pady=(0, 40))

        buttonFont = font.Font(family="Arial", size=20, slant="italic")
        self.button1 = tk.Button(
            self.addDataFrame, text="Buscar", font=buttonFont, padx=0,
            command=self.searchForFile)
        self.button1.grid(row=1, column=5, columnspan=1,
                          sticky="EW", pady=(0, 40), padx=(0, 10))

        self.monthLabel = tk.Label(
            self.addDataFrame, text="Mes", font="Arial 20")
        self.monthLabel.grid(row=4, column=0, columnspan=1)
        self.monthEntry = tk.Entry(
            self.addDataFrame, justify="center", font="Arial 20")
        self.monthEntry.grid(row=4, column=1, sticky="NS")

        self.yearLabel = tk.Label(
            self.addDataFrame, text="Año", font="Arial 20")
        self.yearLabel.grid(row=4, column=2, columnspan=1)
        self.yearEntry = tk.Entry(
            self.addDataFrame, justify="center", font="Arial 20")
        self.yearEntry.grid(row=4, column=3, sticky="NS")

        self.button1 = tk.Button(
            self.addDataFrame, text="Subir", font=buttonFont, padx=0,
            command=self.uploadData)
        self.button1.grid(row=4, column=4, columnspan=2,
                          sticky="EW", padx=(40, 10))

        self.wipStatusLabel = tk.Label(
            self.addDataFrame, text="", fg="red", font="Arial 20")
        self.wipStatusLabel.grid(row=5, column=0, columnspan=6, pady=(20, 0))

        #######################################################################
        # Delete Data Tab

        self.deleteDataFrame = ttk.Frame(self.notebook)
        self.deleteDataFrame.pack(fill="both", expand=True)

        self.deleteDataFrame.grid_columnconfigure(
            (0, 1, 2, 3, 4, 5), weight=1, uniform="column")

        self.deleteLabel = tk.Label(
            self.deleteDataFrame, text="Borrar Datos", font="Arial 40")
        # font=controller.title_font)
        self.deleteLabel.grid(row=0, column=0, columnspan=6,
                              pady=(20, 30), padx=(10, 0))

        self.deleteMonthLabel = tk.Label(
            self.deleteDataFrame, text="Mes", font="Arial 20")
        self.deleteMonthLabel.grid(row=4, column=0, columnspan=1)
        self.deleteMonthEntry = tk.Entry(
            self.deleteDataFrame, justify="center", font="Arial 20")
        self.deleteMonthEntry.grid(row=4, column=1, sticky="NS")

        self.deleteYearLabel = tk.Label(
            self.deleteDataFrame, text="Año", font="Arial 20")
        self.deleteYearLabel.grid(row=4, column=2, columnspan=1)
        self.deleteYearEntry = tk.Entry(
            self.deleteDataFrame, justify="center", font="Arial 20")
        self.deleteYearEntry.grid(row=4, column=3, sticky="NS")

        self.deleteButton = tk.Button(
            self.deleteDataFrame, text="Borrar", font=buttonFont, padx=0,
            command=self.deleteWip)
        self.deleteButton.grid(row=4, column=4, columnspan=2,
                               sticky="EW", padx=(40, 10))

        self.statusLabel = tk.Label(
            self.deleteDataFrame, text="", fg="red", font="Arial 20")
        self.statusLabel.grid(row=5, column=0, columnspan=6, pady=(20, 0))

        #######################################################################
        # Add Tabs To Notebook

        self.notebook.add(self.configFrame, text='Configuracion')
        self.notebook.add(self.addDataFrame, text="Agregar Wip")
        self.notebook.add(self.deleteDataFrame, text="Borrar Datos")

        self.setOptionFields()

    def setOptionFields(self):
        self.areaEntry.delete(0, tk.END)
        self.areaEntry.insert(0, self.invOptions['area'])
        self.estacionEntry.delete(0, tk.END)
        self.estacionEntry.insert(0, self.invOptions['estacion'])

        self.ipEntry.delete(0, tk.END)
        self.ipEntry.insert(0, self.redOptions['ip'])
        self.databaseEntry.delete(0, tk.END)
        self.databaseEntry.insert(0, self.redOptions['database'])

    def saveInventoryOptions(self):
        area = self.areaEntry.get()
        estacion = self.estacionEntry.get()
        fn.saveInvOptions(area, estacion, self.rootPath)

    def saveRedOptions(self):
        ip = self.ipEntry.get()
        database = self.databaseEntry.get()
        fn.saveRedOptions(ip, database, self.rootPath)

    def searchForFile(self):
        filetypes = (
            ('excel file', '*.xlsx'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title="Buscar Archivo",
            initialdir=f"{Path.home()}/Documents",
            filetypes=filetypes
        )
        self.filename = filename
        truncated = self.filename.split("/")[-1]
        self.directory.config(text=truncated)

    def uploadData(self):
        month = self.monthEntry.get()
        year = self.yearEntry.get()
        date = month + year
        exist = fn.ceckDatabase(date, self.database)

        if exist and date != "" and self.filename != "":
            self.wipStatusLabel.config(
                text="Ya existen datos en la fecha.", fg="red")
            return

        if self.filename == "":
            self.wipStatusLabel.config(
                text="Debes selecionar un archivo.", fg="red")
            return
        if month == "":
            self.wipStatusLabel.config(
                text="Debes introducir el mes.", fg="red")
            return
        if year == "":
            self.wipStatusLabel.config(
                text="Debes introducir el año.", fg="red")
            return
        fn.insertIntoDb(self.filename, cn.columns,
                        self.database, date, cn.area)
        self.wipStatusLabel.config(
            text="Los datos se cargaron exitosamente.", fg="green")

    def deleteWip(self):
        month = self.deleteMonthEntry.get() + self.deleteYearEntry.get()
        fn.deleteData(month, self.database)
