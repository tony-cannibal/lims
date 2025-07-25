import pandas as pd
import mariadb

# from datetime import date
import configparser

# wip = pd.read_excel("WIP 2023-10-31 H01M05.XLSX").values.tolist()

database = {
    "host": "172.18.4.58",
    "database": "wip_inventory",
    "user": "yura_admin",
    "password": "Metallica24+",
    "port": 3306,
}


def getConfig(path):
    config = configparser.ConfigParser()
    config.read(path + "/conf.ini")
    invOptions = {
        "area": config["config"]["area"],
        "estacion": config["config"]["estacion"],
    }
    redOptions = {
        "ip": config["database"]["host"],
        "database": config["database"]["database"],
    }
    return invOptions, redOptions


def saveInvOptions(area, estacion, path):
    configFile = path + "/conf.ini"
    config = configparser.ConfigParser()
    config.read(configFile)
    config.set("config", "area", area)
    config.set("config", "estacion", estacion)
    with open(configFile, "w") as configuration:
        config.write(configuration)


def saveRedOptions(ip, dataBase, path):
    configFile = path + "/conf.ini"
    config = configparser.ConfigParser()
    config.read(configFile)
    config.set("database", "host", ip)
    config.set("database", "database", dataBase)
    with open(configFile, "w") as configuration:
        config.write(configuration)


def getDatabase(path):
    config = configparser.ConfigParser()
    config.read(path + "/conf.ini")
    database = {
        "host": config["database"]["host"],
        "database": config["database"]["database"],
        "user": config["database"]["user"],
        "password": config["database"]["password"],
        "port": int(config["database"]["port"]),
    }
    return database


def ceckDatabase(date, connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute(
        """
    SELECT * FROM monthly_wip WHERE wip_id LIKE %s LIMIT 10;
                """,
        (date + "%",),
    )
    res = cur.fetchall()
    cur.close()
    if len(res) > 0:
        return True
    else:
        return False


def getRework(lot: str, connection: dict) -> str:
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM zppr1100 WHERE lot = %s LIMIT 10;
                """,
        (lot,),
    )
    res = cur.fetchall()
    if not res:
        return ""
    res = [list(i) for i in res]
    res = res[0][13]
    return res


def insertIntoDb(filedir: str, columns: list, connection: dict, month: str, area: dict):
    """Insert wip data into database."""
    wip = pd.read_excel(filedir).values.tolist()

    con = mariadb.connect(**connection)
    cur = con.cursor()
    for i in wip:
        rework = getRework(i[columns[9]], connection)
        cur.execute(
            """
                INSERT INTO monthly_wip(
                    wip_id, 
                    centro, 
                    lugar_de_elaboracion, 
                    modelo,
                    grupo_artic_externo, 
                    material, 
                    revicion, 
                    unidad,
                    feeder_21700, 
                    feeder_21800, 
                    lote,
                    rework,
                    qty, 
                    item, 
                    ranking,
                    area
                )
                VALUES(
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s,
                    %s, 
                    %s, 
                    %s, 
                    %s
                );
                    """,
            (
                month + str(i[18]),  # wip_id
                i[columns[0]],  # Centro
                i[columns[1]],  # lugar_de_elaboracion
                i[columns[2]],  # modelo
                i[columns[3]],  # grupo
                i[columns[4]],  # Material
                i[columns[5]],  # revicion
                i[columns[6]],  # unidad
                i[columns[7]],  # feeder_21700
                i[columns[8]],  # feeder_21800
                i[columns[9]],  # lote
                rework,
                i[columns[10]],  # qty
                i[columns[11]],  # item
                i[columns[12]],  # rank
                area[i[3]],  # area
            ),
        )
    con.commit()


def deleteData(month, connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute(
        """
    DELETE FROM wip
        WHERE id LIKE %s;
                """,
        (month + "%",),
    )
    con.commit()


def insertIntoZppr(db, filedir):
    zppr = pd.read_excel(filedir).values.tolist()
    conn = mariadb.connect(**db)
    cur = conn.cursor()

    for i in zppr:
        try:
            cur.execute(
                """
                INSERT INTO zppr1100 (
                    lot,
                    estado,
                    area,
                    fecha,
                    modelo,
                    componente,
                    item,
                    ranking,
                    material,
                    a_bag,
                    rev,
                    cantidad,
                    retrabajo,
                    rev_retrabajo,
                    material_retrabajo,
                    circuitos,
                    circuitos_totales
                    ) VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                        );
                        """,
                (
                    i[0],
                    i[1],
                    i[2],
                    i[3].to_pydatetime().strftime("%Y-%m-%d"),
                    i[4],
                    i[5],
                    i[-1],
                    i[6],
                    i[7],
                    i[8],
                    i[9],
                    i[10],
                    i[11],
                    i[12],
                    i[13],
                    i[14],
                    i[15],
                ),
            )

        except mariadb.Error as e:
            print(f"Error: {e}")

        conn.commit()


if __name__ == "__main__":
    # insertIntoDb(wip, columns, database)
    getRework("4224C30001", database)
