import unittest
import mysql.connector
from modules.database import Database
import modules.dictionary as dictionary

class TestDatabase(unittest.TestCase):

    def test_connection_correctly_setted(self):
        db = Database().get_connection()
        self.assertTrue(db.status)

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


###################################################################################################################################

    def test_create_table(self):
        db = Database()
        # test not create table
        response = db.create_table("not_creating_table", [])
        self.assertFalse(response.status)
        response = db.table_exists("not_creating_table")
        self.assertTrue(response.status) # not exist running error
        self.assertFalse(response.content) # but the result of the function is false
        # test create table
        # use deletetable here to ensure there is not existent table
        db.delete_table("creating_table")
        response = db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        self.assertTrue(response.status and response.content)
        response = db.table_exists("creating_table")
        self.assertTrue(response.status and response.content)

        # test create table two times
        db.delete_table("creating_table")
        db.create_table("creating_table", [["name", "INT"]])
        response = db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        self.assertTrue(response.status)
        self.assertFalse(response.content)

    def test_is_table_filled(self): # before test this function, requires create_table, fill_table, delete_table
        db = Database()
        # test with filled table
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        data = [("TestJuan")]
        db.fill_table("creating_table", data)
        self.assertTrue(db.is_table_filled("creating_table"))
        db.delete_table("creating_table")
        # test with empty table
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        self.assertFalse(db.is_table_filled("creating_table"))
        db.delete_table("creating_table")
        # test not existing table
        self.assertIsNone(db.is_table_filled("not_existing_table"))
        # test incorrect data
        self.assertIsNone(db.is_table_filled(None))


    def test_delete_table(self):
        db = Database()
        # test deleting existent table
        db.create_table("delete_table", [["name", "INT"]])
        db.delete_table("delete_table")
        value = db.table_exists("delete_table")
        self.assertIsNotNone(value)
        self.assertFalse(value)
        # test deleting non existent table
        value = db.delete_table("non_existent_table")
        self.assertIsNone(value) # no tengo muy claro como interpretar este caso, si como error, como exito o como indiferente
        # test incorrect variable
        value = db.delete_table(1)
        self.assertIsNotNone(value)
        self.assertFalse(value)

    def test_fill_table(self):
        db = Database()
        # test fill empty table
        db.create_table("filling_table", [["name", "VARCHAR(255)"]])
        familyGamesEndpoint = [("TestJuan")]
        db.fill_table("filling_table", familyGamesEndpoint)
        self.assertTrue(db.is_table_filled("filling_table"))
        db.delete_table("filling_table")
        # test fill not empty table
        familyGamesEndpoint = [("TestJuan2")]
        db.fill_table("not_empty_filling_table", familyGamesEndpoint)
        self.assertTrue(db.is_table_filled("not_empty_filling_table"))
        # test fill not existing table
        familyGamesEndpoint = [("TestJuan3")]
        db.create_table("filling_table", [["name", "VARCHAR(255)"]])
        value = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertIsNotNone(value)
        self.assertFalse(value)
        db.delete_table("filling_table")
        # test fill table with incorrect table structure
        familyGamesEndpoint = [("TestJuan4")]
        db.create_table("filling_table", [["name", "VARCAR(255)"]])
        value = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertIsNotNone(value)
        self.assertFalse(value)
        db.delete_table("filling_table")
        # test fill table with incorrect data
        familyGamesEndpoint = [(5)]
        db.create_table("filling_table", [["name", "VARCHAR(255)"]])
        value = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertIsNotNone(value)
        self.assertFalse(value)
        db.delete_table("filling_table")



if __name__ == "__main__":
    unittest.main()