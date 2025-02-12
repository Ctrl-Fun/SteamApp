import os
import mysql.connector
from modules.logging import error, success

class ReturnData:
    def __init__(self, status = False, content = None):
        self.status = status
        self.content = content


class Database:
    def __init__(self) -> None:
        self.db_config = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
            "host": os.getenv("DB_HOST"),
        }


    def get_connection(self):
        return_data = ReturnData() 
        try:
            connection = mysql.connector.connect(**self.db_config)
            return_data.status = True
            return_data.content = connection
            return return_data
        except mysql.connector.Error as e:
            error(f"Database connection error: {e}")
            return return_data

    def table_exists(self, table_name):
        return_data = ReturnData()

        if not isinstance(table_name, str):
            error("Table name must be a string")
            return return_data

        db = self.get_connection().content
        if db:
            try:
                cursor = db.cursor()
                cursor.execute("SHOW TABLES LIKE %s", (table_name,))
                result = cursor.fetchone() is not None
                return_data.status = True
                return_data.content = result
                return return_data
            except Exception as e:
                error(f"Error reading table '{table_name}': {e}")
                return return_data
            finally:
                cursor.close()
                db.close()
    
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
            return True, None
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                columns = ", ".join(f"{col[0]} {col[1]}" for col in table_structure)
                sql = f"CREATE TABLE `{table}` (id INT AUTO_INCREMENT PRIMARY KEY, {columns})"
                cursor.execute(sql)
                success(f"Table '{table}' created")
            except mysql.connector.errors.ProgrammingError as e:
                error(f"Error in syntax '{table}': {e}")
                return False
            except Exception as e:
                error(f"Error creating table '{table}': {e}")
                return False
            finally:
                cursor.close()
                db.close()

    def delete_table(self, table_name):
        if not self.table_exists(table_name):
            success("Table not exists already")
            return
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                sql = f"DROP TABLE `{table_name}`"
                cursor.execute(sql)
                success(f"Table '{table_name}' deleted")
            except Exception as e:
                error(f"Error deleting table '{table_name}': {e}")
                return False
            finally:
                cursor.close()
                db.close()
                


    def fill_table(self, table_name, table_data):
        if not self.table_exists(table_name):
            error(f"Table '{table_name}' does not exist")
            return False
        
        if not isinstance(table_data, list):
            error("Table data must be a list")
            return False

        db = self.get_connection()
        if db:
            try:
                # Retrieve data columns
                cursor = db.cursor()
                sql = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
                cursor.execute(sql)
                columns_structure = [row[0] for row in cursor.fetchall()[1:]] # IMPORTANT: Exclude 'id' column      

                if not columns_structure:
                    error(f"Could not retrieve columns for '{table_name}'")
                    return False
                
                columns = ", ".join(columns_structure)

                placeholders = ", ".join(["%s"] * len(columns_structure))
                sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
                if(len(table_data)==1):
                    cursor.execute(sql, table_data)
                else:
                    cursor.executemany(sql, table_data)
                db.commit()
                success(f"Rows inserted into '{table_name}'")
            except mysql.connector.Error as e:
                error(f"Error filling table '{table_name}': {e}")
                return False
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
