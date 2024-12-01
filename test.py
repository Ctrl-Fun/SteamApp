import os 
from modules.logging import error as error
import modules.endpoints as endpoints
import modules.colors as colors
from modules.utils import *
from modules.database import Database

database=Database()

# database.endpoints()

# endpoints.GetApiEndpoints()

table_name = "endpoints"

table_data = [
    ["name", "VARCHAR(255)"],
    ["url", "TEXT"]
]

table_content = [
    ("ReportEvent", "https://api.steampowered.com/IClientStats_1046930/ReportEvent/v1/"),
    ("GetNextMatchSharingCode", "https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1/")
    ]

database.createTable(table=table_name, array_data=table_data)
database.fillTable(tableName=table_name, tableData=table_data, data=table_content)