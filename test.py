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

tableExist = database.existTable(tableName=table_name)
if(not tableExist):
    database.createTable(table=table_name, array_data=table_data)

rows_count = database.isTableFilled(tableName=table_name)
if(rows_count == 0):
    table_content = endpoints.GetApiEndpoints()
    database.fillTable(tableName=table_name, tableData=table_data, data=table_content)


# result = database.clearTable(tableName=table_name)

result = database.isTableFilled(tableName=table_name)

print(result)