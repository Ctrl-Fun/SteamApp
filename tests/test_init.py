import unittest
import os
from modules.database import Database
from modules.init import Init

class TestInitApp(unittest.TestCase):

    def test_load_endpoints(self):
        TOKEN = os.getenv("TOKEN")
        BASE_PATH = os.getenv("BASE_PATH")
        db = Database()

        # NORMAL USE
        response = Init.load_endpoints(database=db,TOKEN=TOKEN,BASE_PATH=BASE_PATH)
        self.assertTrue(response.status)
        response = db.is_table_filled("endpoints")
        self.assertTrue(response.status and response.content)