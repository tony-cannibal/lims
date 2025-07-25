import tkinter as tk

fontTitle = "Arial 16"

fontLable = "Arial 12"

borderColor = "#ccc"

columnHeadigns = [
    "N°",
    "Lote",
    "Retrabajo",
    "Modelo",
    "Item",
    "N/P",
    "Cantidad",
    "Prioridad",
]
columnWith = [8, 25, 25, 30, 40, 40, 30, 15]

database = {
    "host": "172.18.4.58",
    "database": "wip_inventory",
    "user": "yura_admin",
    "password": "Metallica24+",
    "port": 3306,
}

labelConf = {
    "font": fontLable,
    # "highlightthickness": 1,
    # "highlightbackground": borderColor,
    # "highlightcolor": borderColor,
    "relief": tk.SOLID,
    "borderwidth": 1,
}


statusConf = {
    "font": "Arial 18",
    "highlightthickness": 1,
    "highlightbackground": borderColor,
    "highlightcolor": borderColor,
}

month = {"01": "1", "07": "7", "10": "A"}

saveHeadings = [
    "id ",
    "wip_id ",
    "centro ",
    "lugar_de_elaboracion ",
    "estado  ",
    "modelo ",
    "grupo_artic_externo ",
    "material ",
    "revicion ",
    "unidad ",
    "feeder_21700 ",
    "feeder_21800",
    "lote",
    "rework",
    "qty",
    "item",
    "ranking",
    "area",
    "fecha",
]
