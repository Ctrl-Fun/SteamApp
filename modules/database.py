import os
import mysql.connector
from modules.logging import error, success
from modules.returndata import ReturnData

class Database:
    def __init__(self) -> None:
        self.db_config = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
            "host": os.getenv("DB_HOST"),
        }

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def table_exists(self, table_name):
        if not isinstance(table_name, str):
            raise Exception("Table name must be a string")
        
        db = self.get_connection()
        if db:
            cursor = db.cursor()
            cursor.execute("SHOW TABLES LIKE %s", (table_name,))
            result = cursor.fetchone() is not None
            cursor.close()
            db.close()
            return result
    
    def is_table_filled(self, table_name):
        if not self.table_exists(table_name):
            raise Exception(f"Table {table_name} does not exist")

        db = self.get_connection()
        if db:
            cursor = db.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            row_count = cursor.fetchone()[0]
            cursor.close()
            db.close()
            return row_count > 0

    def create_table(self, table, table_structure):
        response = self.table_exists(table)
        if response:
            success("Table already exists")
            return False
        
        db = self.get_connection()
        if db:
            cursor = db.cursor()
            columns = ", ".join(f"{col[0]} {col[1]}" for col in table_structure)
            sql = f"CREATE TABLE `{table}` (id INT AUTO_INCREMENT PRIMARY KEY, {columns})"
            cursor.execute(sql)
            success(f"Table '{table}' created")
            if cursor:
                cursor.close()
            db.close()
            return True

    def delete_table(self, table_name):
        if not self.table_exists(table_name):
            success("Table not exists already")
            return False
        
        db = self.get_connection()
        if db:
                cursor = db.cursor()
                sql = f"DROP TABLE `{table_name}`"
                cursor.execute(sql)
                success(f"Table '{table_name}' deleted")
                cursor.close()
                db.close()
                return True
                

    def fill_table(self, table_name, table_data):
        if not self.table_exists(table_name):
            raise Exception(f"Table '{table_name}' does not exist")
            
        if not isinstance(table_data, list):
            raise Exception("Table must be a list of list elements, parent error")
        
        if not all(isinstance(e,list) for e in table_data):
            raise Exception("Table must be a list of tuples, children error")

        db = self.get_connection()
        if db:
            # Retrieve data columns
            cursor = db.cursor()
            sql = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
            cursor.execute(sql)
            columns_structure = [row[0] for row in cursor.fetchall()[1:]] # IMPORTANT: Exclude 'id' column      

            if not columns_structure:
                raise Exception(f"Could not retrieve columns for '{table_name}'")
            
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
            cursor.close()
            db.close()
            return True

    def get_table_cols(self, table_name):
        return f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"

    def select_from_table(self, table, columns=None, where_clause=None, order_by=None, limit=None):
        if not self.table_exists(table):
            raise Exception(f"Table '{table}' does not exist")
        
        db = self.get_connection()
        if db:
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
            response = cursor.fetchall()
            cursor.close()
            db.close()
            return response