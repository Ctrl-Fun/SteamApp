import unittest
import mysql.connector
from modules.database import Database
import modules.dictionary as dictionary

class TestDatabase(unittest.TestCase):

    def test_table_exists(self):
        db = Database()
        # chequeamos que tabla existe
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        data = db.table_exists("creating_table")
        self.assertTrue(data)
        db.delete_table("creating_table")
        # chequeamos que tabla no existe
        data = db.table_exists("non_existent_table")
        self.assertFalse(data)
        # chequeamos consulta incorrecta (generamos un error)
        with self.assertRaises(Exception):
            db.table_exists(1)

    def test_create_table(self):
        db = Database()
        # test incorrect inputs
        with self.assertRaises(Exception):
            db.create_table("not_creating_table", [])
        # test create table
        # use deletetable here to ensure there is not existent table
        self.assertTrue(db.create_table("creating_table", [["name", "VARCHAR(255)"]]))
        self.assertTrue(db.table_exists("creating_table"))
        # test create table two times
        self.assertFalse(db.create_table("creating_table", [["name", "VARCHAR(255)"]]))
        db.delete_table("creating_table")

    def test_delete_table(self):
        db = Database()
        # test deleting existent table
        db.create_table("delete_table", [["name", "INT"]])
        response = db.delete_table("delete_table")
        self.assertTrue(response)
        response = db.table_exists("delete_table")
        self.assertFalse(response)
        # test deleting non existent table
        self.assertFalse(db.delete_table("non_existent_table"))
        with self.assertRaises(Exception):
            db.delete_table(1)

    def test_is_table_filled(self): # before test this function, requires create_table, fill_table, delete_table
        db = Database()
        # test with filled table        
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        data = [["TestJuan"]]
        db.fill_table("creating_table", data)
        response = db.is_table_filled("creating_table")
        self.assertTrue(response)
        db.delete_table("creating_table")
        # test with empty table
        db.create_table("creating_table", [["name", "VARCHAR(255)"]])
        response = db.is_table_filled("creating_table")
        self.assertFalse(response)
        db.delete_table("creating_table")
        # test not existing table
        with self.assertRaises(Exception):
            db.is_table_filled("non_existent_table")
        # test incorrect data
        with self.assertRaises(Exception):
            db.is_table_filled(None)

    def test_fill_table(self):
        db = Database()
        # test fill one value
        db.create_table("filling_table", [["name", "VARCHAR(255)"]])
        familyGamesEndpoint = [["TestJuan"]]
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertTrue(response)
        # test fill several values
        familyGamesEndpoint = [["TestJuan"],["TestJuan"],["TestJuan"],["TestJuan"],["TestJuan"]]
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertTrue(response)
        # test fill not empty table
        familyGamesEndpoint = [["TestJuan2"]]
        response = db.fill_table("filling_table", familyGamesEndpoint)
        self.assertTrue(response)
        db.delete_table("filling_table")
        # test fill not existing table
        familyGamesEndpoint = [["TestJuan3"]]
        with self.assertRaises(Exception):
            db.fill_table("non_existent_table", familyGamesEndpoint)
        # test fill table with incorrect data
        familyGamesEndpoint = [["TestJuan4"]]
        db.create_table("filling_table", [["name", "INT"]])
        with self.assertRaises(Exception):
            db.fill_table("filling_table", familyGamesEndpoint)
        db.delete_table("filling_table")
        # test fill table incorrect data
        db.create_table("filling_table", [["name", "INT"]])
        familyGamesEndpoint = [(5)] # no deberia colar, debe ser un list de lists
        with self.assertRaises(Exception):
            db.fill_table("filling_table", familyGamesEndpoint)
        familyGamesEndpoint= [5] # no deberia colar, debe ser un list de lists
        with self.assertRaises(Exception):
            db.fill_table("filling_table", familyGamesEndpoint)
        familyGamesEndpoint = 5 # no debe colar, debe ser un array
        with self.assertRaises(Exception):
            db.fill_table("filling_table", familyGamesEndpoint)
        familyGamesEndpoint = [[]] # no debe colar, debe ser un array
        with self.assertRaises(Exception):
            db.fill_table("filling_table", familyGamesEndpoint)
        familyGamesEndpoint = [[5,6,7]] # no debe colar, ya que la tabla es de una columna y no de tres
        with self.assertRaises(Exception):
            db.fill_table("filling_table", familyGamesEndpoint)
        db.delete_table("filling_table")
        # test fill table incorrect data structure
        db.create_table("filling_table", [["name", "INT"],["name2", "INT"],["name3", "INT"]])
        familyGamesEndpoint = [(2)] # no debe colar, ya que la tabla es de tres columnas y no de una
        with self.assertRaises(Exception):
            db.fill_table("filling_table", familyGamesEndpoint)
        db.delete_table("filling_table")
        
    def test_select_from_table(self):
        db = Database()
        db.delete_table("creating_table")

        # Test: Table does not exist
        with self.assertRaises(Exception):
            db.select_from_table("non_existent_table")

        # Test: Select all columns from a filled table
        db.create_table("creating_table", [["name", "VARCHAR(255)"], ["value", "INT"]])
        data = [["TestSelectFromTb", 1], ["TestSelectFromTb", 1], ["airambo", 99], ["endpoints", 55]]
        db.fill_table("creating_table", data)
        
        response = db.select_from_table("creating_table")  # Should return tuples with all columns
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], tuple)

        # Test: Select with one column
        response = db.select_from_table("creating_table", columns=["name"])
        self.assertIsInstance(response, list)

        # Test: Select with multiple columns
        response = db.select_from_table("creating_table", columns=["value", "name"])
        self.assertIsInstance(response, list)

        # Test: Selecting a non-existent column should raise an exception
        with self.assertRaises(Exception):
            db.select_from_table("creating_table", columns=["invalid_column"])

        # Test: Selecting with WHERE clause
        response = db.select_from_table("creating_table", where_clause="name = 'airambo' AND id > 2")
        self.assertIsInstance(response, list)

        # Test: Invalid WHERE clause (empty string or invalid format)
        with self.assertRaises(Exception):
            db.select_from_table("creating_table", where_clause=[""])
        with self.assertRaises(Exception):
            db.select_from_table("creating_table", where_clause="invalid SQL syntax")

        # Test: ORDER BY (ascending)
        response = db.select_from_table("creating_table", order_by="value ASC")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0][2], 1)  # First result should have the smallest value

        # Test: ORDER BY (descending)
        response = db.select_from_table("creating_table", order_by="value DESC")
        self.assertIsInstance(response, list)
        self.assertEqual(response[0][2], 99)  # First result should have the highest value

        # Test: ORDER BY with non-existent column should raise an exception
        with self.assertRaises(Exception):
            db.select_from_table("creating_table", order_by="non_existent_column ASC")

        # Test: LIMIT (should return the first 2 rows)
        response = db.select_from_table("creating_table", limit=2)
        self.assertEqual(len(response), 2)

        # Test: LIMIT with ORDER BY (should return top 2 sorted results)
        response = db.select_from_table("creating_table", order_by="value ASC", limit=2)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0][2], 1)  # Smallest value

        # Test: WHERE + ORDER BY + LIMIT combined
        response = db.select_from_table("creating_table", where_clause="name = 'TestSelectFromTb'", order_by="value DESC", limit=1)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0][1], "TestSelectFromTb")

        # Test: LIMIT set to 0 should return an empty list
        # response = db.select_from_table("creating_table", limit=0)
        # self.assertEqual(response, [])

        # Test: Negative LIMIT should raise an exception
        with self.assertRaises(Exception):
            db.select_from_table("creating_table", limit=-1)

        # Cleanup
        db.delete_table("creating_table")




    



if __name__ == "__main__":
    unittest.main()