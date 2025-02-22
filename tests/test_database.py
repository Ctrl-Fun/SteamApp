import unittest
import mysql.connector
from modules.database import Database
import modules.dictionary as dictionary

class TestDatabase(unittest.TestCase):

    def test_table_exists(self):
        db = Database()
        # chequeamos que tabla existe
        data = db.table_exists("user_friends")
        self.assertTrue(data.status and data.content)
        # chequeamos que tabla no existe
        data = db.table_exists("non_existent_table")
        self.assertTrue(data.status)
        self.assertFalse(data.content)
        # chequeamos consulta incorrecta (generamos un error)
        data = db.table_exists(1)
        self.assertFalse(data.status)

    def test_create_table(self):
        db = Database()
        # test not create table
        response = db.create_table("not_creating_table", [])
        self.assertFalse(response.status)
        response = db.table_exists("not_creating_table")
        self.assertTrue(response.status) # not exist running error
        self.assertFalse(response.content) # but the result of the function is false
        db.delete_table("creating_table")
        # test create table
        # use deletetable here to ensure there is not existent table
        response = db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        self.assertTrue(response.status and response.content)
        response = db.table_exists("creating_table")
        self.assertTrue(response.status and response.content)
        db.delete_table("creating_table")
        # test create table two times
        db.create_table("creating_table", [["name", "INT"]])
        response = db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        self.assertTrue(response.status)
        self.assertFalse(response.content)
        db.delete_table("creating_table")

    def test_delete_table(self):
        db = Database()
        # test deleting existent table
        db.create_table("delete_table", [["name", "INT"]])
        response = db.delete_table("delete_table")
        self.assertTrue(response.status and response.content)
        response = db.table_exists("delete_table")
        self.assertTrue(response.status)
        self.assertFalse(response.content)
        # test deleting non existent table
        response = db.delete_table("non_existent_table")
        self.assertFalse(response.status)
        # test incorrect variable
        response = db.delete_table(1)
        self.assertFalse(response.status)

    def test_is_table_filled(self): # before test this function, requires create_table, fill_table, delete_table
        db = Database()
        # test with filled table        
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        data = [["TestJuan"]]
        db.fill_table("creating_table", data)
        response = db.is_table_filled("creating_table")
        self.assertTrue(response.status and response.content)
        db.delete_table("creating_table")
        # test with empty table
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        response = db.is_table_filled("creating_table")
        self.assertTrue(response.status)
        self.assertFalse(response.content)
        db.delete_table("creating_table")
        # test not existing table
        response = db.is_table_filled("non_existent_table")
        self.assertFalse(response.status)
        # test incorrect data
        response = db.is_table_filled(None)
        self.assertFalse(response.status)

    def test_fill_table(self):
        db = Database()
        # test fill one value
        db.create_table("filling_table", [["name", "VARCHAR(255)"]])
        familyGamesEndpoint = [["TestJuan"]]
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertTrue(response.status)
        # test fill several values
        familyGamesEndpoint = [["TestJuan"],["TestJuan"],["TestJuan"],["TestJuan"],["TestJuan"]]
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertTrue(response.status)
        # return
        # test fill not empty table
        familyGamesEndpoint = [["TestJuan2"]]
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertTrue(response.status)
        db.delete_table("filling_table")
        # test fill not existing table
        familyGamesEndpoint = [["TestJuan3"]]
        response = db.fill_table("non_existent_table", familyGamesEndpoint)
        self.assertFalse(response.status)
        # test fill table with incorrect data
        familyGamesEndpoint = [["TestJuan4"]]
        db.create_table("filling_table", [["name", "INT"]])
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertFalse(response.status)
        db.delete_table("filling_table")
        # test fill table incorrect data
        db.create_table("filling_table", [["name", "INT"]])
        familyGamesEndpoint = [(5)] # no deberia colar, debe ser un list de lists
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertFalse(response.status)
        familyGamesEndpoint= [5] # no deberia colar, debe ser un list de lists
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertFalse(response.status)
        familyGamesEndpoint = 5 # no debe colar, debe ser un array
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertFalse(response.status)
        familyGamesEndpoint = [[]] # no debe colar, debe ser un array
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertFalse(response.status)
        familyGamesEndpoint = [[5,6,7]] # no debe colar, ya que la tabla es de una columna y no de tres
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertFalse(response.status)
        db.delete_table("filling_table")
        # test fill table incorrect data structure
        db.create_table("filling_table", [["name", "INT"],["name2", "INT"],["name2", "INT"]])
        familyGamesEndpoint = [(2)] # no debe colar, ya que la tabla es de tres columnas y no de una
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertFalse(response.status)


    




    



if __name__ == "__main__":
    unittest.main()