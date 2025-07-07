import pandas as pd
import mariadb
import cn
from datetime import datetime


def createsTables(db):
    conn = mariadb.connect(**db)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS zppr1100 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                lot VARCHAR(15) UNIQUE NOT NULL,
                estado VARCHAR(5),
                area VARCHAR(4) NOT NULL,
                fecha DATE NOT NULL,
                modelo VARCHAR(5),
                componente VARCHAR(7),
                item VARCHAR(20),
                ranking INT,
                material VARCHAR(20),
                a_bag VARCHAR(20),
                rev VARCHAR(4),
                cantidad INT,
                retrabajo VARCHAR(15),
                rev_retrabajo VARCHAR(4),
                material_retrabajo VARCHAR(20),
                circuitos INT,
                circuitos_totales INT,
                creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP() NOT NULL
                );
                    """
        )
    except mariadb.Error as e:
        print(f"Error: {e}")


def getZpprData(file):
    df = pd.read_excel(file)
    df = df.iloc[:, [1, 3, 7, 8, 9, 10, 12, 13, 14, 15, 21, 50, 51, 52, 55, 56]]
    df["item"] = df.iloc[:, 5].map(cn.grupos)
    df = df.fillna("")
    df = df.values.tolist()
    return df


def insertIntoZppr(db, data):
    conn = mariadb.connect(**db)
    cur = conn.cursor()

    for i in data:
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
