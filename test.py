import os 
from modules.logging import error as error
import modules.endpoints as endpoints
import modules.colors as colors
from modules.utils import *
from modules.database import Database
from modules.init import Init



### STARTING APP

database=Database()

# Get and Save All Api Info
table_name = "endpoints"
table_data = [
    ["name", "VARCHAR(255)"],
    ["url", "TEXT"]
]

tableExist = database.table_exists(table_name)
if(not tableExist):
    database.create_table(table_name, table_data)

rows_count = database.is_table_filled(table_name)
if(rows_count == 0):
    table_content = endpoints.GetApiEndpoints()
    database.fill_table(table_name, table_data, table_content)


# result = database.clearTable(tableName=table_name)

result = database.is_table_filled(table_name)

print(result)