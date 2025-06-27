import mariadb
import configparser
from datetime import date


database = {
    'host': '172.18.4.58',
    'database': 'wip_inventory',
    'user': 'yura_admin',
    'password': 'Metallica24+',
    'port': 3306
}


def getConfig(path):
    config = configparser.ConfigParser()
    config.read(path + '/conf.ini')
    area = config['config']['area']
    station = config['config']['estacion']
    return area, station


def getDatabase(path):
    config = configparser.ConfigParser()
    config.read(path + '/conf.ini')
    database = {
        'host': config['database']['host'],
        'database': config['database']['database'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'port': int(config['database']['port'])
    }
    return database


def getMonth(connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM global_conf WHERE conf_options = %s;
                """, ('auto', ))
    res = cur.fetchall()
    auto = bool(int(res[0][2]))

    cur.execute("""
    SELECT * FROM global_conf WHERE conf_options = %s;
                """, ('month', ))
    res = cur.fetchall()
    month = res[0][2]

    if auto:
        return date.today().strftime("%m%y")
    else:
        return month


def getWip(connection: dict, area: str, month: str) -> (dict, dict):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM wip WHERE id LIKE %s AND area = %s;
                """, (month + "%", area))
    wip = cur.fetchall()
    cur.close()
    con.close()
    wip = [list(i) for i in wip]
    wip = {i[10]: i for i in wip}
    return wip


def getInventory(connection, area, month):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM inventario WHERE id LIKE %s AND area = %s;
                """, (month + "%", area))
    inventario = cur.fetchall()
    cur.close()
    con.close()
    inventario = [list(i) for i in inventario]
    inventario = {i[1]: i for i in inventario}
    return inventario


def checkCode(code):
    if code == "":
        return "err"
    length = len(code)
    start = code[0]
    if code == "":
        return "err"
    if length == 10 and start == "4":
        return code
    elif start == "!" and length >= 17:
        return code[1:11]
    else:
        return "err"


def captureRecord(record, mes, connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute("""
    INSERT INTO inventario(
        id, lote, modelo, item, num_parte, cantidad, area, estacion)
        VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s
            );""", (
                record[0], record[1], record[2], record[3],
                record[4], record[5], record[6], record[7]
                ))
    con.commit()
    cur.close()


def checkAnomaly(identifier, connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()

    cur.execute("""
    SELECT * FROM anomalies WHERE anomaly = %s;
    """, (identifier,))
    res = cur.fetchall()
    if len(res) > 0:
        return True
    else:
        return False


def saveAnomaly(code, identifier, connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute("""
    INSERT INTO anomalies( anomaly, lot)
        VALUES( %s, %s );""", (identifier, code))
    con.commit()
    cur.close()
