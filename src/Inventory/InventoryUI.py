import tkinter as tk
from tkinter import font
from tkinter import filedialog as fd
from pathlib import Path


# from ttkbootstrap import Style
from tkinter import ttk
from datetime import date
from . import constants as cn
from . import functions as fn


class Inventory(ttk.Frame):
    def __init__(self, parent, controller, path):
        super().__init__(parent)
        self.controller = controller
        self.rootPath = path
        self.area, self.station = fn.getConfig(self.rootPath)
        self.database = fn.getDatabase(self.rootPath)
        self.mes = fn.getMonth(self.database)
        self.wip = fn.getWip(self.database, self.area, self.mes)
        self.wipLength = len(self.wip)
        self.rework = fn.getRework(fn.getWip(self.database, self.area, self.mes))
        self.inventory = {}
        self.inventoryLength = len(self.inventory)

        ######################################
        # Data Capture
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="column")

        self.label_1 = ttk.Label(
            self, text=f"INVENTARIO DE WIP FEEDER {self.area}", font="arial 14"
        )
        self.label_1.grid(row=0, column=0, columnspan=6)
        customFont = font.Font(family="Arial", size=14)

        self.captura = ttk.Entry(self, font=customFont, width=50, justify="center")
        self.captura.grid(row=1, column=0, sticky="EW", pady=20, columnspan=6)

        self.captura.bind("<Return>", self.captureItem)

        # self.combo = ttk.Combobox(self, width=8)
        # self.combo.grid(row=1, column=3, columnspan=1,
        #                  padx=(15, 0), ipadx=10)

        # self.optionButton = tk.Button(
        #     self, text="Opciones", font=customFont)
        # self.optionButton.grid(row=1, column=4, padx=10, sticky="EW")
        #
        # self.configButton = tk.Button(
        #     self, text="Configuracion", font=customFont)
        # # command=lambda: self.changeSize("other"))
        # self.configButton.grid(row=1, column=5, sticky="EW")

        self.statusLabel = tk.Label(self, text="Status", **cn.statusConf)
        self.statusLabel.grid(row=2, column=0, sticky="EW", pady=(0, 10), columnspan=8)

        #######################################
        # Labels

        self.statusFrame = ttk.LabelFrame(self, text="Status")
        self.statusFrame.grid(column=0, row=4, columnspan=6, sticky="EW")

        self.statusFrame.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")

        self.label_sap = tk.Label(
            self.statusFrame,
            text="SAP",
            background="#666",
            **cn.labelConf,
            # relief=tk.SOLID,
        )
        self.label_sap.grid(row=0, column=0, sticky="NSEW", padx=(6, 0))
        self.labelSapAmount = tk.Label(
            self.statusFrame, text=self.wipLength, **cn.labelConf
        )
        self.labelSapAmount.grid(row=1, column=0, sticky="NSEW", padx=(6, 0))

        self.label_inventario = tk.Label(
            self.statusFrame, text="INVENTARIO", background="#666", **cn.labelConf
        )
        self.label_inventario.grid(row=0, column=1, padx=10, sticky="NSEW")

        self.labelInventarioAmount = tk.Label(
            self.statusFrame, text="0", **cn.labelConf
        )
        self.labelInventarioAmount.grid(row=1, column=1, padx=10, sticky="NSEW")

        self.label_porcentaje = tk.Label(
            self.statusFrame,
            text="PORCENTAJE DE INVENTARIO",
            background="#666",
            wraplength=110,
            justify="center",
            **cn.labelConf,
        )
        self.label_porcentaje.grid(row=0, column=2, sticky="NSEW", padx=(0, 6))

        self.labelPorcentajeAmount = tk.Label(
            self.statusFrame, text="0", wraplength=110, justify="center", **cn.labelConf
        )
        self.labelPorcentajeAmount.grid(row=1, column=2, sticky="NSEW", padx=(0, 6))

        ###############################################
        # Tables

        self.tabWidget = ttk.Notebook(self.statusFrame)

        self.progressTab = ttk.Frame(self.tabWidget)
        self.missingTab = ttk.Frame(self.tabWidget)

        self.tabWidget.add(self.progressTab, text="Escaneado")
        self.tabWidget.add(self.missingTab, text="Faltantes")

        self.history = ttk.Treeview(
            self.progressTab, columns=cn.columnHeadigns, show="headings"
        )
        self.history.tag_configure("oddrow", background="#333333")
        self.history.tag_configure("evenrow", background="#222222")
        for i in range(8):
            self.history.heading(cn.columnHeadigns[i], text=cn.columnHeadigns[i])
        for i in range(8):
            self.history.column(
                cn.columnHeadigns[i], width=cn.columnWith[i], anchor="center"
            )

        self.history.pack(expand=1, fill="both")

        self.faltantes = ttk.Treeview(
            self.missingTab, columns=cn.columnHeadigns, show="headings"
        )
        self.faltantes.tag_configure("oddrow", background="#333333")
        self.faltantes.tag_configure("evenrow", background="#222222")

        for i in range(8):
            self.faltantes.heading(cn.columnHeadigns[i], text=cn.columnHeadigns[i])
        for i in range(8):
            self.faltantes.column(
                cn.columnHeadigns[i], width=cn.columnWith[i], anchor="center"
            )
        self.faltantes.pack(expand=1, fill="both")

        self.tabWidget.grid(column=0, row=2, columnspan=3, sticky="EW", pady=5, padx=5)

        self.toExcel = tk.Button(
            self,
            text="Excel",
            font="Arial 14",
            command=self.actualidadExcel,
        )
        self.toExcel.grid(row=7, column=5, pady=10)

        ##############################################################
        # set
        self.updateTables()
        self.updateLabels()

    ##############################################################
    # Functions

    # def getText(self, event):
    #     codigo = self.captura.get()
    #     self.captura.delete(0, 'end')
    #     codigo = fn.checkCode(codigo)
    def actualidadExcel(self):
        filetypes = (("excel file", "*.xlsx"), ("All files", "*.*"))
        save_as = fd.asksaveasfilename(
            title="Guardar Como.",
            initialdir=f"{Path.home()}/Documents",
            filetypes=filetypes,
            defaultextension=".xlsx",
        )
        # actualidad = fn.getWip(self.database, self.area, self.mes)
        fn.wipToExcel(self.mes, self.area, self.database, save_as)
        print(save_as)

    def updateTables(self):
        self.history.delete(*self.history.get_children())
        self.inventory = fn.getInventory(self.database, self.area, self.mes)
        inv_index = 1
        for i in self.inventory:
            row = (
                inv_index,
                self.inventory[i][2],  # lote
                self.wip[self.inventory[i][2]][13],  # retrabajo
                self.inventory[i][3],  # modelo
                self.inventory[i][4],  # item
                self.inventory[i][5],  # np
                self.inventory[i][6],  # cantidad
                self.inventory[i][8],  # prioridad
            )
            if inv_index % 2 == 0:
                self.history.insert("", tk.END, values=row, tags=("evenrow",))
            else:
                self.history.insert("", tk.END, values=row, tags=("oddrow",))
            inv_index += 1
        self.history.yview_moveto(1)

        hist_index = 1
        for i in self.wip:
            if i not in self.inventory:
                row = (
                    hist_index,
                    self.wip[i][12],  # lote
                    self.wip[i][13],  # rework
                    self.wip[i][5],
                    self.wip[i][15],
                    self.wip[i][7],
                    self.wip[i][14],
                    self.wip[i][16],
                )
                if hist_index % 2 == 0:
                    self.faltantes.insert("", tk.END, values=row, tags=("evenrow"))
                else:
                    self.faltantes.insert("", tk.END, values=row, tags=("oddrow"))
                hist_index += 1
        self.faltantes.yview_moveto(1)

    def captureItem(self, event):
        codigo = self.captura.get()
        self.captura.delete(0, "end")
        rw = None
        if codigo in self.rework:
            rw = self.rework[codigo]
        if codigo == "":
            return
        codigo = fn.checkCode(codigo)
        if codigo == "err":
            self.statusLabel.config(text="Codigo Incorrecto", bg="#590707")
            return
        if codigo in self.wip:
            print(codigo)
            print(self.inventory)
            if codigo not in self.inventory:
                code = codigo
                wip_id = f"{str(self.mes)}{str(self.wip[code][12])}"
                record = [
                    wip_id,  # wip id
                    self.wip[code][12],  # lote
                    self.wip[code][5],  # modelo
                    self.wip[code][15],  # item
                    self.wip[code][7],  # num parte
                    self.wip[code][14],  # catidad
                    self.wip[code][17],  # area
                    self.wip[code][16],  # rank
                    self.station,  # estacion
                ]
                fn.captureRecord(record, self.database)
                fn.updatemonthly_wip(wip_id, self.database)
                self.updateTables()
                self.updateLabels()
                self.statusLabel.config(text=f"Lote {code} inventariado.", bg="#145710")
            else:
                self.statusLabel.config(
                    text=f"El lote {codigo} ya esta inventariado.", bg="#7e8a13"
                )
        else:
            self.statusLabel.config(
                text=f"El lote {codigo} no esta en wip", bg="#590707"
            )
            identifier = f"{self.mes}{codigo}{self.area}"
            if not fn.checkAnomaly(identifier, self.database):
                fn.saveAnomaly(codigo, identifier, self.database)

    def updateLabels(self):
        self.inventoryLength = len(self.inventory)
        if self.inventoryLength == 0:
            self.labelPorcentajeAmount.config(text="0%")
            return

        self.labelInventarioAmount.config(text=str(self.inventoryLength))
        porcentaje = str(
            "{:.2f}".format(float(self.inventoryLength / self.wipLength) * 100)
        )
        self.labelPorcentajeAmount.config(text=porcentaje + "%")
