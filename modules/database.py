import os
import mysql.connector
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

    def create_table(self, table, table_structure):
        if self.table_exists(table):
            success("Table already exists")
            return
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                columns = ", ".join(f"{col[0]} {col[1]}" for col in table_structure)
                sql = f"CREATE TABLE `{table}` (id INT AUTO_INCREMENT PRIMARY KEY, {columns})"
                cursor.execute(sql)
                success(f"Table '{table}' created")
            except mysql.connector.Error as e:
                error(f"Error creating table '{table}': {e}")
            finally:
                cursor.close()
                db.close()


    def fill_table(self, table, table_structure, table_data):
        if not self.table_exists(table):
            error(f"Table '{table}' does not exist")
            return
        
        if not isinstance(table_data, list):
            error("Table data must be a list")
            return False

        # Verificar que cada elemento es una tupla
        for item in table_data:
            if not isinstance(item, tuple):
                error("Table data must be a list of tuples")
                return False
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                if cursor.fetchone()[0] > 0:
                    success(f"Table '{table}' already filled")
                    return
                
                columns = ", ".join(col[0] for col in table_structure)
                placeholders = ", ".join(["%s"] * len(table_structure))
                sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
                cursor.executemany(sql, table_data)
                db.commit()
                success(f"Rows inserted into '{table}'")
            except mysql.connector.Error as e:
                error(f"Error filling table '{table}': {e}")
            finally:
                cursor.close()
                db.close()

    def select_from_table(self, table, columns=None, where_clause=None, order_by=None, limit=None):
        if not self.table_exists(table):
            error(f"Table '{table}' does not exist")
            return None
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                # Generar columnas para seleccionar
                columns = ", ".join(columns) if columns else "*"
                
                # Construir consulta SQL
                query = f"SELECT {columns} FROM `{table}`"
                if where_clause:
                    query += f" WHERE {where_clause}"

                if order_by:
                    query += f" ORDER BY {order_by}"

                if limit:
                    query += f" LIMIT {limit}"

                # Ejecutar consulta
                cursor.execute(query)
                return cursor.fetchall()
            except mysql.connector.Error as e:
                error(f"Error selecting from table '{table}': {e}")
            finally:
                cursor.close()
                db.close()
        return None

    
    ################### DE AQUI PARA ABAJO A BORRAR!

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
