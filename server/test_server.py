from unittest import TestCase
import Server


class TestServer(TestCase):
    def test_getReading(self):
        server = Server()
        server.get_Reading( )
        self.fail()
