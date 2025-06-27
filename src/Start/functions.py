import mariadb
import configparser


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


def getActiveStatus(connection):
    con = mariadb.connect(**connection)
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM global_conf WHERE conf_options = %s;
                """, ("active",))
    status = cur.fetchall()
    status = bool(int(status[0][2]))
    return status
