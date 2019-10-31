import unittest
# import server.Server
import Client.Client

import server.Database


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     s = Server()
    #     s.serve()
    #     client = Client()
    #     client.run()
    #
    #
    #
    #     self.assertEqual(True, True)
    def test_database(self):
        database = server.Database()
        database.database.query('select * from "test" ')

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
