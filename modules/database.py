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
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as e:
            error(f"Database connection error: {e}")
            return ReturnData(status=False,content=str(e))

    def table_exists(self, table_name):
        if not isinstance(table_name, str):
            response = "Table name must be a string"
            error(response)
            return ReturnData(status=False,content=response)

        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute("SHOW TABLES LIKE %s", (table_name,))
                result = cursor.fetchone() is not None
                return ReturnData(status=True,content=result)
            except Exception as e:
                error(f"Error reading table '{table_name}': {e}")
                return ReturnData(status=False,content=str(e))
            finally:
                cursor.close()
                db.close()
    
    def is_table_filled(self, table_name):
        if not self.table_exists(table_name):
            response = f"Table '{table_name}' does not exist"
            error(response)
            return ReturnData(status=False, content=response)  # O retornar 0 si prefieres.

        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                row_count = cursor.fetchone()[0]
                value = row_count > 0 # Devuelve True si tiene filas, False si está vacía.
                return ReturnData(status=True, content=value)
            except mysql.connector.Error as e:
                error(f"Error checking rows in table '{table_name}': {e}")
                return ReturnData(status=False,content=str(e))
            finally:
                cursor.close()
                db.close()

    def create_table(self, table, table_structure):
        response = self.table_exists(table)
        if response.status and response.content:
            success("Table already exists")
            return ReturnData(status=True,content=False)
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                columns = ", ".join(f"{col[0]} {col[1]}" for col in table_structure)
                sql = f"CREATE TABLE `{table}` (id INT AUTO_INCREMENT PRIMARY KEY, {columns})"
                cursor.execute(sql)
                success(f"Table '{table}' created")
                return ReturnData(status=True,content=True)
            except mysql.connector.errors.ProgrammingError as e:
                error(f"Error in syntax '{table}': {e}")
                return ReturnData(status=False,content=str(e))
            except Exception as e:
                error(f"Error creating table '{table}': {e}")
                return ReturnData(status=False,content=str(e))
            finally:
                if cursor:
                    cursor.close()
                db.close()

    def delete_table(self, table_name):
        if not self.table_exists(table_name):
            success("Table not exists already")
            return ReturnData(status=True,content=False)
        
        db = self.get_connection()
        if db:
            try:
                cursor = db.cursor()
                sql = f"DROP TABLE `{table_name}`"
                cursor.execute(sql)
                success(f"Table '{table_name}' deleted")
                return ReturnData(status=True,content=True)
            except Exception as e:
                error(f"Error deleting table '{table_name}': {e}")
                return ReturnData(status=False,content=str(e))
            finally:
                cursor.close()
                db.close()


    def fill_table(self, table_name, table_data):
        if not self.table_exists(table_name):
            response = f"Table '{table_name}' does not exist" 
            error(response)
            return ReturnData(status=False,content=response)
        
        if not isinstance(table_data, list):
            response = "Table must be a list of list elements, parent error" 
            error(response)
            return ReturnData(status=False,content=response)
        
        if not all(isinstance(e,list) for e in table_data):
            response = "Table must be a list of tuples, chilren error"
            error(response)
            return ReturnData(status=False,content=response) 

        db = self.get_connection()
        if db:
            try:
                # Retrieve data columns
                cursor = db.cursor()
                sql = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
                cursor.execute(sql)
                columns_structure = [row[0] for row in cursor.fetchall()[1:]] # IMPORTANT: Exclude 'id' column      

                if not columns_structure:
                    response = f"Could not retrieve columns for '{table_name}'"
                    error(response)
                    return ReturnData(status=False,content=response)
                
                columns = ", ".join(columns_structure)

                placeholders = ", ".join(["%s"] * len(columns_structure))
                sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
                if(len(table_data)==1):
                    print(table_data)
                    cursor.execute(sql, table_data[0])
                else:
                    cursor.executemany(sql, table_data)
                db.commit()
                success(f"Rows inserted into '{table_name}'")
                return ReturnData(status=True,content=True)
            except mysql.connector.Error as e:
                error(f"Error filling table '{table_name}': {e}")
                return ReturnData(status=False,content=str(e))
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