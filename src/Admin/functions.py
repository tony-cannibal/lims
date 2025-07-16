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
    SELECT * FROM wip WHERE id LIKE %s LIMIT 10;
                """,
        (date + "%",),
    )
    res = cur.fetchall()
    cur.close()
    if len(res) > 0:
        return True
    else:
        return False


def insertIntoDb(filedir, columns, connection, month, area):
    """Insert wip data into database."""
    wip = pd.read_excel(filedir).values.tolist()

    con = mariadb.connect(**connection)
    cur = con.cursor()
    for i in wip:
        cur.execute(
            """
                INSERT INTO wip(
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
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s);
                    """,
            (
                month + str(i[18]),
                i[columns[0]],
                i[columns[1]],
                i[columns[2]],
                i[columns[3]],
                i[columns[4]],
                i[columns[5]],
                i[columns[6]],
                i[columns[7]],
                i[columns[8]],
                i[columns[9]],
                i[columns[10]],
                i[columns[11]],
                i[columns[12]],
                area[i[3]],
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


if __name__ == "__main__":
    # insertIntoDb(wip, columns, database)
    pass
