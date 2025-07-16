# import pandas as pd
import fn
from datetime import datetime


files = [
    "ENERO - JUNIO 2025.xlsx",
    "ENERO - MAYO 2024.xlsx",
    "JUNIO - DICIEMBRE 2024.xlsx",
]

db = {
    "user": "yura_admin",
    "password": "Metallica24+",
    "database": "wip_inventory",
    "host": "172.18.4.58",
}


if __name__ == "__main__":
    fn.createsTables(db)

    for i in files:
        data = fn.getZpprData(i)
        fn.insertIntoZppr(db, data)

    # print(data[0][3].to_pydatetime().strftime("%Y-%m-%m"))
    # print(datetime.fromtimestamp(data[0][3]).strftime("%Y-%m-%d"))
    # for i in data:
    #     print()
