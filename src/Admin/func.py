import pandas as pd

wip = pd.read_excel("WIP 2023-10-31 H01M05.XLSX")

# columns = [col for col in wip.columns]


# for i in columns:
#     if " " in i:
#         print('_'.join(i.split(" ")).lower())
#     else:
#         print(i.lower())

cols = [
    'centro',
    'lugar_de_montaje',
    'denominación',
    'lugar_de_elaboración',
    'denominación.1',
    'modelo',
    'grupo_artíc._externo',
    'material',
    'lista_mat.alternat.',
    'unidad_medida_base',
    'progreso_de_elaboración',
    'finalización_de_la_elaboración',
    'sub_en_espera',
    'finalización_de_sub',
    'finalización_de_montaje',
    'espera_de_entrada_de_mercancías',
    'stock_trn',
    'stock_mty',
    'lote',
    'estado',
    'clase_de_orden',
    'qty',
    'denom.gr-artículos',
    'denom.gpo.artíc.ext.',
    'ranking',
    'descrip.breve',
]

for i in cols:
    if '.' in i:
        print('_'.join(i.split('.')))
