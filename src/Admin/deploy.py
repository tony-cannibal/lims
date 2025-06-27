import mariadb

database = {
    'host': '172.18.4.58',
    'database': 'wip_inventory',
    'user': 'yura_admin',
    'password': 'Metallica24+',
    'port': 3306
}


def createTables(connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wip (
            id VARCHAR(50) PRIMARY KEY,
            centro VARCHAR(50),
            lugar_de_elaboracion VARCHAR(50),
            modelo VARCHAR(50),
            grupo_artic_externo VARCHAR(50),
            material VARCHAR(50),
            revicion VARCHAR(50),
            unidad VARCHAR(50),
            feeder_21700 VARCHAR(50),
            feeder_21800 VARCHAR(50),
            lote VARCHAR(50),
            qty VARCHAR(50),
            item VARCHAR(50),
            ranking INT,
            area VARCHAR(10),
            fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id VARCHAR(50) PRIMARY KEY,
            lote VARCHAR(10),
            modelo VARCHAR(20),
            item VARCHAR(50),
            num_parte VARCHAR(50),
            cantidad INT,
            area VARCHAR(10),
            estacion VARCHAR(20),
            fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS global_conf (
            id INT PRIMARY KEY,
            option VARCHAR(50),
            state INT,
            update_at TIMESTAMP
            );""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id INT PRIMARY KEY AUTO_INCREMENT,
            anomaly VARCHAR(50) UNIQUE,
            lot VARCHAR(20),
            fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );""")
    cur.close()
    con.close()


createTables(database)
