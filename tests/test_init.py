import unittest
import os
from modules.database import Database
from modules.init import Init
import modules.dictionary as dictionary


class TestInitApp(unittest.TestCase):

    def test_load_endpoints(self):
        TOKEN = os.getenv("TOKEN")
        BASE_PATH = os.getenv("BASE_PATH")
        db = Database()

        # NORMAL USE
        table_structure = dictionary.Database['endpoints']
        db.delete_table("endpoints")
        db.create_table("endpoints",table_structure)
        Init.load_endpoints(database=db,TOKEN=TOKEN,BASE_PATH=BASE_PATH)
        result = db.select_from_table("endpoints")
        self.assertTrue(len(result)>50)


        # self.assertTrue(response.status)
        # response = db.is_table_filled("endpoints")
        # self.assertTrue(response.status and response.content)