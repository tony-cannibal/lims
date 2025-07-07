# import pandas as pd
import fn
from datetime import datetime


file = "ENERO - JUNIO 2025.xlsx"

db = {
    "user": "yura_admin",
    "password": "Metallica24+",
    "database": "wip_inventory",
    "host": "172.18.4.58",
}


if __name__ == "__main__":
    fn.createsTables(db)
    data = fn.getZpprData(file)

    # print(data[0][3].to_pydatetime().strftime("%Y-%m-%m"))
    # print(datetime.fromtimestamp(data[0][3]).strftime("%Y-%m-%d"))
    fn.insertIntoZppr(db, data)
    # for i in data:
    #     print()
