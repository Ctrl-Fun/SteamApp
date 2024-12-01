import mysql.connector
from modules.logging import error, success

class Database:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            user="steamapp_user",
            password="steamapp",
            database='steamapp',
            host="localhost"
        )

    def createTable(self, table: str, array_data: list):
        db = self.db

        if(db):
            cursor = db.cursor()
            cursor.execute("""
                SHOW TABLES
            """)
            resultado = cursor.fetchall()
            tables = [item[0] for item in resultado]

            if(not table in tables):
                columns = ""
                for idx, item in enumerate(array_data):
                    if idx == len(array_data) - 1:  # Si es el último elemento
                        columns += f"{item[0]} {item[1]}"
                    else:
                        columns += f"{item[0]} {item[1]}, "

                sql = f"CREATE TABLE {table} (id INT AUTO_INCREMENT PRIMARY KEY, {columns})"
                cursor.execute(sql)
                success("Table created")
            else:
                success("Table exists already")
        else:
            error("Database doesn't exist")

    def fillTable(self, tableName: str, tableData: list, data: list):
        # data es una lista de tuplas
        db = self.db
        columnsList = [item[0] for item in tableData]
        columnsStr = ", ".join(str(x) for x in columnsList)
        if(db):
            cursor = db.cursor()
            cursor.execute("""
                SHOW TABLES
            """)
            resultado = cursor.fetchall()
            tables = [item[0] for item in resultado]
            print(tables)
            if(tableName in tables):
                cursor.execute(f"SELECT COUNT(*) FROM {tableName};")
                resultado = cursor.fetchone()
                print(resultado[0]) 
                if(resultado[0] <= 0):
                    print("filling table...")
                    #necesitamos definir como van a llegar los datos
                    sql = f"INSERT INTO {tableName} ({columnsStr}) VALUES (%s, %s)"
                    cursor.executemany(sql, data) 
                    db.commit()
            else:
                error("Table "+ tableName +" doesn't exis")
        else:
            error("Database doesn't exist")

    def endpoints(self):
        db = self.db

        if(db): # chequear conexion con bbdd
            cursor = db.cursor()
            cursor.execute("""
                SHOW TABLES
            """)
            resultado = cursor.fetchall()
            tables = [item[0] for item in resultado]

            if("endpoints" in tables):
                cursor.execute("SELECT COUNT(*) FROM endpoints;")
                resultado = cursor.fetchone()
                print(resultado)

                if(resultado[0] <= 0):   # llenar tabla
                    sql = ("INSERT INTO endpoints (nombre_endpoint, url_endpoint) VALUES (%s, %s)")
                    values = ("ReportEvent","https://api.steampowered.com/IClientStats_1046930/ReportEvent/v1/")
                    cursor.execute(sql, values)
                    db.commit()

                    print(cursor.rowcount, "registro(s) insertado(s)")
                else:
                    print("tabla endpoints con valores")
            else:
                cursor.execute("CREATE TABLE endpoints (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), url TEXT)")
        else:
            error("Error in request")

    def games(self):
        db = self.db
    # Games database 
        if(db):
            cursor = db.cursor()
            cursor.execute("""
                SHOW TABLES
            """)
            resultado = cursor.fetchall()
            tables = [item[0] for item in resultado]
            print(tables)
            if("games" in tables):
                cursor.execute("SELECT COUNT(*) FROM games;")
                resultado = cursor.fetchone()
                print(resultado[0]) 
                if(resultado[0] <= 0):
                    print("filling table...")
                    sql = "INSERT INTO games (name, gameId) VALUES (%s, %s)"
                    val = [
                        ('Peter', 'Lowstreet 4'),
                        ('Amy', 'Apple st 652'),
                        ('Hannah', 'Mountain 21'),
                        ('Michael', 'Valley 345'),
                        ('Sandy', 'Ocean blvd 2'),
                        ('Betty', 'Green Grass 1'),
                        ('Richard', 'Sky st 331'),
                        ('Susan', 'One way 98'),
                        ('Vicky', 'Yellow Garden 2'),
                        ('Ben', 'Park Lane 38'),
                        ('William', 'Central st 954'),
                        ('Chuck', 'Main Road 989'),
                        ('Viola', 'Sideway 1633')
                        ]
                    cursor.executemany(sql, val) 
                    db.commit()
            else:
                cursor.execute("CREATE TABLE games (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), gameId VARCHAR(255))")
        else:
            error("Error in request")
