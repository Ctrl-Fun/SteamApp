import os
import mysql.connector
from dotenv import load_dotenv
from modules.logging import error, success

class Database:
    def __init__(self) -> None:
        self.db_config = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
            "host": os.getenv("DB_HOST"),
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as e:
            error(f"Database connection error: {e}")
            return None

    def table_exists(self, table_name):
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute("SHOW TABLES LIKE %s", (table_name,))
                return cursor.fetchone() is not None
            finally:
                cursor.close()
                db.close()
        return False
    
    def is_table_filled(self, table_name):
        if not self.table_exists(table_name):
            error(f"Table '{table_name}' does not exist")
            return False  # O retornar 0 si prefieres.

        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                row_count = cursor.fetchone()[0]
                return row_count > 0  # Devuelve True si tiene filas, False si está vacía.
            except mysql.connector.Error as e:
                error(f"Error checking rows in table '{table_name}': {e}")
                return False
            finally:
                cursor.close()
                db.close()

    def create_table(self, table, array_data):
        if self.table_exists(table):
            success("Table already exists")
            return
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                columns = ", ".join(f"{col[0]} {col[1]}" for col in array_data)
                sql = f"CREATE TABLE `{table}` (id INT AUTO_INCREMENT PRIMARY KEY, {columns})"
                cursor.execute(sql)
                success(f"Table '{table}' created")
            except mysql.connector.Error as e:
                error(f"Error creating table '{table}': {e}")
            finally:
                cursor.close()
                db.close()

    def fill_table(self, table, table_data, data):
        if not self.table_exists(table):
            error(f"Table '{table}' does not exist")
            return
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                if cursor.fetchone()[0] > 0:
                    success(f"Table '{table}' already filled")
                    return
                
                columns = ", ".join(col[0] for col in table_data)
                placeholders = ", ".join(["%s"] * len(table_data))
                sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
                cursor.executemany(sql, data)
                db.commit()
                success(f"Rows inserted into '{table}'")
            except mysql.connector.Error as e:
                error(f"Error filling table '{table}': {e}")
            finally:
                cursor.close()
                db.close()


    
    ################### DE AQUI PARA ABAJO A BORRAR!
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
