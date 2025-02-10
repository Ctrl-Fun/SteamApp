import unittest
import mysql.connector
from modules.database import Database
import modules.dictionary as dictionary

class TestDatabase(unittest.TestCase):

    def test_connection_correctly_setted(self):
        db = Database().get_connection()
        self.assertIsNotNone(db)

    def test_table_exists(self):
        db = Database()
        self.assertTrue(db.table_exists("user_friends"))
        self.assertFalse(db.table_exists("non_existent_table"))
        self.assertFalse(db.table_exists(1))

    def test_is_table_filled(self):
        db = Database()
        self.assertTrue(db.is_table_filled("endpoints"))
        self.assertFalse(db.is_table_filled("user_friends"))
        self.assertFalse(db.is_table_filled("non_existent_table"))
        self.assertFalse(db.is_table_filled(1))

    def test_create_table(self):
        db = Database()
        # test not create table
        db.create_table("not_creating_table", [])
        self.assertFalse(db.table_exists("not_creating_table"))
        # test create table
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        self.assertTrue(db.table_exists("creating_table"))
        # test create table two times
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])

    def test_fill_table(self):
        db = Database()
        # test fill empty table
        db.create_table("filling_table", [["name", "VARCHAR(255)"]])
        familyGamesEndpoint = [("TestJuan","https://api.steampowered.com/TestJuan/")]
        db.fill_table("endpoints", familyGamesEndpoint)
        # test fill not empty table

        # test fill not existing table

        # test fill table with incorrect table structure

        # test fill table with incorrect data
    



if __name__ == "__main__":
    unittest.main()