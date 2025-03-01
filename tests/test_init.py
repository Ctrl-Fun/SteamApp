import unittest
import os
from modules.database import Database
from modules.init import Init
import modules.dictionary as dictionary


class TestInitApp(unittest.TestCase):

    def test_init_app(self):
        db = Database()
        # normal execution
        db.delete_table("endpoints")
        db.delete_table("user_games")
        db.delete_table("user_friends")
        Init()
        self.assertTrue(db.table_exists("endpoints") and len(db.select_from_table("endpoints")) == 169)
        self.assertTrue(db.table_exists("user_games") and len(db.select_from_table("user_games"))>5)
        self.assertTrue(db.table_exists("user_friends") and len(db.select_from_table("user_friends"))>5)
        # test execution with existing tables
        Init()
        self.assertTrue(db.table_exists("endpoints") and len(db.select_from_table("endpoints")) == 169)
        self.assertTrue(db.table_exists("user_games") and len(db.select_from_table("user_games"))>5)
        self.assertTrue(db.table_exists("user_friends") and len(db.select_from_table("user_friends"))>5)
        # test execution with existing and empty tables
        db.delete_table("endpoints")
        db.delete_table("user_games")
        db.delete_table("user_friends")
        table_structure = dictionary.Database['endpoints']
        db.create_table("endpoints",table_structure)
        table_structure = dictionary.Database['user_games']
        db.create_table("user_games",table_structure)
        table_structure = dictionary.Database['user_friends']
        db.create_table("user_friends", table_structure)
        Init()
        self.assertTrue(db.table_exists("endpoints") and len(db.select_from_table("endpoints")) == 169)
        self.assertTrue(db.table_exists("user_games") and len(db.select_from_table("user_games"))>5)
        self.assertTrue(db.table_exists("user_friends") and len(db.select_from_table("user_friends"))>5)


    def test_load_endpoints(self):
        TOKEN = os.getenv("TOKEN")
        BASE_PATH = os.getenv("BASE_PATH")
        db = Database()

        # test with empty created table
        table_structure = dictionary.Database['endpoints']
        db.delete_table("endpoints")
        db.create_table("endpoints",table_structure)
        Init.load_endpoints(database=db,TOKEN=TOKEN,BASE_PATH=BASE_PATH)
        result = db.select_from_table("endpoints")
        self.assertTrue(len(result)==169)
        # test without created table
        db.delete_table("endpoints")
        Init.load_endpoints(db,TOKEN,BASE_PATH)
        result = db.select_from_table("endpoints")
        self.assertTrue(len(result)==169)
        # test with filled table
        Init.load_endpoints(db,TOKEN,BASE_PATH)
        result = db.select_from_table("endpoints")
        self.assertTrue(len(result)==169)